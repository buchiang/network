# Learning Objectives

完成本节后，你将能够：

- 理解什么是 Data-Driven Thinking（数据驱动思想）

- 理解为什么企业网络自动化不能按照"一台设备写一个脚本"的方式开发

- 理解**数据（Data）与逻辑（Logic）**分离的重要性

- 理解 Device Inventory 在整个自动化系统中的定位

- 建立企业网络自动化最重要的工程思维：代码处理数据，而不是代码描述设备

### Problem

假设你的实验室只有一台 Cisco IOSv 你已经完成了前几章的代码：

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.100.11",
    "username": "admin",
    "password": "cisco123",
    "secret": "cisco123"
}

connection = ConnectHandler(**device)
connection.enable()

output = connection.send_command("show version")

print(output)

connection.disconnect()
```

对于一台设备，这段代码完全没有问题, 但是现在实验室扩大了。

你的 EVE-NG 环境变成了：

```

            +----------------+
            | Automation Host|
            +--------+-------+
                     |
        -----------------------------
        |      |      |      |      |
      IOSv1  IOSv2  IOSv3  IOSv4  IOSv5
```

如果要求在五台设备上执行 show version。很多初学者的第一反应是继续复制代码。

例如：

```python
device1 = {...}
device2 = {...}
device3 = {...}
device4 = {...}
device5 = {...}
```

然后：

```python 
connection1 = ConnectHandler(**device1)
...
connection2 = ConnectHandler(**device2)
...
connection3 = ConnectHandler(**device3)
...
```
代码会越来越长, 如果增加到 200 台设备：

```
device1
device2
...
device200
```

问题开始暴露。

## 什么是真正的数据？

先观察下面两个例子。

### 方案一：设备写进程序

Python Script ➡ Router A ➡ Router B ➡ Router C

程序本身知道：Router A, Router B, Router C

也就是说设备信息已经"写死（Hard Code）"在程序里面。程序与设备紧密耦合, 任何设备变化，都需要修改程序。

### 方案二：程序处理数据

Python Script ➡ Device Inventory（数据） ➡ Router A ➡ Router B ➡ Router C

程序不知道 Router A, Router B, Router C

程序只知道"请把 Inventory 里面的每一台设备都处理一遍。"

**这就是 Data-Driven。**

程序处理的是：数据。

不是：某一台具体设备。

## 什么叫 Data-Driven？

Data-Driven 可以用一句话概括 - 程序只负责处理规则，数据负责描述对象。

例如程序负责：

登录设备 ➡ 进入 Enable ➡ 执行 Show ➡ 打印结果 ➡ 退出连接

数据负责：设备A, 设备B, 设备C

两者职责不同。

## 为什么企业网络必须采用 Data-Driven？

先思考一个真实场景, 一家企业拥有总部40台设备, 分公司120台设备, 数据中心80台设备

总计240台网络设备

如果每台设备都写：

```python
device1 = {}
device2 = {}
device3 = {}
```

工程会变成 Script ≈ Inventory

脚本越来越像数据库, 这不是 Automation。而是把所有数据都塞进代码。

真正的企业自动化应该是：**Automation Code + Device Data** 二者完全独立。

因此增加设备-修改数据。不是修改代码。

### 一个现实世界的类比

假设你是快递员。错误的方法今天送：张三, 李四, 王五 全部写进你的工作流程。

明天新增一个客户, 你必须重新修改工作流程。显然不可维护。

正确的方法工作流程永远只有：

拿到客户名单 ➡ 逐个配送

今天名单有：3 人。

明天名单有：300 人。

你的工作流程完全不用改。只需要客户名单改变。网络自动化也是完全相同的思想。

## Cisco Implementation

在企业网络中，一个自动化系统通常包含两部分。

### 第一部分：Automation Logic 负责：

SSH 登录 ➡ 执行命令 ➡ 发送配置 ➡ 保存配置 ➡ 记录日志

### 第二部分：Device Inventory 负责：

设备名称, IP 地址, 用户名, 密码, Enable Password

两部分彼此独立。

Automation Logic 不应该关心 "今天有多少台设备？" 它只负责： "把收到的每台设备都完成自动化任务。"

因此，一个典型的企业自动化流程可以表示为：
```

                Device Inventory
                       │
                       ▼
              Automation Program
                       │
                       ▼
              Connect to Device
                       │
                       ▼
               Execute Task
                       │
                       ▼
                Collect Result
                       │
                       ▼
                    Logging
```

请注意，在这一流程中，程序始终围绕"设备数据"运行，而不是围绕某一台固定设备编写。

## Lab Topology

![](<../Chapter 2 — Python Foundations for Network Engineers/Image/c2.9-0.png>)

# Troubleshooting

### 问题一：为什么不能复制 device 变量很多次？

可以做到, 但随着设备数量增加：

- 代码重复

- 修改困难

- 容易遗漏

- 可读性下降

这种方式在实验中或许可行，但不符合企业工程实践。

### 问题二：是不是必须学习新的 Python 语法？

不是。

Chapter 5 的目标之一，就是证明：

仅利用 Chapter 2 已学习的 Python 基础（尤其是列表和字典），就能够构建一个可扩展的多设备自动化程序。

因此，本章不会引入新的 Python 语言特性，而是提升已有知识的工程应用能力。

## Engineering Notes

本节最重要的内容不是代码，而是思维方式的转变。

请牢记下面四条工程原则：

1. 程序负责处理流程（Logic）。

2. 数据负责描述设备（Data）。

3. 增加设备时，应优先修改数据，而不是修改程序。

一个优秀的自动化程序，应能够在设备数量变化时保持代码基本不变。

这也是后续所有网络自动化框架共同遵循的核心思想。