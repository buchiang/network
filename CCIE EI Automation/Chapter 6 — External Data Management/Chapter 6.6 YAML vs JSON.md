# Chapter Objective

前面几节，我们分别学习了：

- YAML

- JSON

它们都能够保存 Device Inventory。那么新的问题就是：

>Which format should we use?

实际上，这两个问题并不存在绝对的答案。企业会根据不同场景选择不同的数据格式。

本节将比较两种格式的特点，而不是判断哪一种"更好"。

## The Same Data in Two Formats

首先，看同一份 Inventory。

### YAML

```yaml
- host: 192.168.100.11
  username: admin
  password: Cisco123
  device_type: cisco_ios

- host: 192.168.100.12
  username: admin
  password: Cisco123
  device_type: cisco_ios
```

### JSON

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

两份数据完全相同, 区别只是表示方式不同。

## Readability

对于网络工程师来说 YAML 更容易阅读。

原因包括：

- 没有大量括号

- 没有大量引号

- 没有大量逗号

- 更容易发现层级关系

例如：
```yaml
host: 192.168.100.11
username: admin
password: Cisco123
```

几乎和普通配置文档一样。而 JSON：

```json
{
  "host": "192.168.100.11",
  "username": "admin",
  "password": "Cisco123"
}
```

虽然结构规范，但是视觉上更加"密集"。

因此

>对于人工维护的数据文件，YAML 通常具有更好的可读性。

## Syntax Strictness

JSON 的语法要求更加严格。

例如必须使用：`"host"` 不能写 `host` 并且每个字段之间必须有逗号, 最后一个字段不能保留逗号。

相比之下，YAML 更加宽松。

例如：host: 192.168.100.11 就已经足够。

因此：

- JSON 更强调格式一致性。

- YAML 更强调阅读体验。

## Editing Experience

假设需要新增一台设备。

YAML：
```yaml
- host: 192.168.100.13
  username: admin
  password: Cisco123
  device_type: cisco_ios
```

只需要增加几行。

JSON：
```json
,
{
  "host": "192.168.100.13",
  "username": "admin",
  "password": "Cisco123",
  "device_type": "cisco_ios"
}
```

还需要注意：

- 逗号

- 大括号

- 数组格式

因此对于经常手工编辑的 Inventory，YAML 通常更加方便。

## Python Support

对于 Python 来说：两种格式都可以读取。

JSON：

```python
import json

with open("devices.json") as file:
    devices = json.load(file)
```

YAML（将在下一节介绍）：

```python
import yaml

with open("devices.yaml") as file:
    devices = yaml.safe_load(file)
```

程序最终得到的都是 list 里面包含 dict 因此自动化程序几乎不需要修改。真正变化的是数据来源。

## Comparison Table

| Feature           | YAML      | JSON     |
| ----------------- | --------- | -------- |
| Human Readability | Excellent | Good     |
| Manual Editing    | Easy      | Moderate |
| Syntax Strictness | Flexible  | Strict   |
| Uses Indentation  | Yes       | No       |
| Uses Brackets     | Rarely    | Yes      |
| Uses Commas       | No        | Yes      |
| Python Support    | Yes       | Yes      |

从这个比较可以看出它们解决的是同一个问题：表示结构化数据, 只是设计目标略有不同。

## Which One Should We Choose?

对于本 Workbook，我们采用以下工程原则 

### YAML 

适合：

- 手工维护 Inventory

- 配置文件

- 可读性优先

### JSON

适合：

- 数据交换

- 程序之间传递数据

- 需要严格格式的场景

需要强调的是：

>这并不是一个非此即彼的选择。

一个自动化项目完全可以：

- 使用 YAML 保存静态 Inventory。

- 使用 JSON 接收其他程序生成的数据。

两种格式可以在同一个项目中共存。

## Engineering Perspective

对于自动化工程师来说，真正重要的不是学会 YAML, 或者学会 JSON, 而是理解 Python 程序不应该依赖某一种具体的数据格式。

只要能够构建出相同的 Python 数据结构，自动化程序就可以继续运行。这也是软件工程中**数据与逻辑解耦（Decoupling Data from Logic）**的重要体现。

## Engineering Best Practice

在本 Workbook 中，我们建议：

- 将 YAML 作为默认的人工维护 Inventory 格式。

- 理解并能够读取 JSON，因为它广泛用于自动化工具和系统间的数据交换。

- 不在程序中写死设备信息，而是统一从外部数据文件读取。

这样，无论未来数据来源如何变化，自动化逻辑都可以保持稳定。