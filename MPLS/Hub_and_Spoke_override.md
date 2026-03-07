
[](Hub_and_Spoke_override.md)

在实际业务环境中, 大多数客户只会分配同样的 AS, 这时候就需要 override 将私网 AS 转换为公网 AS

## 配置

前期配置依照 [Hub&Spoke](MPLS_VPN_Hub&Spoke.md)

## 关键配置

PE_1

```
PE_1(config)#router bgp 10000
PE_1(config-router)#address-family ipv4 vrf HUBIN
PE_1(config-router-af)#neighbor 172.16.10.1 as-override
// 将 CE_1 发给 PE_1 的 BGP 路由将 AS 转为 10000

PE_1(config-router)#address-family ipv4 vrf HUBOUT
PE_1(config-router-af)#neighbor 172.16.20.1 allowas-in 2
// 要允许带有 AS 10000 的 BGP 路由重回 AS 10000
```

PE_2

```
PE_2(config)#router bgp 10000
PE_2(config-router)#address-family ipv4 vrf SPOKE1
PE_2(config-router-af)#neighbor 172.16.2.1 as-override
```

将 CE_2 发给 PE_2 的 BGP 路由将 AS 转为 10000

PE_3

```
PE_3(config)#router bgp 10000
PE_3(config-router)#address-family ipv4 vrf VPNB
PE_3(config-router-af)#neighbor 172.16.3.1 as-override
```

将 CE_3 发给 PE_3 的 BGP 路由将 AS 转为 10000

```
CE_1#ping 192.168.2.1 source 192.168.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.2.1, timeout is 2 seconds:
Packet sent with a source address of 192.168.1.1
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/2 ms
CE_1#ping 192.168.3.1 source 192.168.1.1
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.3.1, timeout is 2 seconds:
Packet sent with a source address of 192.168.1.1
!!!!!
Success rate is 100 percent (5/5), round-trip min/avg/max = 1/1/2 ms

CE_1#show ip bgp
BGP table version is 4, local router ID is 192.168.1.1
Status codes: s suppressed, d damped, h history, * valid, > best, i - internal,
              r RIB-failure, S Stale, m multipath, b backup-path, f RT-Filter,
              x best-external, a additional-path, c RIB-compressed,
              t secondary path,
Origin codes: i - IGP, e - EGP, ? - incomplete
RPKI validation codes: V valid, I invalid, N Not found

     Network          Next Hop            Metric LocPrf Weight Path
 *>   192.168.1.0      0.0.0.0                  0         32768 i
 *>   192.168.2.0      172.16.10.254                          0 10000 10000 i
 *>   192.168.3.0      172.16.10.254                          0 10000 10000 i
```