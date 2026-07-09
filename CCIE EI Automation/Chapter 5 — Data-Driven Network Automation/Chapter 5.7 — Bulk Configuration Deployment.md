# Learning Objectives

完成本节后，你将能够：

- 理解批量配置（Bulk Configuration Deployment）的工程意义

- 使用同一套程序向多台 Cisco IOSv 下发配置

- 理解为什么配置部署比 Show Collection 风险更高

- 在已有的 Inventory 和 Fault Isolation 基础上实现安全的批量配置

- 建立"先验证、后部署、再验证"的工程习惯

企业自动化真正的价值不仅仅是观察网络，还包括：

- 批量修改 Banner

- 批量创建 Loopback

- 批量修改 Description

- 批量部署 AAA

- 批量更新 NTP

这就进入了 Configuration Deployment（配置部署）与 Show Collection 不同，配置部署会改变设备状态，因此必须更加谨慎。

### Data Collection vs Configuration Deployment

虽然两者都建立在同一个 Data-Driven Workflow 上，但目标完全不同。

#### Data Collection

Connect ➡ Read Device State ➡ Disconnect

特点：

- 只读取

- 不修改设备

- 风险低

#### Configuration Deployment

Connect ➡ Modify Configuration ➡ Verify ➡ Disconnect

特点：

- 修改设备

- 可能影响业务

- 必须验证结果

因此：配置部署必须比状态采集更加严格。

## 企业中，一个配置错误可能影响整个网络。

例如假设需要修改 Banner 如果200台设备全部失败。影响范围200 Devices

因此配置自动化遵循一个基本原则, **先验证，再修改；修改完成后，再验证**。

这也是本 Workbook 一直坚持的实验流程：

Observe ➡ Verify ➡ Analyze ➡ Configure ➡ Verify Again

## Cisco Implementation

本节仍然沿用：Inventory ➡ or device in devices

唯一变化是原来的 `connection.send_command()`

变成：`connection.send_config_set()`

整体 Workflow 没有变化。这说明 Data-Driven 的设计具有很好的可扩展性。

## EVE-NG Lab

### Lab Objective

为所有 Cisco IOSv创建：

```
interface Loopback100
 description Configured by Automation
Observe
```

在任何修改之前，先执行：

`show running-config | section interface Loopback100`

确认：Loopback100 不存在, 记录观察结果。

### Verify

准备配置：

```python
commands = [
    "interface Loopback100",
    "description Configured by Automation",
]
``` 

这里 `commands` 表示一个配置事务（Configuration Transaction）。整个列表将一次性发送给设备。

### Analyze

观察所有设备是否使用完全相同的配置？

目前答案：是。

因为：我们还没有学习 Jinja2。

因此所有设备部署同一份配置。

### Configure

[main 5.7.py](<LAB/main 5.7.py>)

[operation 5.7.py](<LAB/operation 5.7.py>)

在成功建立连接后：

```python
output = connection.send_config_set(commands)

print(output)
```

程序整体流程：

Inventory ➡ Loop ➡ Connect ➡ Deploy Configuration ➡ Disconnect

上一节已经加入了 Per-Device Error Handling。保持每台设备独立处理异常, 不要删除。

### Verify Again

配置完成后, 再次确认：

```
R1#show running-config | section interface Loopback100
interface Loopback100
 description Configured by Automation
 no ip address
```

如果其中 R2 失败。其它设备仍应完成配置。

# Troubleshooting

### 问题一

只有部分设备配置成功。先确认是否所有设备都进入 Enable Mode。Chapter 3 中 `connect_device()` 应负责完成 Enable。

### 问题二

配置没有生效, 不要立即修改程序。先手工验证：`show running-config`

确认配置是否真正进入 Running Configuration。

如果没有再分析连接、权限、设备状态。

### 问题三

为什么这里不用不同设备不同配置？

因为目前 Inventory 还没有配置数据。Chapter 5 只管理设备信息。

真正做到：

R1 ➡ Hostname R1


R2 ➡ Hostname R2

将在 Chapter 6 External Data 和 Chapter 7 Template-Based Configuration 逐步完成。

## Engineering Notes

本节引入了一个新的工程概念 Configuration Transaction（配置事务）

这里：

```python
commands = [
    "interface Loopback100",
    "description Configured by Automation",
]
```

不是简单的字符串列表。它表示一次完整、相关的配置操作。随着课程推进，一个配置事务可能包含：

- VLAN

- Interface

- OSPF

- ACL

等多个命令。但工程思想保持不变将相关配置作为一个整体进行部署。