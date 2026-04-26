
# 互联网密钥交互协议 IKE Internet Key Exchange

## 主要任务

1. 对建立 IPSec 的双方进行认证

2. 通过密钥交换, 产生用于加密和 HMAC 的随机密钥

3. 协商协议参数(加密协议, 散列函数, 封装模式和密钥有效期)

## 安全关联

IKE 完成以上三步后, 得到一个结果叫做 安全关联 SA.

一种叫做 IKE SA, 一种叫做 IPSec SA.

IKE SA 为第一阶段(相当于 TCP/IP 的三次握手), IPSec SA 为第二阶段(经过认证后, 开始真正加密要传输的数据内容)

## IKE 混合协议

IKE 由 SKEME, Oakley, ISAKMP 组成, 但是 SKEME, Osakley 不炫耀手动配置

1. SKEME 决定 IKE 的密钥交换方式

2. Oakley PESec 框架设计

3. ISAKMP IKE 的本质协议, 决定了包封装与交换, 还有模式切换. **是 IKE 的核心协议**. IKE 和 ISAKMP 是相同概念, 术语可以互相替代

IKE 协议有2个阶段

1. 阶段1 Mainmode 主模式(6个包) Aggressivemode野蛮模式(3个包)

2. 阶段 2Quickmode 快速模式(3个包)

模式

1. Mainmode 主模式

2. Quickmode 快速模式

3. Aggressivemode 野蛮模式(用的比较少, 主要在动态拨号获取 IP 站点的情况下用)

IKE 协商过程就像两个公司做生意的过程。两个公司在具体合作之前需要相互了解，最简单的方法可能就是核查对方公司的工商牌照、公司营业和信誉状况。也很有可能是约一个地点，坐下来面对面地进行介绍和了解。不管怎么样，目的就是相互进行认证，建立基本的信任关系。这个过程其实就是IKE第一个阶段需要完成的任务。第一阶段完成后，信任关系建立了，相应的IKESA 也就建立了。紧接着的主要任务就是基于具体的项目来签订合同。对于IPSec VPN而言，具体的项目就是安全保护通信点之间的流量，具体处理这些流量的策略（IPSec SA）就是合同。IKE第二阶段的任务就是基于需要被加密的流量（A到B）协商相应的IPSec SA。一旦双方在第一阶段建立起了信任关系，它们就没有必要重复进行认证了。接下来，双方的议题就是根据第一阶段建立的IKE SA，给两个站点之间的很多需要被加密的流量协商不同的第二阶段策略（IPSec SA）。

第一阶段既可以使用主模式，也可以使用主动模式来完成，那么什么情况应该使用主模式，什么情况应该使用主动模式呢？以Cisco 的IPSec VPN 为例，只有在一种情况下，第一阶段才会使用3 数据个包交换的主动模式来完成，这就是通过预共享密钥认证的远程访问 VPN（Cisco 的技术名叫做EzVPN），换言之，使用证书认证的EzVPN也是通过6个数据包交换的主模式来完成的。主动模式的交换细节将会在后面 EzVPN 部分进行详细介绍。现在我们需要重点介绍一下主模式6个数据包和快速模式3个数据包，这9个数据包的交换细节。

A 与 B 在阶段一 1,2 包确认对方地址正确, 接收方会尝试匹配发送方的所有 策略 直到能匹配

接收方首先用本地优先的策略（Policy 10）来检查对方所发送过来的全部策略。如果不匹配就由下一个优先的策略来检查，直到找到一个匹配的策略为止。

`show crypto isakmp policy` 可以看到 cisco 的默认策略

`crypto isakmp policy <1-1000>` 建议 10, 20, 30 顺序, 越小越优

```
crypto isakmp policy 10 
hash md5
encryption 3des
authentication pre-share
lifetime 3600
group // 密钥长度

crypto isakmp xxx // 设置一个预共享密钥
// crypto isakmp xxx x.x.x.x 可以指定这个密钥的peer地址, 规定该对等体地址使用这个密钥
```

同样在对等体上需要进行镜像配置



## Diffie-Hellman

diffie hellman 是一个密钥非对称算法公式

这个算法用于 'crypto isakmp key ...' 的密钥

