# Learning Objectives

完成本节后，你将能够：

- 理解什么是 Device Inventory

- 理解为什么 Device Inventory 是网络自动化的基础

- 使用 Python List 和 Dictionary 构建企业级设备清单

- 理解为什么企业使用"设备集合"而不是"多个独立变量"

- 为后续多设备自动化建立统一的数据组织方式

**本节只学习如何组织设备数据，不进行设备连接。**

### 什么是 Device Inventory？

在企业网络中，Inventory（清单）表示自动化程序所管理的全部网络设备信息。

请注意 Inventory 不是配置文件。Inventory 也不是程序逻辑。

它只是-**一组描述网络设备的数据。**

例如：

```
Inventory

├── R1
├── R2
├── R3
└── R4
```

程序以后所有工作都围绕这个 Inventory 展开。

### 多个设备

```python
devices = [
    {...},
    {...},
    {...},
    {...},
]
```

这里出现了一个重要关系：

```
List
    │
    ├── Dictionary（R1）
    ├── Dictionary（R2）
    ├── Dictionary（R3）
    └── Dictionary（R4）
```

也就是说：

- 一个 Dictionary = 一台设备

- 一个 List = 整个 Device Inventory

这是后续整本 Workbook 都将采用的数据组织方式。

### Inventory 的职责

请牢记下面：

```
Inventory
    ↓
告诉程序有哪些设备？
```

程序：

```
Automation Logic
    ↓
告诉设备：应该做什么？
```

两者职责不同。不要混合。

## Cisco Implementation

企业中，无论设备数量是多少，Inventory 的作用都保持一致。



Automation Program：

读取 Inventory ➡ 逐台处理设备 ➡ 完成自动化任务

因此：

Inventory 的大小可以变化。

Automation Logic 不需要变化。

## LAB 

在 `automation/inventory/` 目录中新建：

devices.py

写入：

```python
devices = [
    {
        "device_type": "cisco_ios",
        "host": "12.1.1.1",
        "username": "admin",
        "password": "cisco123",
        "secret": "cisco123",
    },
    {
        "device_type": "cisco_ios",
        "host": "12.1.1.2",
        "username": "admin",
        "password": "cisco123",
        "secret": "cisco123",
    },
    {
        "device_type": "cisco_ios",
        "host": "23.1.1.3",
        "username": "admin",
        "password": "cisco123",
        "secret": "cisco123",
    },
]
```

注意变量名称统一使用 *devices* 而不是 *router_list*, *device_list*, *inventory*, *my_devices* 这样可以保持整本 Workbook 的命名一致性。

## Verify

进入 Python 解释器 python3

测试：
```python
from inventory.devices import devices

print(devices)
```
应看到：
```python 
[
    {...},
    {...},
    {...}
]
```
再验证：`print(len(devices))` 输出：`2`

说明 Inventory 已成功建立。

# Troubleshooting

### 问题一：可以使用 Tuple 吗？

技术上可以, 但不推荐。

原因 Inventory 会不断变化：

- 新增设备

- 删除设备

- 替换设备

List 更符合企业维护需求。

### 问题二：为什么不用 Set？

Set 不适合, 因为：

- 不保证顺序

- 自动去重

- 不能很好地表示结构化设备对象

网络设备通常需要保持完整的结构信息，因此 Dictionary + List 更合适。

### 问题三：为什么不用多个独立变量？

例如：

```python
device1
device2
device3
``` 

因为程序无法方便地"批量处理"这些变量, 而 List 天然支持遍历, 这正是下一节课将要利用的能力。

## Engineering Notes

从本节开始，整个 Workbook 统一采用以下数据组织原则：

```
Device Inventory（List）
        │
        ├── Device（Dictionary）
        ├── Device（Dictionary）
        ├── Device（Dictionary）
        └── ...
```

请特别注意一个工程习惯 devices.py 只负责存放设备数据，不负责执行任何自动化逻辑。

不要在这个文件中：

- 导入 Netmiko

- 建立 SSH 连接

- 执行 show 命令

- 下发配置

它的唯一职责就是维护设备清单。这与 Chapter 4 强调的 Single Responsibility Principle（单一职责原则） 完全一致。