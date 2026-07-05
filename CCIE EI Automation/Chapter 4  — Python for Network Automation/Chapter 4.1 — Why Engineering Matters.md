# Learning Objectives

完成本节后，应能够回答以下问题：

- 为什么能够运行（Working）并不等于工程化（Engineering）。

- 为什么企业网络自动化越来越强调代码质量，而不仅仅是功能实现。

- 什么是可维护性（Maintainability）。

- 什么是可扩展性（Scalability）。

- 什么是代码复用（Code Reuse）。

- 为什么要将网络自动化脚本设计成一个个可复用的能力（Capability）。

- 为什么 Chapter 4 的第一课不是写代码，而是先理解工程思想。

假设现在有一个实验需求。需要登录一台 Cisco IOSv，执行三条命令：

```
show version
show ip interface brief
show ip route
```

在 Chapter 3 中，我们完全可以写出这样的程序：

```
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "10.10.10.1",
    "username": "admin",
    "password": "cisco123",
    "secret": "cisco123",
}

connection = ConnectHandler(**device)

connection.enable()

print(connection.send_command("show version"))
print(connection.send_command("show ip interface brief"))
print(connection.send_command("show ip route"))

connection.disconnect()
```

它可以运行, 实验也能成功。那么问题来了它是不是一个好的企业脚本？

答案是不是。原因并不是它运行失败，而是它无法很好地应对真实企业环境中的变化。

在网络自动化领域，有一个很重要的概念 Working Code ≠ Engineering Code 可以翻译为能够运行的代码，不一定是工程代码。很多刚开始学习 Python 的工程师都会有一种误解 "程序能跑起来就可以了。" 对于实验来说，这没有问题。但企业关注的不仅是今天能运行，还包括：

- 三个月后还能维护吗？

- 同事接手后能理解吗？

- 增加新需求是否容易？

- 出现故障时能快速定位吗？

因此，企业更加关注的是代码生命周期（Code Lifecycle）。

一个脚本的生命周期通常包括：

编写 ➡ 测试 ➡ 上线 ➡ 维护 ➡ 修改 ➡ 再次维护 ➡ 持续演进

真正耗费时间的，往往不是第一次写代码，而是后续不断地维护和修改。

## 场景一：需求增加

最初，只需要执行三条 show 命令。几周后，新的需求来了：

登录设备 ➡ 进入 Enable ➡ 执行 10 条 Show 命令 ➡ 保存输出 ➡ 退出

脚本会越来越长, 如果所有逻辑都堆在一起，每增加一个需求，都要修改多个地方。维护成本迅速增加。

## 场景二：设备数量增加

实验环境1台 Router. 企业环境120台 Router, 85台 Switch, 30台 Firewall 如果每台设备都复制一遍登录代码

```
ConnectHandler(...)
ConnectHandler(...)
ConnectHandler(...)
```

那么一旦密码修改。需要改多少地方？可能几十处。这就是重复代码（Duplicate Code）带来的问题。

## 场景三：人员交接

很多自动化脚本不是一直由同一个人维护。

例如 2026 张工开发。2027 李工维护。2028 王工继续开发。

如果代码组织混乱：

- 没有函数

- 没有日志

- 没有统一命名

- 没有明确结构

新的维护人员需要花费大量时间理解脚本。工程效率会明显下降。

## Cisco Implementation

虽然 Cisco IOS 本身并不关心 Python 代码如何组织，但 Cisco 在官方自动化实践中一直强调自动化脚本应具有可维护性、可重复使用性和可扩展性。例如，一个典型的网络自动化流程可以表示为

```
准备设备信息
⬇
建立连接
⬇
进入特权模式
⬇
执行命令
⬇
处理输出
⬇
关闭连接
```

这个流程本身就具有清晰的阶段划分。因此，在 Python 中，也应该将这些阶段设计为独立的能力，而不是全部写在一个连续的脚本中。这也是后续进行函数封装和模块化设计的基础。

# Troubleshooting

- 问题一：脚本可以运行，为什么还要修改？

因为工程目标不仅是今天能运行，还包括未来能维护、能扩展。

- 问题二：实验环境只有一台 Router，还需要考虑这些吗？

需要。工程设计应在规模较小时建立，而不是等脚本复杂后再整体重构。

- 问题三：是不是所有短脚本都必须重构？

不是。

是否需要重构取决于：

- 是否会重复使用。

- 是否预计持续维护。

- 是否需要扩展功能。

一次性的小工具通常不需要复杂的工程结构；长期维护的自动化项目则应尽早采用工程化设计。

## Engineering Notes

本节引入本书一个非常重要的理念：

Capability First（能力优先）

在后续章节中，我们不再把脚本看作一串连续执行的语句，而是把它看作由多个可以独立理解、独立维护、独立复用的能力组成。

例如：

建立连接

进入 Enable

执行命令

执行配置

保存配置

关闭连接

这些都是独立的能力。

Chapter 4 的核心，就是学习如何用 Python 将这些能力组织成一个具有工程质量的自动化程序。