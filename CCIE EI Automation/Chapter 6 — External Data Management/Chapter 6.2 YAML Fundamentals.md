# Chapter Objective

上一节，我们回答了：

>Why should automation data be separated from Python code?

现在需要回答新的问题：

>If the data is no longer stored in Python, where should it be stored?

企业自动化中最常见的答案之一就是 YAML。

本节将学习 YAML 的基本语法，为下一节构建设备 Inventory 做准备。

## What is YAML?

YAML 是一种用于表示结构化数据（Structured Data）的文本格式。YAML 本身不是一种编程语言，它不会执行任何逻辑，而是专门用于描述数据。

例如，一个设备可以用 YAML 表示为：

```yaml
hostname: R1
ip: 10.1.1.1
username: admin
password: Cisco123
```

这里没有：

- if

- for

- while

- function

只有数据。因此，YAML 更适合作为自动化程序的输入，而不是程序本身。

## Why YAML?

为什么网络自动化中广泛使用 YAML？

主要原因是它非常容易阅读和编写。

例如，同样的数据 Python Dictionary：

```python
device = {
    "hostname": "R1",
    "ip": "10.1.1.1",
    "username": "admin",
    "password": "Cisco123"
}
```

YAML：

```yaml
hostname: R1
ip: 10.1.1.1
username: admin
password: Cisco123
```

可以看到：

- 没有 { }

- 没有引号（大多数情况下可以省略）

- 没有逗号

- 更接近自然语言

对于大型 Inventory，可读性明显更高。

## YAML Uses Indentation

YAML 最重要的规则就是：

>YAML uses indentation to represent hierarchy.

也就是说缩进表示数据之间的层级关系。

例如：

```yaml
device:
  hostname: R1
  ip: 10.1.1.1
```

可以理解为：

```
device
│
├── hostname
└── ip
```

这里 `hostname` 和 `ip` 都属于 `device` 因为它们具有相同的缩进。

## Indentation Rules

YAML 没有规定必须使用几个空格, 但是工程实践中通常使用 **2 Spaces**

例如：

```yaml
device:
  hostname: R1
  ip: 10.1.1.1
```

也可以使用4 Spaces：

```yaml
device:
    hostname: R1
    ip: 10.1.1.1
```

虽然语法正确，但是整个 Workbook 将统一采用2个空格缩进。这样可以保持所有 YAML 文件风格一致。

## Engineering Standard

本 Workbook 统一遵循：

- 使用空格（Spaces）

- 不使用 Tab

- 每一级缩进 2 个空格

例如：

```
site:
  building:
    floor:
      rack: Rack-01
```

层级关系如下：

```
site
└── building
    └── floor
        └── rack
```

## Key–Value Pairs

YAML 最基本的数据结构是 Key–Value Pair（键值对）

格式为 key: value

例如 `hostname: R1`

这里：

Key ➡ hostname

Value ➡ R1

更多示例：

```yaml
username: admin
password: Cisco123
vendor: Cisco
model: IOSv
```

每一行都是一个独立的键值对。

## YAML Data Types

YAML 能够表示多种数据类型。下面是网络自动化中最常见的几种。

### String

```yaml
hostname: R1
username: admin
```

字符串通常可以直接书写。

如果包含特殊字符或需要保留格式，也可以使用引号 `hostname: "R1"`

整个 Workbook 中，当字符串不包含特殊字符时，默认省略引号，以保持文件简洁。

### Integer

```yaml
asn: 65001
vlan: 10
```

数字无需引号。

### Boolean

```yaml
enabled: true
enabled: false
```

注意这是布尔值，而不是字符串。

因此 `enabled: "true"` 与 `enabled: true` 表示的含义不同。

## Comments

YAML 使用：`#` 表示注释。

例如：

```yaml
# Core Router
hostname: R1
ip: 10.1.1.1
```

或者：

```yaml
hostname: R1
# Management Interface
management_ip: 192.168.100.11
```

注释不会被程序读取。它们仅用于帮助工程师理解文件内容。

## Quotation Marks

很多初学者都会问: 什么时候需要使用引号？

对于目前学习的内容，可以遵循一个简单原则-普通字符串可以不加引号。

例如：

```yaml
hostname: R1
vendor: Cisco
```

只有在字符串中包含特殊字符、前后空格或需要避免歧义时，才建议使用引号。

例如：

```yaml
description: "Core Router - Building A"
```

在本 Workbook 的所有示例中，为了保持一致性：普通字符串默认不使用引号, 必要时再使用双引号。

## Common Beginner Mistakes

学习 YAML 时，最常见的错误包括：

### 1. 使用 Tab 缩进

错误：

```yaml
device:
<Tab>hostname: R1
```

正确：

```yaml
device:
  hostname: R1
```

### 2. 缩进不一致

错误：

```yaml
device:
  hostname: R1
   ip: 10.1.1.1
```

正确：

```yaml
device:
  hostname: R1
  ip: 10.1.1.1
```

同一级内容必须保持相同缩进。

### 3. 忘记空格

错误：`hostname:R1`

正确：`hostname: R1`

冒号后应保留一个空格。

## Engineering Best Practice

编写 YAML 文件时，建议遵循以下规范：

- 使用 UTF-8 编码。

- 使用 .yaml 扩展名（整个 Workbook 统一使用 .yaml，而不是 .yml）。

- 使用 2 个空格缩进。

- 不使用 Tab。

- 保持同一级键对齐。

- 在必要位置添加注释，提高可读性。

- 数据文件仅保存数据，不混入任何 Python 代码。

这些规范有助于团队协作，也能减少由于格式问题导致的解析错误。