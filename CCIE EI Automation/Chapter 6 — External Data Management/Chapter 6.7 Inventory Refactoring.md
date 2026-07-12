# Chapter Objective

经过前面的学习，我们已经掌握了：

- 为什么需要外部数据（6.1）

- YAML 基础（6.2）

- YAML Inventory（6.3）

- JSON 基础（6.4）

- Python 读取 JSON（6.5）

- YAML 与 JSON 的比较（6.6）

现在，需要完成本章最后一个工程目标：

>Refactor the automation project to use external inventory files.

这里的 Refactoring 并不是增加新的自动化功能，而是优化工程结构。整个自动化流程保持不变：

Connect ➡ Execute ➡ Disconnect

唯一改变的是：

>Inventory 不再来自 Python 代码，而是来自外部文件。

## The Original Project

Chapter 5 中，我们的程序通常是这样的：

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

for device in devices:

    connection = connect_device(device)

    execute_show_command(
        connection,
        "show version"
    )

    disconnect_device(connection)
```

可以发现程序里面同时包含：

- Automation Logic

- Device Inventory

职责并没有分离。

## Refactoring Goal

我们的目标是：

Automation Logic ➡ Read Inventory ➡ Execute Automation

程序不再关心：

- IP Address

- Username

- Password

程序唯一需要的是 devices 至于 devices 来自哪里，程序并不关心。这就是良好的软件设计。

## Refactoring with JSON

首先回顾 JSON 方案。

目录：

```
automation_project/

├── inventory/
│   └── devices.json
│
├── modules/
│
├── scripts/
│
└── main.py
```

读取：

```python
import json

with open("inventory/devices.json", "r") as file:
    devices = json.load(file)
```

之后：

```python
for device in devices:

    connection = connect_device(device)

    execute_show_command(
        connection,
        "show version"
    )

    disconnect_device(connection)
```

可以看到只有读取 Inventory 的代码发生变化, 自动化流程完全没有变化。

## Refactoring with YAML

接下来，我们完成 YAML 这条知识线。由于 YAML 不是 Python 标准库的一部分，因此需要安装第三方库。

在 Ubuntu 22.04 中执行：`pip install pyyaml`

安装完成后：

```python
import yaml #读取 YAML：

with open("inventory/devices.yaml", "r") as file:
    devices = yaml.safe_load(file)
```

完整程序：

```python
import yaml

from modules.connection import (
    connect_device,
    disconnect_device,
    execute_show_command
)

with open("inventory/devices.yaml", "r") as file:
    devices = yaml.safe_load(file)

for device in devices:

    connection = connect_device(device)

    execute_show_command(
        connection,
        "show version"
    )

    disconnect_device(connection)
```

这里唯一新增的是：`yaml.safe_load(file)` 它与 `json.load(file)` 作用完全类似。

>都是将外部数据转换为 Python 对象。

## JSON vs YAML in Python

比较两种读取方式：

JSON：

```python
import json

with open("inventory/devices.json", "r") as file:
    devices = json.load(file)
```

YAML：

```python
import yaml

with open("inventory/devices.yaml", "r") as file:
    devices = yaml.safe_load(file)
```

除了：

- 导入模块不同

- 调用函数不同

后面的自动化代码100%相同。

例如：`for device in devices:` 无需修改, 这说明 Python 程序真正依赖的是：

list ➡ dict

而不是 JSON 或者 YAML

## Data Format Independence

这也是本章最重要的工程思想。

自动化程序：

Automation ➡ Inventory ➡ Devices

Inventory 可以来自：`devices.json`

也可以来自：`devices.yaml`

只要最终得到：`devices`

程序完全无需修改。

因此真正重要的是统一的数据结构, 而不是统一的数据格式。

## Final Project Structure

完成 Refactoring 后，整个工程推荐采用以下目录：

```
automation_project/

├── inventory/
│   ├── devices.yaml
│   └── devices.json
│
├── modules/
│   └── connection.py
│
├── scripts/
│
├── backups/
│
├── logs/
│
└── main.py
```
其中：

- `devices.yaml`：推荐作为人工维护的 Inventory。

- `devices.json`：用于学习 JSON、测试或与其他程序交换数据。

实际项目中通常只维护一种格式，避免多个 Inventory 文件内容不一致。