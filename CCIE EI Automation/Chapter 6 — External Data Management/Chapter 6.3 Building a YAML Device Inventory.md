# Chapter Objective

上一节，我们学习了 YAML 的基本语法, 但是，仅仅了解 YAML 语法还不足以用于网络自动化。

本节将回答新的工程问题：

>How can we store a device inventory in YAML?

完成本节后，我们将把 Chapter 5 中的 Python Inventory 迁移为一个独立的 YAML 数据文件，实现真正的数据与代码分离。

## From Python Inventory to YAML Inventory

回顾 Chapter 5，我们使用的是 Python Dictionary：

```python
devices = [
    {
        "host": "192.168.100.11",
        "username": "admin",
        "password": "Cisco123",
        "device_type": "cisco_ios",
    },
    {
        "host": "192.168.100.12",
        "username": "admin",
        "password": "Cisco123",
        "device_type": "cisco_ios",
    }
]
```

这里存在一个问题 Inventory 和 Python 程序混在一起。我们的目标是把这些设备信息移动到独立的数据文件。

例如：

```
automation_project/

├── inventory/
│   ├── devices.py      ← Chapter 5
│   └── devices.yaml    ← Chapter 6
│
├── modules/
├── scripts/
└── main.py
```

从这一刻开始 Python 负责逻辑, YAML 负责数据。

## YAML Sequence（列表）

在 Python 中：

```python
devices = [
    ...
]
```

是一个 List。

YAML 也支持列表，称为 Sequence

Sequence 使用 `-` 表示一个新的元素。

例如：

```yaml
- R1
- R2
- R3
```

可以理解为：

```python
[
    "R1",
    "R2",
    "R3"
]
```

因此：Python List ➡ YAML Sequence

## YAML Mapping（字典）

Chapter 2 学过 Python Dictionary：

```python
device = {
    "hostname": "R1",
    "ip": "10.1.1.1"
}
```

对应 YAML：

```yaml
hostname: R1
ip: 10.1.1.1
```

YAML 中这种 Key–Value 结构称为 Mapping

因此：Python Dictionary ➡ YAML Mapping

## Combining Sequence and Mapping

企业 Inventory 并不是一个字符串列表。而是多个设备对象。

因此每个设备都是一个 Mapping。多个设备组成一个 Sequence。

例如：

```yaml
- hostname: R1
  ip: 10.1.1.1

- hostname: R2
  ip: 10.1.1.2
```

可以理解为：

```
Sequence

├── Device 1 (Mapping)

└── Device 2 (Mapping)
```

这是网络自动化最常见的 YAML 结构。

## Building the First Device Inventory

现在，把 Chapter 5 的 Inventory 转换为 YAML。

创建 [devices.yaml](Lab/invertory/devices.yaml)

内容如下：

```yaml
- host: 12.1.1.1
  username: admin
  password: Cisco123
  device_type: cisco_ios

- host: 12.1.1.2
  username: admin
  password: Cisco123
  device_type: cisco_ios

- host: 23.1.1.3
  username: admin
  password: Cisco123
  device_type: cisco_ios
```

可以发现没有：

- `{ }`
- `[ ]`
- `,`

整个 Inventory 更容易阅读。

## Comparing Python and YAML

同一份 Inventory：

Python：

``` python
devices = [
    {
        "host": "192.168.100.11",
        "username": "admin",
        "password": "Cisco123",
        "device_type": "cisco_ios",
    }
]
```

YAML：

```yaml
- host: 192.168.100.11
  username: admin
  password: Cisco123
  device_type: cisco_ios
```

可以看到 Python 更强调语法, YAML 更强调数据。

因此：Python 适合编程, YAML 适合保存配置和 Inventory。

## Naming Conventions

为了保持整个 Workbook 的一致性，我们统一采用以下字段名称。

| Field       | Description           |
| ----------- | --------------------- |
| host        | Management IP Address |
| username    | SSH Username          |
| password    | SSH Password          |
| device_type | Netmiko Device Type   |


保持与前几章完全一致：

```yaml
- host: 192.168.100.11
  username: admin
  password: Cisco123
  device_type: cisco_ios
```

不要混用 ip 和 host 因为 Netmiko 默认使用 host 统一字段名称可以减少后续代码转换工作。

## Inventory Validation

一个合格的 Inventory 应满足以下要求：

✓ 每台设备都具有：

- host

- username

- password

- device_type

✓ 所有字段拼写一致。

例如：

正确 `device_type: cisco_ios`

错误 `deviceType: cisco_ios`

或者 `device-type: cisco_ios`

字段名称的不一致会导致 Python 程序无法正确读取。因此，在团队中应统一字段命名规范。

## Engineering Practice

在企业环境中，一个 Inventory 文件通常应遵循以下原则：

- 一个文件保存一种类型的数据。

- 字段名称在整个项目中保持一致。

- 使用统一的缩进风格。

- 避免重复信息。

- 保持数据文件简洁，仅包含数据。

目前，我们的 [devices.yaml](Lab/invertory/devices.yaml) 只保存设备连接信息，这已经足够支撑前几章完成的自动化任务。

随着课程推进，Inventory 会逐步扩展，但始终遵循“数据与代码分离”的原则。

>注意： 为了符合本章范围，我们暂不引入更复杂的 Inventory 组织方式（如按站点、角色分组等），这些属于后续自动化框架或 Source of Truth 的内容，不在本章讨论范围内。