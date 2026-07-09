# Learning Objectives

完成本节后，你将能够：

- 在多个 Cisco IOSv 上批量执行 Show Commands

- 理解 Show Collection 的工程意义

- 将 Inventory、Loop 与 Netmiko 完整结合

- 学会让同一套程序自动采集整个网络的运行状态

- 建立企业自动化中最常见的"数据采集（Data Collection）"能力

本节仍然只执行 Show Commands，不修改设备配置。

先建立可靠的数据采集能力，再进行配置变更。这也是企业自动化中常见的实践

目前程序已经能够 Connect ➡ Disconnect 但是真正的网络自动化目的不是登录设备。

而是获取设备信息。例如网络管理员每天都会执行：

- show version

- show ip interface brief

- show ip route

- show inventory

- show clock

如果网络拥有300台设备, 人工登录 SSH ➡ show version ➡ 退出 ➡ SSH 下一台, 几乎不可维护。

因此企业自动化的第一类任务通常就是：

> Bulk Show Collection（批量状态采集）

目前程序流程：Inventory ➡ Loop ➡ Connect ➡ Disconnect

现在只需要在中间增加一步：Inventory ➡ Loop ➡ Connect ➡ **Show Command** ➡ Disconnect

整个模型几乎没有变化。只是每台设备多执行一个动作。这说明**前几节建立的数据驱动模型已经具有可扩展性**。

## 为什么企业自动化通常先做 Show？

原因很简单, 任何配置变更之前，首先需要知道设备当前状态。

例如升级前：show version 确认 IOS Version。

配置接口前：`show ip interface brief` 确认接口是否存在。

排查路由：`show ip route` 确认路由是否正确。

因此 Observe 永远先于 Configure。

这正是 Workbook 一直强调的实验流程：

Observe ➡ Verify ➡ Analyze ➡ Configure ➡ Verify Again

Show Collection 本质上就是 Observe。

## Cisco Implementation

本节仍然使用 Chapter 4 的 `connect_device()` 建立连接。连接成功后

调用 `connection.send_command()` 获取设备状态。

然后立即 `disconnect_device()`

释放 SSH Session。

整个流程：

Device ➡ Connect ➡ Collect ➡ Disconnect

## Verify

修改：

main5.5.py

```python
from inventory.devices import devices
from modules.connection import connect_device
from modules.connection import disconnect_device

for device in devices:

    print("=" * 60)
    print(f"Connecting to {device['host']}")

    connection = connect_device(device)

    output = connection.send_command("show version")

    print(output)

    disconnect_device(connection)
```
注意：

这里只新增了一行：

`output = connection.send_command("show version")`

整个程序结构几乎没有变化。

## Configure

本实验不修改设备配置。仅采集 `show version` 输出。

## Verify Again

验证所有设备是否都输出 `Cisco IOS Software` 以及 `Version` 等信息。

如果四台设备均输出成功。说明程序已经能够批量采集整个实验网络状态。

# Troubleshooting

### 问题一：第一台成功，第二台失败。

不要立即修改代码。先验证 `ssh admin@R2` 是否可以正常登录。

如果 SSH 本身失败。说明问题属于实验环境。不是 Python。

### 问题二：ReadTimeout

通常说明设备响应较慢。先观察 CPU 接口状态 Console 而不是立即增加 Timeout。

### 问题三：某一台设备失败后，整个程序停止。

这是目前代码的一个工程缺陷。因为目前异常会直接退出整个 for 循环。

## Engineering Notes

这一节虽然只增加了一行：

`output = connection.send_command("show version")`

但整个程序已经完成了从"连接设备"到"采集网络状态"的能力升级。

在真实企业环境中，绝大多数自动化项目都是从批量数据采集开始，而不是从批量配置下发开始。原因很简单：

- 数据采集风险低。

- 可以验证自动化程序是否稳定。

- 可以为后续配置变更提供可靠依据。

因此，在企业实践中，一个成熟团队通常会先完成"观察网络"的自动化，再逐步扩展到"修改网络"的自动化。