# Chapter Objective

上一节介绍了 Jinja2 Template Engine 的工作方式。

但是，一个 Template 为什么能够适用于不同设备？

关键就在于：

>Variables（变量）

变量是 Jinja2 最基础、也是最重要的组成部分。

本节将学习：

- 什么是 Template Variable

- Jinja2 Variable Syntax

- Variable Replacement

- 使用 Python Data Render Template

- 企业工程中的变量设计原则

## What Is a Variable?

在 Chapter 2 中，我们已经学习过 Python Variable。

例如：`hostname = "R1"` 这里 `hostname` 是变量名称（Variable Name）。而 `R1` 是变量的值（Value）。

Jinja2 也有变量。不同的是：

Python Variable：`hostname = "R1"`

Jinja2 Variable：`{{ hostname }}`

二者表示的是同一个概念：

>这里有一个变量，它的值将在运行时确定。

## Variable Delimiters

Jinja2 使用：`{{ }}` 表示输出一个变量。

例如：`hostname {{ hostname }}` 这里固定内容 `hostname` 变量 `{{ hostname }}`

最终生成：hostname R1

如果：hostname = "R2" 则生成 hostname R2

因此 `{{ }}` 表示：

>"将变量输出到最终结果中。"

这是 Jinja2 中最常见的语法。

## The Rendering Process

例如Template `hostname {{ hostname }}` 

Python Data：

```python
data = {
    "hostname": "R1"
}
```

Render 后 `hostname R1`

整个过程：

```
Template
hostname {{ hostname }}

        │
        ▼

Data
hostname = R1

        │
        ▼

Rendering

        │
        ▼

hostname R1
```
Template 保持不变, 变化的是 Data。

## Multiple Variables

Template 通常包含多个变量, 例如：

```jinja2
hostname {{ hostname }}

interface Loopback0
 ip address {{ loopback_ip }} {{ subnet_mask }}
```

Data：

```python
{
    "hostname": "R1",
    "loopback_ip": "1.1.1.1",
    "subnet_mask": "255.255.255.255"
}
```

Render：

```
hostname R1

interface Loopback0
 ip address 1.1.1.1 255.255.255.255
```

可以发现 Template 中有几个变量，Jinja2 就会替换几个变量。

## Variables Can Appear Anywhere

变量不仅可以位于一行的末尾。

例如：`hostname {{ hostname }}`

也可以位于字符串中间：`description Connected to {{ neighbor }}`

Render：`description Connected to R2`

变量也可以组成整个字符串：`{{ interface_name }}`

Render：`GigabitEthernet0/0`

甚至多个变量连续出现：`{{ ip_address }}/{{ prefix_length }}`

Render：`10.1.1.1/30`

因此：Jinja2 并不限制变量出现的位置。

它只负责：

找到变量 ➡ 替换变量 ➡ 输出结果。

## Variables Come from Structured Data

Jinja2 本身不会产生数据, 变量必须来自：

- Python Dictionary

- JSON

- YAML

例如 Python：

```python
device = {
    "hostname": "R1",
    "loopback": "1.1.1.1"
}
```

JSON：

```json
{
    "hostname": "R1",
    "loopback": "1.1.1.1"
}
```

YAML：

```yaml
hostname: R1
loopback: 1.1.1.1
```

无论数据来自哪里，最终都会转换成 Python 数据对象，Jinja2 使用这些对象完成渲染。

因此：

> Jinja2 不关心数据来源，只关心变量名称和值。

## Variable Names

变量名称应该具有明确的工程含义。

例如推荐：

```jinja2
{{ hostname }}

{{ router_id }}

{{ loopback_ip }}

{{ interface_name }}

{{ ospf_process }}

{{ area }}

{{ description }}
```

避免：

```jinja2
{{ a }}

{{ value }}

{{ test }}

{{ x }}

{{ item1 }}
```

原因很简单, Template 通常会被：

- 多个工程师维护

- 长期维护

- 多个项目复用

清晰的变量名称能够显著提高可读性。

例如：`router-id {{ router_id }}` 比 `router-id {{ value }}` 更容易理解。

## Variable Naming Consistency

变量名称应该与 Inventory 保持一致。

例如：

Inventory：

```yaml
hostname: R1
loopback_ip: 1.1.1.1
router_id: 1.1.1.1
```

Template：

```jinja2
hostname {{ hostname }}
router-id {{ router_id }}
ip address {{ loopback_ip }}
```

不要出现：

Inventory：

```yaml
hostname: R1
```

Template：

```jinja2
{{ device_name }}
```

这种情况会导致 Template 找不到对应变量。

因此：

Template ➡ Inventory ➡ Python Dictionary

三者应使用完全一致的变量名称, 这是企业工程中的重要规范。

## Variables Do Not Change the Template

Template：`hostname {{ hostname }}`

第一次 Render：`hostname = "R1"`

得到：`hostname R1`

第二次：`hostname = "R2"`

得到：`hostname R2`

第三次：`hostname = "Branch-01"`

得到：`hostname Branch-01`

可以看到 Template 始终没有发生变化。变化的是 Data。

这正是 Template 最大的优势

>一次编写，多次复用。

## Engineering Guidelines

企业项目中，建议遵循以下变量设计原则：

| Guideline                    | Description                         |
| ---------------------------- | ----------------------------------- |
| Use meaningful names         | 使用具有明确含义的变量名。                       |
| Keep names consistent        | Inventory、Template 和 Python 使用相同名称。 |
| Separate data from templates | 不要在模板中写死设备信息。                       |
| Avoid abbreviations          | 除非是行业通用缩写，否则避免使用不明确的缩写。             |
| Reuse variables              | 相同的数据在模板中重复使用同一个变量。                 |

例如：

```jinja2
hostname {{ hostname }}

router ospf 1
 router-id {{ router_id }}

interface Loopback0
 ip address {{ router_id }} 255.255.255.255

```
这里：`{{ router_id }}` 在模板中被复用。

如果 Inventory 修改 `router_id: 10.10.10.10` 模板中的所有引用都会自动更新，无需修改模板本身。

## Engineering Summary

变量（Variables）是 Jinja2 模板的基础，它们使用 `{{ ... }}` 语法表示需要在渲染时替换的数据。模板定义配置结构，而变量提供设备之间的差异信息。

在企业自动化项目中，变量应始终来自结构化数据（如 Python Dictionary、JSON 或 YAML），并保持与 Inventory 一致的命名规范。通过将设备参数抽象为变量，同一份模板即可生成任意数量的设备配置，实现真正的数据与配置结构分离，为后续学习表达式（Expressions）、循环（Loops）和条件（Conditions）打下基础。