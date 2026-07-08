# Learning Objectives

完成本节后，你将能够：

- 将 Device Inventory 与 Netmiko 结合

- 使用同一套代码依次连接多个 Cisco IOSv

- 理解多设备自动化程序的完整执行流程

- 学会将已有工程模块组合成一个完整的自动化任务

- 为后续批量执行 Show Commands 做准备

本节不会编写新的 SSH 登录代码。我们将直接复用：

- Chapter 3 的 Netmiko 登录能力

- Chapter 4 的工程化函数设计

- Chapter 5 的 Device Inventory

这是 Chapter 4 强调的 Code Reuse（代码复用） 的第一次实际应用。

## 为什么不是同时连接所有设备？

因为目前我们还没有学习：

- 多线程

- asyncio

- Connection Pool

本章采用 Sequential Processing（顺序处理）

即：Connect ➡ Execute ➡ Disconnect ➡ Next Device

这样有几个优点：

- 容易理解

- 容易调试

- 占用资源少

- 出现故障容易定位

这是企业自动化最常见的第一阶段实现方式, 在建立正确工程模型之前，不应过早引入并发技术。

## Cisco Implementation

结合前面章节，我们已经拥有：

Inventory ➡ devices ➡ `for device in devices:` ➡ `connect_device(device)` ➡ `disconnect_device(connection)`

请注意这里并没有重新编写 `ConnectHandler()`

因为 Chapter 4 已经封装好了 `connect_device()` 这就是工程化设计最大的优势。

# Troubleshooting

### 问题一：程序在第二台设备停止。

例如：

```
Connecting R1
Success

Connecting R2
Failed...
```

先不要立即修改代码。按照 Workbook 的实验流程：

Observe ➡ Analyze ➡ Find Root Cause

首先确认 R2 是否能够手工 SSH 登录？

如果 Linux ssh admin@12.1.1.2 都无法连接。那么问题不是 Python。而是设备连通性。

### 问题二：某一台设备认证失败。

例如：Authentication failed.

先检查 Inventory 中 password secret 是否正确。不要首先怀疑 Netmiko。

### 问题三 为什么没有 try 包住整个 for

因为：这样会导致一台设备失败, 整个 Inventory 停止。

企业自动化通常希望：

R1

Success

↓

R2

Failed

↓

Continue

↓

R3

Success

因此，更合理的工程实践是每台设备独立处理异常。

Revision Note

> 这里先建立设计思想，不立即修改代码。

> 下一节在批量执行 Show Commands 时，我们会将异常处理放到每台设备的处理流程中，而不是整个循环外层。这样既符合 Chapter 4 的异常处理原则，也能保证一台设备失败不会影响其它设备。

## Engineering Notes

这一节标志着整个 Workbook 的一个重要里程碑。

Chapter 3：

One Program ➡ One Device

---

Chapter 5：

One Program ➡ Many Devices

程序本身几乎没有增加复杂度。

真正发生变化的是：

Data ➡ Inventory ➡ Loop

这也是企业自动化项目能够管理数百台甚至数千台设备的根本原因。

请牢记下面这个工程公式：

Automation Capability = Automation Logic + Device Inventory

而不是 Automation Capability = 更多的 Python 代码

优秀的自动化系统通常不是依靠不断复制代码来扩展，而是依靠更好的数据组织方式。

