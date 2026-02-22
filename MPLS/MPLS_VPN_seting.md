

![实验拓扑](../image/MPLS/MPLS_VPN/22022600.png)

# PE1 设置

```
PE_1(config)#router ospf 110
PE_1(config-router)#router-id 1.1.1.1

PE_1(config)#int e0/0
PE_1(config-if)#ip address 12.1.1.1 255.255.255.0
PE_1(config-if)#no shu
PE_1(config-if)#ip ospf 110 area 0
PE_1(config-if)#mpls ip

PE_1(config)#int lo0
PE_1(config-if)#ip address 1.1.1.1 255.255.255.255
PE_1(config-if)#no shu
PE_1(config-if)#ip ospf 110 area 0

PE_1(config)#ip vrf VPNA
PE_1(config-vrf)#rd 10000:1
PE_1(config-vrf)#route-target 88:99

PE_1(config)#ip vrf VPNB
PE_1(config-vrf)#rd 10000:3
PE_1(config-vrf)#route-target 66:77

PE_1(config)#int e0/1
PE_1(config-if)#ip vrf forwarding VPNA
PE_1(config-if)#ip address 172.16.1.254 255.255.255.0
PE_1(config-if)#no shu

PE_1(config-if)#int e0/2
PE_1(config-if)#ip vrf forwarding VPNB
PE_1(config-if)#ip address 172.16.3.254 255.255.255.0
PE_1(config-if)#no shu

PE_1(config)#router bgp 10000
PE_1(config-router)#bgp router-id 1.1.1.1
PE_1(config-router)#no bgp default ipv4-unicast

PE_1(config-router)#neighbor 2.2.2.2 remote-as 10000
PE_1(config-router)#neighbor 2.2.2.2 update-source lo0

PE_1(config-router)#address-family vpnv4
PE_1(config-router-af)#neighbor 2.2.2.2 activate


PE_1(config-router)#address-family ipv4 vrf VPNA
PE_1(config-router-af)#neighbor 172.16.1.1 remote-as 65001

PE_1(config-router)#address-family ipv4 vrf VPNB
PE_1(config-router-af)#neighbor 172.16.3.1 remote-as 65003
```

# P1 设置

```
P1(config)#router ospf 110
P1(config-router)#router-id 2.2.2.2

P1(config-router)#int e0/0
P1(config-if)#ip address 12.1.1.2 255.255.255.0
P1(config-if)#no shu
P1(config-if)#ip ospf 110 area 0
P1(config-if)#mpls ip

P1(config)#int e0/1
P1(config-if)#ip address 23.1.1.2 255.255.255.0
P1(config-if)#no shu
P1(config-if)#ip ospf 110 area 0
P1(config-if)#mpls ip

P1(config)#int lo0
P1(config-if)#ip address 2.2.2.2 255.255.255.255
P1(config-if)#no shu
P1(config-if)#ip ospf 110 area 0

P1(config)#router bgp 10000
P1(config-router)#bgp router-id 2.2.2.2
P1(config-router)#no bgp default ipv4-unicast

P1(config-router)#neighbor 1.1.1.1 remote-as 10000
P1(config-router)#neighbor 1.1.1.1 update-source lo0

P1(config-router)#neighbor 4.4.4.4 remote-as 10000
P1(config-router)#neighbor 4.4.4.4 update-source lo0

P1(config-router)#address-family vpnv4

P1(config-router-af)#neighbor 1.1.1.1 activate
P1(config-router-af)#neighbor 1.1.1.1 route-reflector-client

P1(config-router-af)#neighbor 4.4.4.4 activate
P1(config-router-af)#neighbor 4.4.4.4 route-reflector-client
```

# P2 设置

```
P2(config)#router ospf 110
P2(config-router)#router-id 3.3.3.3

P2(config)#int e0/0
P2(config-if)#ip address 23.1.1.3 255.255.255.0
P2(config-if)#no shu
P2(config-if)#ip ospf 110 area 0
P2(config-if)#mpls ip

P2(config)#int e0/1
P2(config-if)#ip address 34.1.1.3 255.255.255.0
P2(config-if)#no shu
P2(config-if)#ip ospf 110 area 0
P2(config-if)#mpls ip

P2(config)#int lo0
P2(config-if)#ip address 3.3.3.3 255.255.255.255
P2(config-if)#no shu
P2(config-if)#ip ospf 110 area 0
```

# PE2 设置

```
PE_2(config)#router ospf 110
PE_2(config-router)#router-id 4.4.4.4

PE_2(config)#ip vrf VPNA
PE_2(config-vrf)#rd 10000:2
PE_2(config-vrf)#route-target 88:99

PE_2(config)#ip vrf VPNB
PE_2(config-vrf)#rd 10000:4
PE_2(config-vrf)#route-target 66:77

PE_2(config)#int e0/0
PE_2(config-if)#ip address 34.1.1.4 255.255.255.0
PE_2(config-if)#no shu
PE_2(config-if)#ip ospf 110  area 0
PE_2(config-if)#mpls ip

PE_2(config)#int e0/1
PE_2(config-if)#ip vrf forwarding VPNA
PE_2(config-if)#ip address 172.16.2.254 255.255.255.0
PE_2(config-if)#no shu

PE_2(config)#int e0/2
PE_2(config-if)#ip vrf forwarding VPNB
PE_2(config-if)#ip address 172.16.4.254 255.255.255.0
PE_2(config-if)#no shu

PE_2(config)#int lo0
PE_2(config-if)#ip address 4.4.4.4 255.255.255.255
PE_2(config-if)#no shu
PE_2(config-if)#ip ospf 110  area 0

PE_2(config)#router bgp 10000
PE_2(config-router)#bgp router-id 4.4.4.4
PE_2(config-router)#no bgp default ipv4-unicast
PE_2(config-router)#neighbor 2.2.2.2 remote-as 10000
PE_2(config-router)#neighbor 2.2.2.2 update-source lo0

PE_2(config-router)#address-family vpnv4
PE_2(config-router-af)#neighbor 2.2.2.2 activate

PE_2(config-router)#address-family ipv4 vrf VPNA
PE_2(config-router-af)#neighbor 172.16.2.1 remote-as 65002

PE_2(config-router)#address-family ipv4 vrf VPNB
PE_2(config-router-af)#neighbor 172.16.4.1 remote-as 65004
```

## CE 配置(例子)
```
CE_1(config)#int e0/0
CE_1(config-if)#ip address 172.16.1.1 255.255.255.0
CE_1(config-if)#no shu
CE_1(config-if)#int lo0
CE_1(config-if)#ip address 192.168.1.1 255.255.255.0
CE_1(config-if)#no shu

CE_1(config)#router bgp 65001
CE_1(config-router)#bgp router-id 192.168.1.1
CE_1(config-router)#neighbor 172.16.1.254 remote-as 10000
CE_1(config-router)#network 192.168.1.0 mask 255.255.255.0

CE_2(config)#int e0/0
CE_2(config-if)#ip address 172.16.2.1 255.255.255.0
CE_2(config-if)#no shu
CE_2(config-if)#int lo0
CE_2(config-if)#ip address 192.168.2.1 255.255.255.0
CE_2(config-if)#no shu

CE_2(config-if)#router bgp 65002
CE_2(config-router)#bgp router-id 192.168.2.1
CE_2(config-router)#neighbor 172.16.2.254 remote-as 10000
CE_2(config-router)#network 192.168.2.0 mask 255.255.255.0
```

## 排错命令

1. 业务连通性与 VRF 基础排错 (第一道防线)

    - show ip vrf / show ip vrf brief

    确认 VRF 是否创建，RD 是否正确，关键是看接口是否成功绑定到了该 VRF 下。

    - show ip vrf detail VPNB

    这是排查路由无法导入导出
    重点检查 Export VPN route-target communities 和 Import 是否与对端 PE 完美匹配。

    - show ip route vrf VPNB

    查看该 VRF 的私网路由表。如果有 B 打头的路由，
    说明控制平面基本通了；注意看下一跳是否是指向对端 PE 的 Loopback。


    - ping vrf VPNB 192.168.2.1 / traceroute vrf VPNB 192.168.2.1

    在 PE 上模拟客户发包。如果 Ping 不通但路由有，
    立刻使用 traceroute 看包死在了哪一跳（通常是标签黑洞）。


2. 控制平面排错：MP-BGP (查路由传没传)

    如果 show ip route vrf 里没有路由，说明 BGP 没把路由送过来，重点查这里。

    - show bgp vpnv4 unicast all summary

    确认与 RR 或对端 PE 的 VPNv4 邻居是否建立。
    最右侧 State/PfxRcd 必须是数字（代表收到的路由条数），
    如果是 Active 或 Idle 说明 TCP/BGP 建连失败。

    - show bgp vpnv4 unicast all

    查看 PE 或 RR 上收到的所有 VPNv4 路由。你能在这里直观地看到路由前面的 Route Distinguisher (RD) 是多少，以及路由是不是最优的 (*>)。

    - show bgp vpnv4 unicast vrf VPNB 192.168.2.0/24 (显微镜命令)

    查看某条特定路由的“DNA”。重点看 Extended Community 里面带的 RT 值对不对，
    以及 BGP 为它分配的内层私网标签 (Local Label / Remote Label)。

3. 数据平面排错：MPLS 与标签 

    如果路由表正常，但就是 Ping 不通，100% 是底层标签断了。

    - show mpls ldp neighbor

    确认骨干网直连链路的 LDP 邻居是否处于 Operational 状态。
    如果起不来，通常是底层 OSPF 没通，或者 Router-ID 无法 Ping 通。

    - show mpls interfaces

    快速确认哪些物理接口成功开启了 Yes (LDP 协议)。排查是否漏敲了 mpls ip。

    - show mpls forwarding-table (LFIB 标签转发表)

    这是数据平面最重要的命令！查找去往对端 PE Loopback（例如 4.4.4.4）的前缀。
    如果显示的 Outgoing Label 是 No Label，说明外层标签没打上，必生黑洞。
    正常应该是具体的数字或 Pop Label (倒数第二跳弹出)。

    - show bgp vpnv4 unicast all labels

    快速总览所有私网路由对应的 内层 VPN 标签。

4. 底层基建排错：IGP 

    一切上层建筑的基础。

    - show ip ospf neighbor

    确认状态是否为 FULL。

    - show ip route ospf

    确认全局路由表里，有没有对端 PE 和 RR 的 Loopback 地址（必须是 /32 掩码）。如果没有，BGP 和 LDP 全都得瘫痪。