
![](image.png)

在此拓扑中模拟了一个生产环境, R1 与 R2 的 e0/1 均为 `ip nat inside` e0/0 均为 `ip nat outside`

`access list 1 permit 192.168.1.0 0.0.0.255`

`access list 1 permit 192.168.2.0 0.0.0.255`

`ip nat inside source list 1 interface e0/0 overload`

因为在 R1 与 R3 配置了 NAT, 这个时候如果设置了 IPSec 的感兴趣流是 192.168.1.0 - 192.168.2.0 就会失效, 因为在 CISCO 设备的逻辑中, NAT 的优先级是高于 IPSec 的

这个时候就需要一个技术 **NAT 排除**

# NAT 排除

