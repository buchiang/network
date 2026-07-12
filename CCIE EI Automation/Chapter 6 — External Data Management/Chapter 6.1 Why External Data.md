# Chapter Objective

在 Chapter 5 中，我们已经能够通过一个 Python Inventory 管理多台设备。

例如：

```python
devices = [
    {
        "host": "192.168.100.11",
        "username": "admin",
        "password": "Cisco123",
        "device_type": "cisco_ios"
    },
    {
        "host": "192.168.100.12",
        "username": "admin",
        "password": "Cisco123",
        "device_type": "cisco_ios"
    }
]
```

程序可以遍历整个 Inventory，并自动连接所有设备。对于实验环境，这已经足够, 但是在真实企业环境中，这种做法很快就会遇到工程问题。

本节将回答 Chapter 6 的核心问题：

>Why should automation data be separated from Python code?

## Code vs Data

首先，需要区分两个概念。

### Python Code

Python Code 描述的是程序应该做什么。

例如：

```python
for device in devices:
    connection = connect_device(device)
    execute_show_command(connection, "show version")
    disconnect_device(connection)
```

这里定义的是自动化流程：

- 遍历设备

- 建立连接

- 执行命令

- 断开连接

无论设备数量如何变化，这段代码通常都不需要修改。

### Automation Data

Automation Data 描述的是程序应该处理哪些对象。

例如：

```python
devices = [
    {
        "host": "10.1.1.1",
        "username": "admin"
    },
    {
        "host": "10.1.1.2",
        "username": "admin"
    }
]
```

这里描述的是：

- IP 地址

- 用户名

- 密码

- 平台类型

这些都属于数据，而不是程序逻辑。

#### 因此可以得到一个非常重要的工程原则：

>Code describes behavior. Data describes objects.

这也是后续所有自动化框架都会遵循的基本思想。

## The Problem with Hard-Coded Data

在 Chapter 5 中，我们一直采用这种方式：

```python
devices = [
    ...
]
```

这被称为：Hard-Coded Data（硬编码数据）

意思是：数据直接写在 Python 程序内部。

例如：

```python
commands = [
    "show version",
    "show ip interface brief",
    "show ip route"
]
```

或者：

```python
username = "admin"
password = "Cisco123"
```

这些值都固定写在代码中。

### 为什么硬编码会成为问题？

假设公司新增一台设备 R5, 你需要修改：

```python
devices = [
    ...
]
```

然后重新保存程序。如果公司每天新增几十台设备，那么程序将被频繁修改。

---

再例如公司要求所有设备密码修改为 Cisco456 如果密码写在多个 Python 文件中：

```
backup.py
deploy.py
audit.py
inventory.py
health_check.py
```

那么每个程序都需要修改。维护成本会迅速增加。

## A Small Example

假设现在有两个脚本：

backup.py

```python
devices = [
    {
        "host": "10.1.1.1",
        "password": "Cisco123"
    }
]
```

另一个：show_version.py

```python
devices = [
    {
        "host": "10.1.1.1",
        "password": "Cisco123"
    }
]
```

看起来没有问题。但是某一天密码修改了。

你必须同时修改：

```
backup.py
show_version.py
```
如果忘记修改其中一个脚本结果就是一个程序能够登录，另一个程序全部失败。这类问题在企业环境中非常常见。

## Separating Code from Data

更好的工程方式是 Python 只负责自动化逻辑。

例如：

```python

inventory = load_inventory()

for device in inventory:
    connection = connect_device(device)
    execute_show_command(connection, "show version")
    disconnect_device(connection)
```

程序完全不知道：

- IP 地址

- 用户名

- 密码

- 平台

它只知道：

读取 Inventory ➡ 遍历 Inventory ➡ 自动化

所有设备信息，都存放在独立的数据文件中。

例如 devices.yaml 或者 devices.json

以后如果设备发生变化只需要修改数据文件。Python 程序完全不需要修改。

## Benefits of External Data

将数据与代码分离后，可以带来许多工程优势。

| Benefit         | Description                       |
| --------------- | --------------------------------- |
| Reusability     | 同一个 Python 程序可以用于不同的数据集。          |
| Maintainability | 修改设备信息无需修改程序逻辑。                   |
| Scalability     | Inventory 从几台扩展到数千台时，程序结构保持不变。    |
| Readability     | 数据文件专门存放数据，代码更简洁、更容易理解。           |
| Collaboration   | 网络工程师可以维护 Inventory，而开发者专注于自动化逻辑。 |

这些优势并非只适用于网络自动化，而是软件工程中的通用设计原则。

## Engineering Analogy

可以用一个生活中的例子来理解这种设计。假设一家快递公司每天都需要打印发货标签。

打印程序负责：

- 打开打印机

- 设置纸张

- 打始打印

- 输出标签

它并不需要把所有客户地址写在程序中, 客户地址应该来自当天的订单数据。

如果今天新增了一位客户，只需更新订单，而无需修改打印程序。

网络自动化也是同样的思路：

- 自动化程序负责执行流程。

- **设备清单（Inventory）** 提供需要处理的对象。

程序读取数据，而不是保存数据。

## Engineering Best Practice

从本章开始，整个 Workbook 将遵循以下工程原则：

>Keep automation logic in Python, and keep automation data in external files.

这一原则将贯穿后续章节，也是企业自动化项目中最常见、最重要的设计方式之一。