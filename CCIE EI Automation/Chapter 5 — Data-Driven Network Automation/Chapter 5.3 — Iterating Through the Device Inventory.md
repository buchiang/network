# Learning Objectives

完成本节后，你将能够：

- 理解为什么自动化程序必须遍历（Iterate）Device Inventory

- 使用 Chapter 2 已学习的 `for` 循环处理多个设备

- 理解**数据驱动（Data-Driven）如何与循环（Loop）**结合

- 验证 Device Inventory 是否能够被程序正确访问

- 为下一节连接多台设备做好准备

本节仍然不使用 Netmiko, 我们只验证程序是否能够正确处理 Device Inventory。

目前，我们已经有了 Device Inventory。

```python
devices = [
    {...},
    {...},
    {...},
]
```
但是，这只是一个数据集合。

程序如何知道：

- 第一台设备是谁？

- 第二台设备是谁？

- 第三台设备是谁？

如果程序不能逐个读取这些数据，那么 Inventory 就没有任何意义。

### 什么叫 Iterate？

Iterate（遍历）表示：按照一定顺序，依次处理集合中的每一个元素。

```python
for device in devices:
```

意思就是请把 Inventory 中的每一台设备，一个接一个交给变量 `device`。

### 数据是如何流动的？

假设：

devices = [
    {"host": "192.168.100.11"},
    {"host": "192.168.100.12"},
    {"host": "192.168.100.13"},
]

程序执行：`for device in devices:`

第一次循环：

device ➡ {"host":"192.168.100.11"}

第二次循环：

device ➡ {"host":"192.168.100.12"}

第三次循环：

device ➡ {"host":"192.168.100.13"}

请注意：

程序完全不知道今天有几台设备, 它只知道 **Inventory 里面还有没有下一台**。这就是 Data-Driven 的真正体现。

## 为什么变量名使用 `device`？

请观察 `devices` 表示整个设备集合。而 `device` 表示当前正在处理的一台设备。

因此 `for device in devices:`

读起来就是 For each device in devices.

这是 Python 社区以及网络自动化项目中最常见、最容易理解的命名方式。

## 为什么不能使用索引？

例如：

```python
devices[0]
devices[1]
devices[2]
```

技术上可以, 但是：

如果以后增加设备：

```python
devices[3]
devices[4]
devices[5]
```

程序又需要修改, 而 `for device in devices:`

无论 Inventory 有3台还是300台, 程序完全一样。

因此企业工程几乎都会使用直接遍历集合。而不是手工访问索引。

## Cisco Implementation

企业自动化程序每天都在执行类似工作。

例如：

读取 Inventory ➡ 第一台设备 ➡ 执行任务 ➡ 第二台设备 ➡ 执行任务 ➡ 第三台设备 ➡ 执行任务 ➡ …… ➡ 最后一台设备

程序根本不需要知道总共有多少设备。Inventory 自己决定, Automation Logic 永远保持一致。

## Verify

在项目根目录创建测试文件 test_inventory.py

写入：

```python
from inventory.devices import devices

for device in devices:
    print(device)
```
运行 python3 test_inventory.py

预期输出：

```bash
{'device_type': 'cisco_ios', ...}
{'device_type': 'cisco_ios', ...}
{'device_type': 'cisco_ios', ...}
```

## Analyze

继续修改：

```python
from inventory.devices import devices

for device in devices:
    print(device["host"])
```

再次运行 python3 test_inventory.py

预期输出：

```bash
12.1.1.1
12.1.1.2
23.1.1.3
```
分析整个程序没有写：device1 device2 device3 程序只认识 device

每次循环 device 都会自动变成下一台设备。

## Configure

继续增加输出：

```python
from inventory.devices import devices

for device in devices:
    print("Current Device:")
    print(device["host"])
    print("-" * 30)
```

运行结果类似：

```bash
Current Device:
12.1.1.1
------------------------------

Current Device:
12.1.1.2
------------------------------

Current Device:
23.1.1.3
------------------------------
```

这里虽然只是打印，但是程序已经完成了逐台处理设备。只是目前处理动作还是 Print 下一节将变成：

- SSH Login

- Verify Again

再次回答下面几个问题程序里面是否出现 device1

答案：没有。

程序里面是否出现：device2

答案：没有。

程序为什么还能处理四台设备？

因为程序处理的是 devices 而不是某一个固定变量。

# Troubleshooting

### 问题一：出现 ModuleNotFoundError

通常原因：项目目录不正确。

确认：

```
automation/

├── inventory/
│   ├── __init__.py
│   └── devices.py
│
└── test_inventory.py
```

如果 inventory 目录缺少：__init__.py 在某些环境下可能无法作为 Python 包导入。

从 Python 3.3 开始，支持 Implicit Namespace Packages，理论上没有 __init__.py 也可以导入。但为了保持企业项目结构清晰，并兼容更多开发工具和静态分析器，本 Workbook 统一保留 __init__.py。

### 问题二：出现 KeyError: 'host'

说明某个 Dictionary 没有 "host" 字段。检查 Inventory 中所有 Dictionary 是否保持一致。

例如不要混用 "ip" 和 "host" 整个 Workbook 统一使用 host

### 问题三：为什么不用 for i in range(len(devices)):

Chapter 2 我们已经学习过这种写法, 但这里并不需要索引。

因为我们真正需要的是设备对象本身。

因此 `for device in devices:` 更加符合：

- Python 风格

- 可读性

- 企业最佳实践

只有在确实需要索引（例如比较前后元素、记录位置编号等）时，才考虑使用索引方式。

## Engineering Notes

本节虽然只使用了一个简单的 for 循环，但它代表着企业自动化最核心的执行模型：

```
Inventory
      │
      ▼
for device in devices
      │
      ▼
Process Current Device
      │
      ▼
Next Device
      │
      ▼
Until Inventory Ends
```

从这一刻开始，程序已经具备了**水平扩展（Horizontal Scaling）**的基础。

请注意：

这里的"扩展"指的是同一套程序能够处理更多设备。

并不是：

- 多线程

- 多进程

- asyncio

这些并发技术将在后续章节讨论，本章坚持单线程、顺序处理，先建立正确的工程模型。