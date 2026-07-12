# Learning Objectives

完成本节后，你将能够：

- 理解为什么企业自动化需要组织（Organize）Operational Tasks

- 将设备数据、命令数据和程序逻辑保持分离

- 建立统一的 Operational Task 组织方式

- 为后续 Chapter 6（External Data）做好工程准备

- 理解为什么良好的数据组织比增加代码更重要

>本节不会引入 YAML、JSON 或 Jinja2。

>我们仍然使用 Python List 和 Dictionary，只优化当前工程的数据组织方式。

之前已经讲过了 device 字典和 command list, 现在生产中需要每天执行

```
show version
show ip interface brief
show ip route
show inventory
show clock
show logging
show arp
show ip ospf neighbor
show cdp neighbors
...
```

Command Inventory 会越来越长, 如何让其保持清晰, 易维护?

## Operational Task

检查设备基本信息

```
show version
show inventory
show clock
```

归类于 Device Information Task

检查网络连通性：

```
show ip interface brief
show ip route
```

归类于 Network Status Task

### Why 

生产环境维护的是任务（Task）, 不是单独的一条命令。

例如每天上午 `Collect Device Status`

下午 `Verify Routing`

晚上 `Backup Configuration`

每一个都是一个 Operational Task。而不是几十条零散命令. 这种组织方式更容易维护，也更符合企业运维流程。

## Cisco Implementation

保持当前工程结构：

```
automation/

├── inventory/
│
├── modules/
│
├── logs/
│
└── main.py
```

在 main.py 中仍然定义：

```python
commands = [
    "show version",
    "show ip interface brief",
    "show ip route",
]
```

但增加注释：

```python
commands = [
    # Device Information
    "show version",

    # Interface Status
    "show ip interface brief",

    # Routing Information
    "show ip route",
]
```

请注意这是工程组织优化。不是 Python 技术变化。

# Troubleshooting

### 问题一 为什么这里只增加注释？

因为 Chapter 5 重点仍然是 Data Organization。不是 External Data。

真正的数据外部化将在 Chapter 6 完成。

### 问题二 为什么不建立 不同 Python 文件？

例如：device_commands.py, routing_commands.py

因为这会提前进入更复杂的数据管理。

目前 Command Inventory 规模仍然很小。没有必要增加工程复杂度。

遵循 Keep It Simple（KISS）

### 问题三 为什么不使用 YAML？

因为 YAML 属于 Chapter 6。

本章坚持 Python 基础数据结构。

## Engineering Notes

Chapter 5 已经建立了三个重要的数据对象：

Device Inventory ➡ Current Device ➡ Command Inventory

整个自动化程序始终围绕数据集合运行。

而不是围绕某一台设备、某一条命令运行。

这是 Data-Driven Network Automation 最重要的工程思想。