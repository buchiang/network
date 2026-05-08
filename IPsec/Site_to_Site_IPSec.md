
![](../image/IPSec/07052600.png)

对于 Site to Site 最重要的一个问题是路由, VPC6 要访问 VPC8, 但是 R1 只有直连 SW 方向和 R2, 不知道 VPC8 在哪

通信点是 VPC 加密点是 R1 和 R3

加密点需要路由:

1. 远端通信点

2. 远端解密点

