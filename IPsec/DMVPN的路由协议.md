
![](../image/IPSec/22062600.png)

根据 [DMVPN_原理](DMVPN_原理.md) 的设置, 隧道已经建立成功, 但是所有流量依旧汇聚在中心站点.

## DMVPN EIGRP

(镜像配置)

```
R1(config)#router eigrp 90
R1(config-router)#no auto-summary
R1(config-router)#network 172.16.1.100 0.0.0.0
R1(config-router)#network 192.168.1.0 0.0.0.255
```

邻居建立成功

```
R1#show ip eigrp neighbors
EIGRP-IPv4 Neighbors for AS(90)
H   Address                 Interface              Hold Uptime   SRTT   RTO  Q  Seq
                                                   (sec)         (ms)       Cnt Num
1   172.16.1.2              Tu0                      11 00:01:41    1  1428  0  3
0   172.16.1.1              Tu0                      14 00:02:23    5  1470  0  4
```

```
R1#show ip route eigrp
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is 202.100.1.254 to network 0.0.0.0

D     192.168.2.0/24 [90/27008000] via 172.16.1.1, 00:00:56, Tunnel0
D     192.168.3.0/24 [90/27008000] via 172.16.2.1, 00:00:32, Tunnel0
```

```
R2#show ip route eigrp
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is 202.100.2.254 to network 0.0.0.0

D     192.168.1.0/24 [90/27008000] via 172.16.1.100, 00:16:53, Tunnel0
```

R2 和 R3 只有 R1 的路由, 原因是 EIGRP 的水平分割, R1 从 Tunnel 学习到的路由 不能再从相同接口传出去, 要让分支站点互通需要在中心站点取消水平分割.

```
R1(config)#int tunnel 0
R1(config-if)#no ip split-horizon eigrp 90
```

```
R3#show ip route eigrp
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is 202.100.3.254 to network 0.0.0.0

D     192.168.1.0/24 [90/27008000] via 172.16.1.100, 00:19:23, Tunnel0
D     192.168.2.0/24 [90/28288000] via 172.16.1.100, 00:00:22, Tunnel0
```

现在 R2 和 R3 都能学习到彼此的路由了, 还有一个问题就是彼此的路由还要是经过 R1 via 172.16.1.100

### 分支站点虚拟互联

可以从 trace 里看到这样中心站点的流量负担依旧很重

```
R3#trace 192.168.2.1
Type escape sequence to abort.
Tracing the route to 192.168.2.1
VRF info: (vrf in name/id, vrf out name/id)
  1 172.16.1.100 0 msec 1 msec 1 msec
  2 172.16.1.1 1 msec 1 msec *
```

同样还是要在接口处关掉自己为下一跳

```
R1(config)#int tunnel 0
R1(config-if)#no ip next-hop-self eigrp 90
```

```
R3#trace 192.168.2.1
Type escape sequence to abort.
Tracing the route to 192.168.2.1
VRF info: (vrf in name/id, vrf out name/id)
  1 172.16.1.1 1 msec 1 msec *
```

同样在路由表也能看到, 192.168.2.0 是从 172.16.1.1 来的而不是从中心站点来的

```
R3#show ip route eigrp
Codes: L - local, C - connected, S - static, R - RIP, M - mobile, B - BGP
       D - EIGRP, EX - EIGRP external, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
       i - IS-IS, su - IS-IS summary, L1 - IS-IS level-1, L2 - IS-IS level-2
       ia - IS-IS inter area, * - candidate default, U - per-user static route
       o - ODR, P - periodic downloaded static route, H - NHRP, l - LISP
       a - application route
       + - replicated route, % - next hop override, p - overrides from PfR

Gateway of last resort is 202.100.3.254 to network 0.0.0.0

D     192.168.1.0/24 [90/27008000] via 172.16.1.100, 00:01:40, Tunnel0
D     192.168.2.0/24 [90/28288000] via 172.16.1.1, 00:01:39, Tunnel0
```

## DMVPN OSPF

对于 OSPF 来讲, 他不知道接口是 DMVPN, GRE over IPSec, 如果直接建立邻居, 中心接口会从同一个接口接收到不同邻居的发送的邻居建立报文, 这是违反 OSPF 的设计的

需要手动修改**OSPF网络类型-点到多点**, 因为分支站点之间也会建立虚拟的连接, 所以所有站点都需要建立点到多点.

建立 OSPF 后可以在接口看到

```
R1#show ip ospf interface tunnel 0
Tunnel0 is up, line protocol is up
  Internet Address 172.16.1.100/24, Area 0, Attached via Interface Enable
  Process ID 110, Router ID 202.100.1.100, Network Type POINT_TO_POINT, Cost: 1000
  Topology-MTID    Cost    Disabled    Shutdown      Topology Name
        0           1000      no          no            Base
  Enabled by interface config, including secondary ip addresses
  Transmit Delay is 1 sec, State POINT_TO_POINT
  Timer intervals configured, Hello 10, Dead 40, Wait 40, Retransmit 5
    oob-resync timeout 40
    Hello due in 00:00:02
  Supports Link-local Signaling (LLS)
  Cisco NSF helper support enabled
  IETF NSF helper support enabled
  Index 1/1/1, flood queue length 0
  Next 0x0(0)/0x0(0)/0x0(0)
  Last flood scan length is 0, maximum is 0
  Last flood scan time is 0 msec, maximum is 0 msec
  Neighbor Count is 0, Adjacent neighbor count is 0
  Suppress hello for 0 neighbor(s)
```

`Process ID 110, Router ID 202.100.1.100, Network Type POINT_TO_POINT, Cost: 1000`

OSPF 默认是点到点, 并且因为是隧道, Cisco 会把开销设置到1000

### 点到多点设置

镜像配置

```
R1(config)#interface tunnel 0
R1(config-if)#ip ospf network point-to-multipoint
```

### 分支站点虚拟互联

改为点到多点后, 邻居成功建立

```
R3#show ip route ospf
......
      172.16.0.0/16 is variably subnetted, 4 subnets, 2 masks
O        172.16.1.1/32 [110/2000] via 172.16.1.100, 00:00:57, Tunnel0
O        172.16.1.100/32 [110/1000] via 172.16.1.100, 00:00:57, Tunnel0
      192.168.1.0/32 is subnetted, 1 subnets
O        192.168.1.1 [110/1001] via 172.16.1.100, 00:00:57, Tunnel0
      192.168.2.0/32 is subnetted, 1 subnets
O        192.168.2.1 [110/2001] via 172.16.1.100, 00:00:57, Tunnel0
```

由于 OSPF 原理目前不能阶段不能像 EIGRP 一样解决中心站点负载, 因为 OSPF 是链路状态协议, 现在不能优化下一跳

## DMVPN BGP

BGP 的 AS 号是一种资源, 所以多数情况各个分支站点会用同一个 AS 号, 这时候就需要 allowas-in

R1

```
R1(config)#router bgp 65001
R1(config-router)#bgp router-id 1.1.1.1
R1(config-router)#neighbor 172.16.1.1 remote-as 65002
R1(config-router)#neighbor 172.16.1.2 remote-as 65002
R1(config-router)#network 192.168.1.0 mask 255.255.255.0
```

R2, R3 镜像配置

```
R2(config)#router bgp 65002
R2(config-router)#bgp router-id 2.2.2.2
R2(config-router)#neighbor 172.16.1.100 remote-as 65001
R2(config-router)#neighbor 172.16.1.100 allowas-in 1
R2(config-router)#network 192.168.2.0 mask 255.255.255.0
```

```
R3#show ip bgp
......

     Network          Next Hop            Metric LocPrf Weight Path
 *>   192.168.1.0      172.16.1.100             0             0 65001 i
 *>   192.168.2.0      172.16.1.1                             0 65001 65002 i
 *>   192.168.3.0      0.0.0.0                  0         32768 i
```

现在可以看到接收到了路由, 同样也是因为 BGP 特性, EBGP 会传递邻居路由, 如果是 IBGP 就需要做路由反射

### BGP 下一跳优化

```
R3#show ip route bgp

......

B     192.168.1.0/24 [20/0] via 172.16.1.100, 00:02:14
B     192.168.2.0/24 [20/0] via 172.16.1.1, 00:02:14
```

可以看到 BGP 直接从不同站点学到的不同路由, 不需要修改下一跳.

## 后记

```
R3#traceroute 192.168.2.1 source 192.168.3.1
Type escape sequence to abort.
Tracing the route to 192.168.2.1
VRF info: (vrf in name/id, vrf out name/id)
  1 172.16.1.100 1 msec
    172.16.1.1 1 msec 1 msec
R3#traceroute 192.168.2.1 source 192.168.3.1
Type escape sequence to abort.
Tracing the route to 192.168.2.1
VRF info: (vrf in name/id, vrf out name/id)
  1 172.16.1.1 1 msec 5 msec *
```

在 DMVPN 第一次访问分支站点的时候是需要经过中心站点的, 因为分支站点不知道另外一个分支站点的公网 IP, 在后续学习到对应分支站点的公网 IP 后, 就不用再经过中心站点的, DMVPN 在没有流量经过的时候, 是不会往另外分支站点发送报文的.

