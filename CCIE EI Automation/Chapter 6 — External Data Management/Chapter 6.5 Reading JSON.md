# Chapter Objective

上一节，我们学习了 JSON 的语法。现在需要解决真正的工程问题

>How can Python read external JSON data?

完成本节后，我们将实现：

devices.json ➡ Python ➡ Device Inventory ➡ Automation

这意味着，从本节开始，设备信息将来自外部数据文件，而不是写在 Python 程序中。

## Preparing the JSON Inventory

首先，在 inventory/ 目录创建 [devices.json](Lab/invertory/devices.json)

内容如下：

```json
[
  {
    "host": "192.168.100.11",
    "username": "admin",
    "password": "cisco123",
    "device_type": "cisco_ios"
  },
  {
    "host": "192.168.100.12",
    "username": "admin",
    "password": "cisco123",
    "device_type": "cisco_ios"
  },
  {
    "host": "192.168.100.13",
    "username": "admin",
    "password": "cisco123",
    "device_type": "cisco_ios"
  }
]
```

这就是本章将要读取的 Device Inventory。

## The `json` Module

Python 标准库已经提供了读取 JSON 的模块 `import json` 这一模块在 Chapter 2 已经介绍过，因此这里不再重复讲解 import 的语法。

本节重点关注：

>如何使用 `json` 模块读取外部数据。

## Opening the File

读取 JSON 的第一步仍然是打开文件。

```python
with open("inventory/devices.json", "r") as file:
    ...
```

这里：

| Component | Description |
| --------- | ----------- |
| `with`    | 自动管理文件资源    |
| `open()`  | 打开文件        |
| `"r"`     | Read Mode   |
| `file`    | 文件对象        |

这与 Chapter 2 学习的文件读取方式完全一致。

## Parsing JSON

文件打开后，需要将 JSON 文本转换为 Python 对象。

使用 `json.load()`

完整代码如下：

```python
import json

with open("/home/user/automation_project/automation/inventory/devices.json", "r") as file:
    devices = json.load(file)
```

这里最重要的一步是 `devices = json.load(file)` 它完成了：

JSON Text ➡ Python Objects

解析（Parse）过程。

## What Does json.load() Return?

很多初学者容易误解 json.load() 返回的是字符串。实际上并不是。它返回对应的 Python 数据结构。

例如 JSON：

```json
[
  {
    "host": "192.168.100.11"
  }
]
```

读取以后 `devices = json.load(file)` 得到的是：

```python
[
    {
        "host": "192.168.100.11"
    }
]
```

注意这是一个真正的 Python List, Python Dictionary 而不是 JSON 字符串。

因此我们可以直接使用前几章学过的代码。

## Verifying the Data

可以先打印整个 Inventory：

```python
import json

with open("inventory/devices.json", "r") as file:
    devices = json.load(file)

print(devices)
```

输出：

```bash
(venv) user@ubuntu22-desktop:~$ /home/user/automation_project/venv/bin/python /home/user/automation_project/automation/main.py
[{'host': '192.168.100.11', 'username': 'admin', 'password': 'Cisco123', 'device_type': 'cisco_ios'}, {'host': '192.168.100.12', 'username': 'admin','password': 'Cisco123', 'device_type': 'cisco_ios'}, {'host': '192.168.100.13', 'username': 'admin', 'password': 'Cisco123', 'device_type': 'cisco_ios'}]
```

注意一个容易混淆的现象：

- JSON 文件使用 双引号。

- Python 打印 Dictionary 时通常显示 单引号。

例如：

JSON：`"host"`

Python：`'host'`

这是 Python 的显示方式，不表示数据发生了变化。

## Using the Inventory

由于 devices 已经变成了 Python List，因此可以直接复用 Chapter 5 的代码。

例如：

```python
import json

with open("inventory/devices.json", "r") as file:
    devices = json.load(file)

for device in devices:
    print(device["host"])
```

输出：

```bash
(venv) user@ubuntu22-desktop:~$ /home/user/automation_project/venv/bin/python /home/user/automation_project/automation/main.py
12.1.1.1
12.1.1.2
23.1.1.3
```

可以看到程序已经完全不知道设备来自哪里。它只知道 `for device in devices:` 这正是数据与代码分离带来的好处。

## Integrating with Existing Automation

现在，把读取 Inventory 与前几章的自动化结合起来。

```python
from modules.connection import (
    connect_device,
    disconnect_device,
    execute_show_command
)
import json

with open("inventory/devices.json", "r") as file:
    devices = json.load(file)

for device in devices:
    connection = connect_device(device)
    try:

        output = execute_show_command(
            connection,
            "show version"
        )
        print("=" * 60)
        print(f"CONNECTING TO DEVICE: {device['host']}".upper())
        print(f"\n{output}")
        print("=" * 60)

        disconnect_device(connection)
    except Exception as e:
        print(e)
```

注意：除了读取 Inventory 的部分之外，后面的自动化代码几乎没有任何变化。

这说明：

>程序逻辑没有改变，改变的只是数据来源。

## Error Handling

读取 JSON 时，常见问题包括：

### File Not Found

例如：inventory/device.json 写错文件名。

Python：
```python
FileNotFoundError
```
### Invalid JSON

例如：

```json
{
    "host": "10.1.1.1",
}
```

最后多了一个逗号。

Python：
```python
JSONDecodeError
```

### Wrong Data Structure

例如：程序希望读取 List 结果 JSON 保存的是：

```json
{
    "R1": {}
}
```

程序虽然能够解析，但是后续：
```python
for device in devices:
```

逻辑可能不符合预期。因此除了语法正确，还要保证 JSON 的数据结构符合程序设计。

## Engineering Best Practice

企业项目中，建议遵循以下流程：

Read External Data ➡ Validate Data ➡ Build Inventory ➡ Execute Automation

不要在程序中重复定义设备信息。Inventory 应作为自动化程序的输入，而不是程序的一部分。