# QoS 分类是整个 QoS 流水线的入口，分类准确，后面所有策略才有意义。一共四种匹配方式，从简单到复杂：

## 方式一：match dscp（最常用）

流量已经被上游设备打好了 DSCP 标记，直接匹配值就行。配置最简单，性能最好。

```
class-map match-any VOICE
 match dscp ef          ← 匹配 DSCP 46

class-map match-any VIDEO
 match dscp af41        ← 可以写名称
 match dscp 34          ← 也可以写十进制，效果一样

class-map match-any BULK_DATA
 match dscp af11 af12 af13   ← 一行可以写多个值
```
`match-any` 表示匹配任意一个条件就算命中（OR 逻辑）。match-all 是 AND 逻辑，多个 match 条件必须全部满足，用得少。

### 方式二：match protocol（NBAR）

NBAR（Network-Based Application Recognition）深度识别应用层协议，不依赖端口号，能识别动态端口的应用。需要在接口上开启 `ip nbar protocol-discovery`。

```
class-map match-any VOICE_SIGNALING
 match protocol sip       ← SIP 信令
 match protocol skinny    ← Cisco SCCP 信令
 match protocol h323      ← H.323 信令

class-map match-any VOICE_MEDIA
 match protocol rtp audio ← RTP 语音流（只匹配音频）

class-map match-any VIDEO_CONF
 match protocol rtp video ← RTP 视频流

class-map match-any WEB
 match protocol http
 match protocol https
 match protocol quic      ← HTTP/3

class-map match-any STREAMING
 match protocol youtube
 match protocol netflix   ← 部分版本支持
```

接口开启协议发现：

```
R1(config)#int e0/1
R1(config-if)#ip nbar protocol-discovery
```

**验证 NBAR 识别到哪些协议：**

```
R1#show ip nbar protocol-discovery interface e0/1
Interface e0/1
    Input                          Output
    Protocol        Packet Count   Packet Count
    --------------- -------------- --------------
    http            1234           5678
    rtp             890            345
    unknown         100            200   ← 无法识别的协议
```

`unknown` 过高说明有流量没被 NBAR 识别，需要自定义协议或用 ACL 补充匹配。

### 方式三：match access-group（ACL）

最精确，可以精确到源 IP、目的 IP、端口号的组合。常用于匹配特定服务器或特定业务系统的流量。

```
ip access-list extended MGMT_ACL
 permit tcp 10.0.0.0 0.0.0.255 any eq 22    ← SSH
 permit udp any any eq 161                   ← SNMP
 permit udp any any eq 162                   ← SNMP Trap

ip access-list extended ORACLE_DB
 permit tcp any 172.16.100.0 0.0.0.255 eq 1521  ← Oracle 数据库

class-map match-any MGMT
 match access-group name MGMT_ACL

class-map match-any DATABASE
 match access-group name ORACLE_DB
```

#### 方式四：match cos（二层标记）

用于交换机接口，匹配以太网帧的 CoS（Class of Service）值，在 802.1Q trunk 帧头里，3 位，值 0–7。

```
class-map match-any VOICE_L2
 match cos 5        ← IP 电话通常打 CoS 5

class-map match-any VIDEO_L2
 match cos 4
```

CoS 只存在于带 802.1Q tag 的帧里，路由器的路由接口看不到 CoS，只有交换机或子接口才能用。

##### 组合使用：分类 + 立即标记

实际部署里，流量进来时往往没有 DSCP，或者不信任终端打的标记。标准做法是在入向先用 NBAR 或 ACL 分类，同时打上 DSCP，后续设备统一用 `match dscp` 处理：

```
policy-map CLASSIFY_AND_MARK
 class VOICE_SIGNALING        ← NBAR 匹配 SIP/SCCP
  set dscp cs3
 class VOICE_MEDIA            ← NBAR 匹配 RTP audio
  set dscp ef
 class DATABASE               ← ACL 匹配数据库流量
  set dscp af31
 class class-default
  set dscp default            ← 其余清零，不信任终端的标记

interface e0/0
 service-policy input CLASSIFY_AND_MARK
```

流量出去时用 `match dscp` 的 policy-map 做队列调度，两个 policy-map 分工明确，入向分类标记，出向队列调度。这是 Lab 考试最标准的 QoS 架构。

**选哪种方式的判断原则：**

|场景|推荐方式|
|:--:|:--:|
|上游已打好|DSCPmatch dscp|
|需要识别应用（动态端口）|match protocol
|(NBAR)精确到特定 IP/端口|match access-group|
|交换机 L2 场景|match cos|
|不信任终端标记|NBAR/ACL 分类 + set dscp 重新标记|