
两者最本质的区别只有一句话：Policing 超速就丢（或降级），Shaping 超速就等。

# Token Bucket 模型

两者都基于令牌桶，先理解桶才能理解行为。

```
令牌以 CIR 速率持续注入桶中
                    ┌─────────┐
令牌注入 ──────────▶│  BC 桶  │ 容量 = Bc
                    └────┬────┘
                         │ 流量消耗令牌
                    ┌────▼────┐
流量到来 ──────────▶│  判断   │──▶ conform：令牌够 → 转发
                    └─────────┘──▶ exceed：令牌不够 → 丢/降级/入队
```

Policing 有两个桶（Bc + Be），Shaping 只有一个桶（Bc）。

# Policing（限速）

超速立即处理（丢弃或降级），不缓冲，不引入额外延迟。用于入向居多，也可用于出向。

```
policy-map POLICE_DEMO
 class VOICE
  police rate 1000000 bps burst 8000
   conform-action transmit
   exceed-action  drop

 class CRITICAL_DATA
  police rate 4000000 bps burst 32000
   conform-action transmit
   exceed-action  set-dscp-transmit af32   ← 超速降级，不丢包
   violate-action set-dscp-transmit af33   ← 严重超速再降一级

 class class-default
  police rate percent 30                   ← 按接口带宽百分比，更灵活
   conform-action transmit
   exceed-action  drop
```

`burst` 值的计算参考：`burst = CIR × 1.5 / 8`（单位 bytes），也可以直接写经验值，Lab 考试不精确计算，写合理值就行。

## 验证：

```
R1#show policy-map interface e0/0 input
  Class-map: VOICE
    police:
      rate 1000000 bps, burst 8000 bytes
      conform 5230 packets   ← 正常转发
      exceed  12 packets     ← 超速，被丢弃
      violate 0 packets
```

# Shaping（整形）

超速的流量不丢弃，放入缓冲队列等待，等令牌恢复后再发送。流量曲线被"削峰填谷"变得平滑。只能用于出向，因为需要缓冲队列。

```
policy-map SHAPE_DEMO
 class class-default
  shape average 2000000          ← 整形到 2Mbps
```

更精细的做法，按流量类型分别整形：

```
policy-map SHAPE_PER_CLASS
 class VOICE
  shape average 500000           ← 语音整形到 500kbps

 class VIDEO
  shape average 1000000          ← 视频整形到 1Mbps

 class class-default
  shape average 500000
```

Shaping 还可以嵌套 policy-map，整形之后再做内部队列调度——这是 Hierarchical QoS（HQoS），Lab 高频考点：

```
policy-map INNER_POLICY          ← 内层：定义队列优先级
 class VOICE
  priority percent 30
 class class-default
  bandwidth percent 70

policy-map OUTER_POLICY          ← 外层：整形 + 嵌套内层
 class class-default
  shape average 2000000          ← 先整形到 2Mbps
  service-policy INNER_POLICY    ← 在整形后的带宽内再做队列调度
```

应用到接口：

```
R1(config)#int e0/1
R1(config-if)#service-policy output OUTER_POLICY
```

## 验证：

```
R1#show policy-map interface e0/1 output
  Class-map: class-default
    Queueing
    queue limit 64 packets
    shape (average) cir 2000000, bc 8000, be 8000
    target shape rate 2000000

    Service-policy : INNER_POLICY        ← 嵌套的内层 policy
      Class-map: VOICE
        priority
        Output Queue: Conversation 24
        Bandwidth 600 kbps               ← 2Mbps × 30%
```

# 直观对比

```
流量速率

  │     超速部分
  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  │  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  ├──────────────────────── CIR 速率限制
  │
  └───────────────────────▶ 时间

Policing 处理结果：
  │  ■■■■■■■■
  ├──────────────────────── CIR
  │  超速部分 → 直接丢弃或降级

Shaping 处理结果：
  │  ■■■■■■■■■■■■■■■■■■■■   ← 流量被"拉平"
  ├──────────────────────── CIR
  │  超速部分 → 缓冲后延迟发送
```

# 选哪个的判断逻辑

|场景|用哪个|原因|
|:--:|:--:|:--:|
|运营商接入边界，入向限速|Policing|入向只能用 Policing|
|对接运营商专线，速率匹配|Shaping|平滑流量，不触发对端 Policing|
语音流量保护|Policing|超速立即丢，不引入队列延迟|
|TCP 数据流量|Shaping|缓冲比丢弃好，TCP 能重传|
Frame Relay / ATM 子接口|Shaping|经典场景，现在少见但 Lab 可能考|

# 一个容易出错的细节

Shaping 的 `bc`（Committed Burst）会影响整形的精度：

```
shape average 2000000 bc 8000
```

`bc` 越小，整形越精确但 CPU 开销越大；`bc` 越大，流量突发越明显但 CPU 开销小。不指定时 IOS 自动计算，Lab 考试不需要手动调，写 `shape average [速率] 就够了`。

Policing 的 `burst` 和 Shaping 的 `bc` 是同一个概念，但 Policing 还有第二个桶 `be`（Excess Burst），允许更大的短时突发后再丢弃。大多数场景不用显式配置 `be`，让 IOS 用默认值。