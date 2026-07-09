# Learning Objectives

完成本节后，你将能够：

- 理解为什么企业自动化必须进行 Per-Device Error Handling（单设备异常处理）

- 理解 Fault Isolation（故障隔离） 在批量自动化中的作用

- 在多设备自动化中实现"一台设备失败，不影响其他设备"

- 区分 Python Exception 与企业自动化中的 Exception Strategy

- 建立可持续运行的批量自动化程序

在上一节已经完成了一个自动化, 程序可依次登陆所有设备并采集 `show version`, 但是在生产环境中一台设备因维护, 故障无法连接会发生什么?

### 什么是 Per-Device Error Handling？

Per-Device Error Handling 指：

>每一台设备独立处理异常，而不是整个自动化任务共用一个异常处理流程。

也就是说每一次循环 `for device in devices:` 都应该看作一次独立的自动化任务, 而不是整个 Inventory 是一个任务。

### Fault Isolation

Fault Isolation（故障隔离）是企业自动化的重要原则。目标不是避免所有错误, 而是限制错误的影响范围。

## 为什么企业必须这样设计？

假设企业拥有500台 Cisco IOS 如果其中5台设备因为维护而离线。自动化程序应该成功完成495台, 而不是因为5台失败, 导致500台全部失败。

因此企业自动化追求的是 Maximum Task Completion（最大任务完成率）而不是 Zero Failure（零失败）这是企业运维与实验室脚本最大的区别。

## Cisco Implementation

目前程序：

Inventory ➡ Loop ➡ Connect ➡ Show ➡ Disconnect

现在需要增加异常隔离：

Inventory ➡ Loop ➡ **Try** ➡ Connect ➡ **Collect** ➡ Disconnect ➡ **Except** ➡ **Log** ➡  Continue

请注意这里 `Try / Except` 并不是新的 Python 知识。Chapter 4 已经学习过 Exception Handling。

本节学习的是：Exception Strategy in Multi-Device Automation。

![](<../Chapter 2 — Python Foundations for Network Engineers/Image/c2.9-0.png>)

现在我把 R2 的 IP 更换为错误的 12.1.1.3

[main 5.5.py](<LAB/main 5.5.py>) 使用之前的 main 文件

```bash
Connecting to 12.1.1.3
Failed to connect device TCP connection to device failed.

Common causes of this problem are:
1. Incorrect hostname or IP address.
2. Wrong TCP port.
3. Intermediate firewall blocking access.

Device settings: cisco_ios 12.1.1.3:22


Traceback (most recent call last):
  File "/home/user/automation_project/automation/main.py", line 12, in <module>
    output = connection.send_command("show version")
AttributeError: 'NoneType' object has no attribute 'send_command'
```

因为一个错误, 整个循环崩溃了

```python
from inventory.devices import devices
from modules.connection import connect_device
from modules.connection import disconnect_device
from modules.operations import collect_show_version

for device in devices:

    print("=" * 60)
    print(f"Connecting to {device['host']}")

    try:
        connection = connect_device(device)

        output = collect_show_version(connection)

        print(output)

        disconnect_device(connection)

    except Exception as error:
        print(f"FAILED: {device['host']}")
        print(error)
```

try 放在每一次循环内部, 而不是整个 for 循环外这是本节最重要的设计。

运行 [main 5.6.py](<LAB/main 5.6.py>) 会发现即使 R2 失败了, 但是程序还会继续往下执行.

```bash
Connecting to 12.1.1.3
Failed to connect device TCP connection to device failed.

Common causes of this problem are:
1. Incorrect hostname or IP address.
2. Wrong TCP port.
3. Intermediate firewall blocking access.

Device settings: cisco_ios 12.1.1.3:22


'NoneType' object has no attribute 'send_command'
None
Failed to disconnect from device: 'NoneType' object has no attribute 'disconnect'
============================================================
Connecting to 23.1.1.3
Cisco IOS Software, Linux Software (I86BI_LINUX-ADVENTERPRISEK9-M), Version 15.7(3)M2, DEVELOPMENT TEST SOFTWARE
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2018 by Cisco Systems, Inc.
Compiled Wed 28-Mar-18 11:18 by prod_rel_team
```

说明 Fault Isolation 已经实现。

# Troubleshooting

### 问题一

为什么不能：

```python
try:

    for device in devices:

        ...

except:
```

因为这样整个 Inventory 只有一个异常处理。一旦 R2 失败整个循环结束。

不能达到 Per-Device Error Handling。

### 问题二

为什么这里只使用 except Exception

因为 Chapter 4 已经介绍了异常处理机制, 本章重点不是研究各种异常类型。

而是异常处理的位置（Placement）随着课程推进，

后续章节可以逐步细化：

- Authentication Failure

- Timeout

- SSH Failure

等不同异常。

### 问题三

程序结束后为什么还能看到错误？

因为自动化程序应该报告失败, 而不是隐藏失败. 隐藏异常会让故障排查更加困难。

## Engineering Notes

企业自动化通常不会要求 100% Success. 而是 100% Execution

例如：

100 Devices ➡ 96 Success ➡ 4 Failed ➡ Generate Report

这比：

Device 4 Failed ➡ Program Exit

更符合真实运维需求。

请牢记下面这条工程原则：

>自动化程序应尽可能完成所有可完成的任务，并准确报告无法完成的部分。

>这是构建可靠自动化系统的重要设计思想。