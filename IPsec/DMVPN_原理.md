
**动态多点VPN** 重点

**Hub&Spoke 组网问题**

1. 中心站点配置量大, 每多一个分支站点就需要增加一份配置, 管理也会更麻烦

2. 分支站点时间流量延迟大, 各分支站点之间没有隧道不能直接通信, 所有流量都需要通过中心站点转发

3. 分支站点间流量占用中心贷款, 因为所有流量都需要通过中心站点转发, 所以会消耗中心站点大量带宽

**全互联组网问题**

1. 中心与分支站点配置量大

2. 分支站点需要维护大量 IPSec sa

3. 每个分支站点都需要一个固定 IP 地址, 导致成本增加

# DMVPN 的优点

1. 简单的星形拓扑配置, 提供了虚拟网状联通性

2. 分支站点支持动态 IP 地址

3. 增加新的分支站点, 无需更改中心站点配置

4. 分支站点流量, 通过动态产生的站点间隧道进行封装

## DMVPN 的4大组成协议

1. 动态多点 GRE (Multipoint GRE, mGRE) 协议

2. 下一跳解析协议 (Next Hop Resolution Protocol, NHRP)

3. 动态路由协议

4. IPSec 技术

|原始数据|IP头部<br>源:站点X内部网络IP<br>目:站点Y内部网络IP|IP负载| | | | |
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|GRE 封装后|<br>源:站点X公网IP<br>目:站点Y公网IP|GRE|IP头部<br>源:站点X内部网络IP<br>目:站点Y内部网络IP|IP 负载|
|DMVPN 加密后<br>传输模式|IP头部<br>源:站点X公网IP<br>目:站点Y公网IP|ESP|GRE|IP 头部<br>源:站点X内部网络IP<br>目:站点Y内部网络IP|IP负载|

# 经典 DMVPN 实验

![](../image/IPSec/22062600.png)

## mGRE 配置

```
R1(config)#int tunnel 0
R1(config-if)#ip add 172.16.1.100 255.255.255.0
R1(config-if)#tunnel mode gre multipoint //配置为多点 GRE
R1(config-if)#tunnel source e0/0
R1(config-if)#tunnel key 12345 //隧道密钥用于标识隧道接口
```

### NHRP 配置

```
R1(config)#int tunnel 0
R1(config-if)#ip nhrp network-id 10 //激活 NHRP, 所有站点 network-id 建议相同
R1(config-if)#ip nhrp authentication cisco //(可选) 激活 NHRP 配置, 密码 cisco
R1(config-if)#ip nhrp map multicast dynamic //动态接收 NHRP 组播映射
```

#### 分支站点配置

```
---mGRE---

R2(config)#int tunnel 0
R2(config-if)#tunnel mode gre multipoint
R2(config-if)#tunnel source e0/0
R2(config-if)#tunnel key 12345

--- NHRP---

R2(config-if)#ip nhrp network-id 10
R2(config-if)#ip nhrp authentication cisco
R2(config-if)#ip nhrp map 172.16.1.100 202.100.1.100
//手动映射中心站点的隧道虚拟 IP 到中心站点的公网 IP. 有了这个映射, 分支站点才能访问中心站点
R2(config-if)#ip nhrp map multicast 202.100.1.100
//mGRE 是 NBMA 网络, 分支站点要和中心站点建立动态路由协议的邻居关系, 必须在每一个分支站点, 映射组播到中心站点的公网 IP, 这样才能够把分支站点的组播送到中心站点. 并且可以看到分支站点间没有组播映射, 所以分支站点间没有动态路由协议的邻居关系
R2(config-if)#ip nhrp nhs 172.16.1.100
NHS 就是 NHRP 服务器, 这个配置定义了 NHRP 服务器地址为中心站点的隧道接口虚拟地址
```

## 测试 NHRP

```
R1#show ip nhrp

172.16.1.1/32 via 172.16.1.1
   Tunnel0 created 00:08:13, expire 00:08:26
   Type: dynamic, Flags: registered nhop
   //由于注册动态(dynamic)获取的映射信息
   NBMA address: 202.100.2.1
   映射 R2 的虚拟 IP 地址到公网 IP
172.16.1.2/32 via 172.16.1.2
   Tunnel0 created 00:00:38, expire 00:09:21
   Type: dynamic, Flags: registered nhop
   NBMA address: 202.100.3.1
   //同样 R3 的虚拟 IP 到公网 IP
```

```
R2#show ip nhrp

172.16.1.100/32 via 172.16.1.100
   Tunnel0 created 00:11:10, never expire
   Type: static, Flags:
   //静态(static) NHRP 映射
   NBMA address: 202.100.1.100
   // 中心站点的虚拟 IP 到公网 IP
```
165