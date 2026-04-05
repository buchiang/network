
## 1. 理论 DSCP 值速查表 & 信任边界

[分类 ](<QoS 分类 Classification 的 NBAR 和 DSCP 匹配方法.md>) ➡ [标记](<QoS 标记 Marking 的 DSCP 值和 CoS 的使用场景.md>) ➡ [限速/整形](<QoS Policing 限速和 Shaping 整形的区别和配置.md>) ➡ [队列](<QoS 队列 Queuing 的 CBWFQ 和 LLQ 配置.md>) ➡ [丢弃](<QoS 丢弃策略 WRED 的配置和 tail-drop 的区别.md>)

|Classification|Marking|Police / Shape|CBWFQ / LLQ|WRED|
|:--:|:--:|:--:|:--:|:--:|
|match protocol|set dscp ef|police rate|priority (LLQ)|randomdetect|
|match dscp|set dscp af31|conform transmit|bandwidth||
|match access-group|set cos 5|exceed drop|fair-queue||

- DSCP 是 QoS 的通用货币

    1. DSCP（Differentiated Services Code Point）占 IP 头 ToS 字段的 6 位，共 64 个值。

    2. 网络设备根据 DSCP 值决定如何处理流量，不同厂商设备互认同一套 DSCP 标准。

|流量类型|DSCP 名称|十进制|十六进制|用途|
|:---:|:--:|:---:|:---:|:---:|
|语音 RTP|EF|46|0x2E|LLQ priority 队列|
|视频|AF41|34|0x22|保证带宽队列|
|呼叫信令|CS3|24|0x18|保证带宽队列|
|关键数据|AF31|26|0x1A|保证带宽队列|
|普通数据|AF21|18|0x12|尽力而为队列|
|网管流量|CS2|16|0x10|低优先级保证|
|默认/其余|BE (CS0)|0|0x00|默认队列|

- 信任边界（Trust Boundary）— Lab 必考概念

- 信任边界决定"从哪里开始相信数据包携带的 DSCP/CoS 标记"。

    - 接入交换机连 IP 电话的端口：trust cos（相信电话打的 CoS）

    - 连 PC 的端口：不信任，重新分类标记（PC 可能乱打标记）

    - 路由器 WAN 接口入向：trust dscp（相信对端打的 DSCP）

`mls qos trust dscp`（交换机接口命令）

`mls qos trust cos`（信任 CoS，L2 标记）

## 2 分类 lass-map：定义流量分类

class-map 是 QoS 的"分拣机"，定义什么流量属于哪一类。match-any = OR 逻辑，match-all = AND 逻辑（默认）。

**三种常用匹配方式**

```
--- 方式一：匹配 DSCP 值（最常用，端到端一致）---
class-map match-any VOICE
 match dscp ef                  匹配语音 RTP 流量

class-map match-any VIDEO
 match dscp af41

class-map match-any CRITICAL_DATA
 match dscp af31

--- 方式二：匹配协议（需要 NBAR）---
class-map match-any VOICE_NBAR
 match protocol rtp audio       NBAR 识别 RTP 语音
 match protocol skinny          Cisco 电话信令
 match protocol sip             SIP 信令

--- 方式三：匹配 ACL（精确控制源/目的）---
ip access-list extended MGMT_TRAFFIC
 permit tcp 10.0.0.0 0.0.0.255 any eq 22
 permit udp any any eq 161

class-map match-any MGMT
 match access-group name MGMT_TRAFFIC
 ```

*class-default 是内置的兜底 class，匹配所有不属于其他 class 的流量。policy-map 最后一条必须有 class class-default，否则不符合 class 的流量没有任何 QoS 处理（相当于 best-effort）。*

## 3 策略 policy-map：定义每类流量的处理动作

policy-map 把 class-map 和处理动作绑在一起。每个 class 块可以有标记、限速、队列三种动作，组合使用。

**完整三类流量 policy-map（语音 + 视频 + 数据）**

```
policy-map ENTERPRISE_QOS

 class VOICE
  priority percent 20
  LLQ：给语音预留 20% 带宽，严格优先发送
  priority 后不能再加 bandwidth，两者互斥

 class VIDEO
  bandwidth percent 30
  CBWFQ：保证视频至少有 30% 带宽
  fair-queue
  在 VIDEO class 内部再做公平队列

 class CRITICAL_DATA
  bandwidth percent 20
  random-detect dscp-based
  WRED：基于 DSCP 的随机早期检测，避免 tail-drop

 class MGMT
  bandwidth percent 5

 class class-default
  bandwidth percent 25
  剩余带宽给普通流量，必须写这条
  fair-queue
```

percent 总和不能超过 100%，但 class-default 的 bandwidth percent 不计入限制。priority class 的带宽不参与其他 class 的带宽计算，可以理解为"额外保留"。实际上只要非 priority class 的 bandwidth percent 之和 ≤ 100% 即可。

- priority vs bandwidth 的本质区别：

    1. priority = LLQ，严格优先，队列里有就先发，专为语音/实时流量设计，但有饿死其他流量的风险，所以通常配合 police 限速使用。

    2. bandwidth = CBWFQ，拥塞时保证最低带宽，不拥塞时可以借用空闲带宽，适合数据类流量。

## 4 限速 Policing：入向限速

**Token Bucket 双桶模型**

- CIR（Committed Information Rate）：承诺速率，正常情况允许的速率

- BC（Committed Burst）：承诺突发，短时间内允许超过 CIR 的量（第一个桶）

- BE（Excess Burst）：超额突发，更大的短时突发（第二个桶，仅 Policing 有）

conform = 在 CIR 内 → 通常 transmit

exceed = 超过 CIR 但在 BC+BE 内 → 通常 transmit 或 set-dscp-transmit（降级）

violate = 超过所有限制 → 通常 drop

**场景：对进入路由器的流量做 Policing（常用于运营商接入边界）**

```
policy-map INGRESS_POLICE

 class VOICE
  police rate 1000000 bps burst 10000
   conform-action transmit
   exceed-action drop
   语音流量超速直接丢，保证低延迟

 class CRITICAL_DATA
  police rate 5000000 bps burst 50000
   conform-action transmit
   exceed-action set-dscp-transmit af11
   超速不丢弃，把 DSCP 降级（af31→af11）再转发
   violate-action drop

 class class-default
  police rate percent 50
   按接口带宽百分比限速，更灵活
   conform-action transmit
   exceed-action drop
```

1. Policing（限速）

    - 超速 → 立即丢弃

    - 不平滑流量

    - 用于入向（in）

    - 引入额外延迟少

2. Shaping（整形）

    - 超速 → 进缓冲队列等待

    - 平滑流量曲线

    - 只用于出向（out）

    - 引入额外延迟

## 5 应用 ervice-policy：应用到接口

policy-map 只是定义，必须用 service-policy 挂到接口才生效。方向选择是关键：in 做分类标记和 Policing，out 做队列和 Shaping。

**完整配置：入向分类标记 + 出向队列**

```
--- 出向 policy：队列调度（应用在 WAN 出口）---
R1(config)#int e0/1
R1(config-if)#service-policy output ENTERPRISE_QOS
output = 出向，流量从这个接口发出时做队列调度

--- 入向 policy：分类 + Policing（应用在 WAN 入口）---
R1(config)#int e0/0
R1(config-if)#service-policy input INGRESS_POLICE
input = 入向，流量进来时做分类和限速
```

**在 policy-map 里嵌套标记（分类 + 标记一起做）**

```
--- 如果流量进来时没有 DSCP 标记，在入向 policy 里先标记 ---
policy-map CLASSIFY_AND_MARK
 class VOICE_NBAR
  set dscp ef              语音打 EF
 class VIDEO_NBAR
  set dscp af41            视频打 AF41
 class class-default
  set dscp default         其余清零

R1(config)#int e0/0
R1(config-if)#service-policy input CLASSIFY_AND_MARK
入向标记后，出向 ENTERPRISE_QOS 就能用 match dscp 正确分类
```

一个接口的同一方向只能挂一个 service-policy。如果要同时做分类标记和 Policing，把两个动作写在同一个 policy-map 里，不能挂两个 policy。

## 6 综合实验 完整端到端实验配置

拓扑：R1（LAN侧）— e0/0 — R2（WAN边界）— e0/1 — R3（远端）。在 R2 的 e0/1 出向做完整 QoS。

**R2 — 完整 QoS 配置（生产可用模板）**

```
--- Step A：定义 class-map ---
class-map match-any VOICE
 match dscp ef
class-map match-any VIDEO
 match dscp af41
class-map match-any SIGNALING
 match dscp cs3
class-map match-any DATA
 match dscp af31 af21
class-map match-any MGMT
 match dscp cs2

--- Step B：定义 policy-map ---
policy-map WAN_OUT
 class VOICE
  priority percent 20
  police rate percent 20
   conform-action transmit
   exceed-action drop
  LLQ 配合 Policing：防止语音独占所有带宽

 class VIDEO
  bandwidth percent 30

 class SIGNALING
  bandwidth percent 5

 class DATA
  bandwidth percent 20
  random-detect dscp-based

 class MGMT
  bandwidth percent 5

 class class-default
  bandwidth percent 20
  fair-queue

--- Step C：应用到接口 ---
R2(config)#int e0/1
R2(config-if)#service-policy output WAN_OUT
```

### 验证：show policy-map interface 输出解读

```
R2#show policy-map interface e0/1
 Service-policy output: WAN_OUT

  Class-map: VOICE (match-any)
    0 packets, 0 bytes        ← 如果为 0 说明没流量命中，检查 class-map
    5 minute offered rate 1000 bps, drop rate 0 bps
    Match: dscp ef (46)
    Queueing
      Priority: 20% (2000 kbps), burst bytes 50000
      Output Queue: Conversation 24
    police:
        rate 2000000 bps
        conform 1234 packets   ← 正常转发的包数
        exceed  0 packets      ← 超速的包数（应该接近 0）

  Class-map: class-default (match-any)
    100 packets, 10000 bytes
    5 minute offered rate 500 bps, drop rate 0 bps
    Match: any
```

## 7 进阶 WRED — 主动队列管理

- 为什么需要 WRED？

    1. 传统 Tail-Drop：队列满了才丢包，且同时丢弃所有 TCP 流量，导致所有 TCP 流同时触发拥塞控制，带宽利用率骤降（TCP 全局同步问题）。

    2. WRED（Weighted Random Early Detection）：队列还没满时就开始随机丢包，让不同 TCP 流在不同时间触发拥塞控制，避免全局同步，维持更高的带宽利用率。

**WRED 的三个门限**

1. min-threshold：低于此值不丢包

2. max-threshold：超过此值全部丢包（等同 tail-drop）

3. 介于两者之间：按概率随机丢包，DSCP 值高的丢弃概率低

**配置方式（在 policy-map 的 class 块里）**

```
policy-map WAN_OUT
 class DATA
  bandwidth percent 20
  random-detect              默认 WRED，基于 IP Precedence

 class DATA
  bandwidth percent 20
  random-detect dscp-based   推荐：基于 DSCP 值差异化丢弃概率
  AF31（26）比 AF21（18）丢弃概率低，高优先数据更受保护
```

### 验证 WRED 工作状态

```
R2#show policy-map interface e0/1 class DATA
  Class-map: DATA
    Queueing
    queue limit 64 packets
    (queue depth/total drops/no-buffer drops) 0/0/0
    exponential weight: 9
    mean queue depth: 0

    dscp    min-th  max-th  mark-prob
    ------------------------------------------
    af31      28      40       1/10    AF31 门限更宽松
    af21      24      40       1/10
    default   20      40       1/10    默认最容易被丢弃
```

### QoS 排错命令速查
`show policy-map interface [接口]`        # 最重要的命令，看每个 class 的统计

`show policy-map interface [接口] input`  # 只看入向

`show policy-map interface [接口] output` # 只看出向

`show class-map [name]`                   # 查 class-map 定义

`show policy-map [name]`                  # 查 policy-map 结构

`show interfaces [接口] | inc rate`       # 看接口速率

`debug qos`                               # 实时调试（生产谨慎）