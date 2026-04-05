
队列是 QoS 里最核心的部分——前面的分类和标记都是为了这一步服务的。拥塞发生时，队列决定谁先发、谁后发、谁被丢。

# 没有 QoS 时发生什么

默认情况下所有流量进同一个 FIFO 队列，先进先出。语音包和大文件传输混在一起，大文件占满队列，语音包排在后面等待，产生抖动和延迟，通话质量崩溃。

# CBWFQ（Class-Based Weighted Fair Queuing）

给每个 class 一个独立的队列，按权重（bandwidth）分配带宽。拥塞时保证每个 class 至少能得到分配的带宽，不拥塞时可以借用空闲带宽。

```
policy-map CBWFQ_DEMO
 class CRITICAL_DATA
  bandwidth percent 30      ← 保证 30% 带宽

 class BULK_DATA
  bandwidth percent 20      ← 保证 20% 带宽

 class MGMT
  bandwidth percent 10      ← 保证 10% 带宽

 class class-default
  bandwidth percent 40      ← 剩余 40% 给默认流量
  fair-queue                ← default class 内部再做公平队列
```

`bandwidth` 有三种写法：

```
bandwidth 1000              ← 绝对值，单位 kbps
bandwidth percent 30        ← 接口带宽的百分比（推荐，适配不同速率接口）
bandwidth remaining percent 30  ← 剩余带宽的百分比（LLQ 之后的剩余部分）
```

# LLQ（Low Latency Queuing）

在 CBWFQ 基础上加一个严格优先队列（Priority Queue）。这个队列里的流量永远最先发送，不需要等待其他队列。专为语音这类对延迟极度敏感的流量设计。

```
policy-map LLQ_DEMO
 class VOICE
  priority percent 20       ← 严格优先，保证 20% 带宽且最先发送

 class VIDEO
  bandwidth percent 30      ← CBWFQ，保证带宽但不绝对优先

 class CRITICAL_DATA
  bandwidth percent 20

 class class-default
  bandwidth percent 30
  fair-queue
```

`priority` 和 `bandwidth` 的本质区别：

```
priority  → 严格优先，队列里有就先发，其他队列等待
            适合：语音、实时交互流量
            风险：流量过大会饿死其他队列

bandwidth → 按权重调度，拥塞时按比例分配
            适合：数据、视频等可以稍微等待的流量
            安全：不会饿死其他队列
```

# Priority 配合 Police 防饥饿

`priority` 本身没有上限，如果语音流量突然暴增，会把所有带宽都占了。所以生产配置里 LLQ 必须配合 Policing：

```
policy-map LLQ_WITH_POLICE
 class VOICE
  priority percent 20
  police rate percent 20
   conform-action transmit
   exceed-action  drop      ← 超过 20% 的语音直接丢
```

这样语音最多只能用 20% 带宽，超出的异常流量（比如语音编解码器故障产生的垃圾包）直接丢弃，不影响其他队列。

# Queue Limit（队列深度）

每个 class 的队列有最大长度限制，超出则 tail-drop：

```
policy-map QUEUE_LIMIT_DEMO
 class VOICE
  priority percent 20
  queue-limit 32 packets    ← 语音队列最多 32 个包，满了直接丢

 class CRITICAL_DATA
  bandwidth percent 30
  queue-limit 64 packets    ← 数据队列可以深一点
```

语音队列应该设得浅：队列越深，排队延迟越大，语音质量越差。语音包宁可丢掉也不要延迟太久（丢包可以靠 jitter buffer 掩盖，但延迟超过 150ms 就能明显感觉到）。

# 完整 LLQ + CBWFQ 生产模板

```
class-map match-any VOICE
 match dscp ef

class-map match-any VIDEO
 match dscp af41

class-map match-any SIGNALING
 match dscp cs3

class-map match-any CRITICAL_DATA
 match dscp af31

class-map match-any BULK_DATA
 match dscp af21 af11

class-map match-any MGMT
 match dscp cs2

policy-map WAN_QUEUING
 class VOICE
  priority percent 20           ← LLQ：语音严格优先
  police rate percent 20
   conform-action transmit
   exceed-action  drop

 class VIDEO
  bandwidth percent 25          ← CBWFQ：视频保证带宽
  queue-limit 64 packets

 class SIGNALING
  bandwidth percent 5

 class CRITICAL_DATA
  bandwidth percent 20
  random-detect dscp-based      ← WRED：主动丢弃，避免 tail-drop

 class BULK_DATA
  bandwidth percent 10
  random-detect dscp-based

 class MGMT
  bandwidth percent 5

 class class-default
  bandwidth percent 15          ← 剩余给普通流量
  fair-queue
  queue-limit 128 packets

interface e0/1
 service-policy output WAN_QUEUING
```

## 验证输出解读

```
R1#show policy-map interface e0/1
 Service-policy output: WAN_QUEUING

  Class-map: VOICE (match-any)          ← class 名称
    5230 packets, 418400 bytes
    5 minute offered rate 84000 bps     ← 实际流量速率
    drop rate 0 bps                     ← 丢包率，语音应该是 0
    Match: dscp ef (46)
    Strict Priority                     ← 确认是 LLQ
    Output Queue: Conversation 24
    Bandwidth 2000 kbps                 ← 20% × 10Mbps 接口
    Burst 50000 bytes
    police:
      rate 2000000 bps
      conform 5230 packets              ← 正常发送
      exceed  0 packets                 ← 超速，应接近 0

  Class-map: CRITICAL_DATA (match-any)
    1200 packets, 96000 bytes
    5 minute offered rate 20000 bps
    drop rate 0 bps
    Match: dscp af31 (26)
    Queueing
    queue limit 64 packets
    (queue depth/total drops/no-buffer drops) 0/0/0
    exponential weight: 9               ← WRED 参数
    mean queue depth: 2

  Class-map: class-default (match-any)
    800 packets, 64000 bytes
    5 minute offered rate 12000 bps
    drop rate 0 bps
    Match: any
    Weighted fair queueing              ← fair-queue 生效
```

关键看三个数字：`offered rate`（进来多少）、`drop rate`（丢了多少）、`queue depth`（队列当前深度）。语音的 `drop rate` 必须是 0，`queue depth` 必须接近 0，否则配置有问题。

# 最常见的考试陷阱

`priority` 和 `bandwidth` 不能在同一个 class 里同时写：

```
class VOICE
 priority percent 20
 bandwidth percent 20    ← 错误！两者互斥，IOS 会报错
```

所有非 priority class 的 bandwidth percent 加上 priority percent 总和不能超过 100%，否则 service-policy 挂接时报错：

```
% Failed: bandwidth sum for all classes exceeds 100%
```

`class-default` 必须写，否则不在任何 class 里的流量没有队列保证，在拥塞时可能完全得不到带宽。