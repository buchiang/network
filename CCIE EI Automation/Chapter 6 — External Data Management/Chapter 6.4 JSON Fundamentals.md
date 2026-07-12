# Chapter Objective

上一节，我们学习了 YAML，并使用 YAML 构建了第一个 Device Inventory, 但是，YAML 并不是网络自动化中唯一的数据格式。

另一种非常重要的数据格式是：

> JSON (JavaScript Object Notation)

JSON 广泛应用于网络自动化、云平台以及各种软件系统之间的数据交换。

本节仅介绍 JSON 的基本语法和数据结构，为下一节使用 Python 读取 JSON 做准备。

## What is JSON?

JSON 是一种轻量级的结构化数据格式，用于存储和交换数据。和 YAML 一样

JSON：

- 不是编程语言

- 不包含程序逻辑

- 专门用于描述数据

例如，一个设备可以表示为：

```json
{
  "host": "192.168.100.11",
  "username": "admin",
  "password": "Cisco123",
  "device_type": "cisco_ios"
}
```

这里仅保存设备信息，没有任何 Python 代码。

## Why JSON?

JSON 具有几个重要特点：

- 结构清晰

- 易于程序解析

- 几乎所有编程语言都支持

- 广泛用于不同系统之间的数据交换

在网络自动化中，JSON 经常作为程序之间交换数据的标准格式。因此，即使工程师平时更喜欢编写 YAML，也必须能够阅读和理解 JSON。

## JSON Objects

JSON 最基本的数据结构是 Object

Object 由一组 Key–Value Pair 组成。格式如下：

``` json
{
  "key": "value"
}
```

例如：

```json
{
  "hostname": "R1",
  "ip": "10.1.1.1"
}

与 Python Dictionary 非常相似：

device = {
    "hostname": "R1",
    "ip": "10.1.1.1"
}
```

因此可以建立对应关系：

| Python     | JSON   |
| ---------- | ------ |
| Dictionary | Object |

## JSON Arrays

如果需要保存多个对象，就需要使用：

>Array

例如：

```json
[
  "R1",
  "R2",
  "R3"
]
```

对应 Python：

```python
[
    "R1",
    "R2",
    "R3"
]
```

因此：

| Python | JSON  |
| ------ | ----- |
| List   | Array |

## Combining Objects and Arrays

企业 Inventory 通常由多个设备对象组成。因此 JSON Inventory 的结构通常是：

```json
[
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

可以理解为：

```
Array

├── Object (Device 1)

└── Object (Device 2)
```

这与上一节学习的：

YAML Sequence

YAML Mapping

完全对应。

## JSON Syntax Rules

JSON 的语法比 YAML 更严格, 需要牢记以下规则。

### Rule 1 — Keys Must Use Double Quotes

正确：

```json
{
  "hostname": "R1"
}
```

错误：

```json
{
  hostname: "R1"
}
```

JSON 要求所有 Key 必须使用双引号。

### Rule 2 — String Values Use Double Quotes

正确：

```json
{
  "hostname": "R1"
}
```

错误：

```json
{
  "hostname": R1
}
```

字符串必须使用双引号。

### Rule 3 — Commas Are Required

正确：

```json
{
  "host": "10.1.1.1",
  "username": "admin"
}
```

错误：

```json
{
  "host": "10.1.1.1"
  "username": "admin"
}
```

每个字段之间必须使用逗号分隔。

### Rule 4 — No Trailing Comma

正确：

```json
{
  "host": "10.1.1.1"
}
```

错误：

```json
{
  "host": "10.1.1.1",
}
```

最后一个字段后面不能保留逗号。

## JSON Data Types

JSON 常见的数据类型包括：

| Data Type | Example          |
| --------- | ---------------- |
| String    | `"R1"`           |
| Number    | `65001`          |
| Boolean   | `true` / `false` |
| Array     | `[1, 2, 3]`      |
| Object    | `{ ... }`        |
| Null      | `null`           |

例如：

```json
{
  "hostname": "R1",
  "asn": 65001,
  "enabled": true
}
```

这些数据类型与 Python 中的对应关系将在下一节读取 JSON 时体现出来。

## YAML vs JSON Syntax

同一份设备数据：

YAML：

```yaml
- host: 192.168.100.11
  username: admin
  password: Cisco123
  device_type: cisco_ios
```

JSON：

```json
[
  {
    "host": "192.168.100.11",
    "username": "admin",
    "password": "Cisco123",
    "device_type": "cisco_ios"
  }
]
```

可以发现：

- YAML 更简洁，更适合人工编写。

- JSON 语法更严格，但结构更加规范。

目前只需要能够阅读两种格式即可，下一节将学习如何使用 Python 读取 JSON 文件。

## Common Beginner Mistakes

学习 JSON 时，最常见的问题包括：

### 1. 使用单引号

错误：

```json
{
  'hostname': 'R1'
}
```

正确：

```json
{
  "hostname": "R1"
}
```

JSON 只允许双引号。

2. 忘记逗号

错误：

```json
{
  "host": "10.1.1.1"
  "username": "admin"
}
```

正确：

```json
{
  "host": "10.1.1.1",
  "username": "admin"
}
```

### 3. 保留最后一个逗号

错误：

```json
{
  "host": "10.1.1.1",
}
```json

正确：

```json
{
  "host": "10.1.1.1"
}
```

## Engineering Best Practice

整个 Workbook 对 JSON 文件统一采用以下规范：

- 使用 UTF-8 编码。

- 使用 .json 扩展名。

- 使用 2 个空格缩进，提高可读性。

- Key 统一使用双引号。

- 字段命名与 YAML Inventory 保持一致，例如：host、username、password、device_type。

这样可以确保 YAML 和 JSON 之间能够方便地转换，而无需修改自动化逻辑。