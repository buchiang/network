# 标记（Marking）是给流量贴标签的动作，让下游所有设备不需要重新分析流量内容，直接看标记就知道怎么处理。

## DSCP 标记

在 policy-map 的 class 块里用 set dscp 完成：

```
policy-map MARK_TRAFFIC
 class VOICE_MEDIA
  set dscp ef           ← 语音，DSCP 46

 class VOICE_SIGNALING
  set dscp cs3          ← 信令，DSCP 24

 class VIDEO
  set dscp af41         ← 视频，DSCP 34

 class CRITICAL_DATA
  set dscp af31         ← 关键数据，DSCP 26

 class BULK_DATA
  set dscp af11         ← 普通数据，DSCP 10

 class MGMT
  set dscp cs2          ← 网管，DSCP 16

 class class-default
  set dscp default      ← 其余清零，DSCP 0
```

### AF 类的内部结构（经常考）

AF（Assured Forwarding）有 4 个类，每类 3 个丢弃优先级，共 12 个值：

```
       丢弃优先级
        低    中    高
AF1x   AF11  AF12  AF13   (DSCP 10, 12, 14)  ← 普通数据
AF2x   AF21  AF22  AF23   (DSCP 18, 20, 22)  ← 中等数据
AF3x   AF31  AF32  AF33   (DSCP 26, 28, 30)  ← 关键数据
AF4x   AF41  AF42  AF43   (DSCP 34, 36, 38)  ← 视频
```

实际用途：Policing 超速时不丢包，而是把 DSCP 降级：

```
 class CRITICAL_DATA
  police rate 5000000 bps
   conform-action transmit
   exceed-action set-dscp-transmit af32   ← AF31 → AF32，同类但丢弃优先级升高
   violate-action set-dscp-transmit af33  ← 再超 → AF33，最容易被 WRED 丢弃
```

这样拥塞时 WRED 优先丢 AF33，保住 AF31，流量降级而不是直接丢弃。

#### CoS 标记

CoS 存在于 802.1Q tag 的 3 位 PCP 字段，只在 L2 帧里有效，路由器转发时会丢失。

```
policy-map MARK_L2
 class VOICE
  set cos 5     ← IP 电话标准值

 class VIDEO
  set cos 4

 class class-default
  set cos 0
```

CoS 和 DSCP 的转换，交换机在 access 口和 trunk 口之间转发时需要互相映射：

```
SW1(config)#mls qos map cos-dscp 0 8 16 24 34 46 48 56
```

这条命令定义 CoS 0→7 分别对应的 DSCP 值，按位置对应：

```
CoS 0 → DSCP 0   (BE)
CoS 1 → DSCP 8
CoS 2 → DSCP 16  (CS2)
CoS 3 → DSCP 24  (CS3)
CoS 4 → DSCP 34  (AF41)
CoS 5 → DSCP 46  (EF)    ← 语音
CoS 6 → DSCP 48  (CS6)
CoS 7 → DSCP 56  (CS7)
```

##### 信任边界的实际配置

CoS 最核心的使用场景就是信任边界，交换机接口上配：

```
SW1(config)#int e0/1           ← 连 IP 电话的端口
SW1(config-if)#mls qos trust cos
```

```
SW1(config)#int e0/2           ← 连 PC 的端口（不信任）
SW1(config-if)#no mls qos trust
```

```
SW1(config)#int g0/0           ← 上行到路由器的 trunk
SW1(config-if)#mls qos trust dscp
```

验证接口信任状态：

```
SW1#show mls qos interface e0/1
Ethernet0/1
  trust state:         trust cos    ← 信任 CoS
  trust mode:          trust cos
  COS override:        dis
  default COS:         0
  DSCP Mutation Map:   Default DSCP Mutation Map
```

###### 同时设置多个标记

一条 `set` 语句只能设一个值，但可以在同一个 class 块里写多条：

```
policy-map DUAL_MARK
 class VOICE
  set dscp ef       ← 设 L3 的 DSCP
  set cos 5         ← 同时设 L2 的 CoS
```

这样不管下游设备看 L2 还是 L3 的标记，都能正确处理。

###### 一个容易混淆的点

`set ip precedence` 和 `set dscp` 操作的是同一个字节（ToS 字段），设了一个另一个会变：

```
set ip precedence 5    → ToS = 0xA0 → DSCP 变成 40（CS5）
set dscp ef            → ToS = 0xB8 → IP Precedence 变成 5
```

现在统一用 `set dscp`，`set ip precedence` 是老命令，新网络不用。Lab 考试如果题目说"设置 IP Precedence 为 5"，直接用 `set dscp cs5`，效果等同。