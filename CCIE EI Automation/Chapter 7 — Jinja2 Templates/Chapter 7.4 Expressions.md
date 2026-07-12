# hapter Objective

上一节学习了 Jinja2 最基础的功能 Variables（变量）, 变量只能完成最简单的工作: 将一个值原样输出。

例如：`hostname {{ hostname }}`

输出：`hostname R1`

但是，企业网络中的配置往往需要对数据进行简单处理。

例如：

- 拼接字符串

- 大小写转换

- 数值计算

- 默认值处理

这些都属于：Expressions（表达式）

本节将学习：

- 什么是 Expression

- Arithmetic Expressions

- String Expressions

- Comparison Expressions

- Built-in Filters（基础）

- 企业工程中的使用原则

## What Is an Expression?

Variable：`{{ hostname }}` 只是输出 `hostname` 对应的值。

而 Expression 可以在输出之前进行计算。

例如：`{{ 10 + 20 }}`

Render：`30`

这里 `10 + 20` 就是一个 Expression。

Jinja2 会先计算 10 + 20 然后输出：30

因此：

> Variable 是数据。Expression 是对数据进行计算。

## Arithmetic Expressions

Jinja2 支持基本数学运算。

例如：`{{ 10 + 5 }}` 输出：`15`

减法：`{{ 10 - 3 }}` 输出：`7`

乘法：`{{ 4 * 5 }}` 输出：`20` 

除法：`{{ 20 / 4 }}` 输出：`5.0`

也可以结合变量：`{{ vlan_id + 1 }}`

如果：`vlan_id = 100`

Render：`101`

>**工程实践说明：**
>在网络模板中，算术表达式通常只用于简单计算，例如 VLAN 编号偏移、计数值或索引。复杂计算应放在 Python 中完成，而不是在模板中实现业务逻辑。

## String Expressions

字符串可以进行拼接。

例如：`{{ hostname ~ "-MGMT" }}`

如果：`hostname = "R1"`

Render：`R1-MGMT`

再例如：`{{ "Loopback" ~ loopback_id }}`

如果：`loopback_id = 0`

Render：`Loopback0`

Jinja2 使用：`~

作为字符串连接（Concatenation）运算符，而不是 Python 中的 + , 这是 Jinja2 的语法特点。

## Comparison Expressions

Jinja2 支持比较运算。

例如：`{{ ospf_area == 0 }}`

如果：ospf_area = 0`

Render：`True`

如果：`ospf_area = 1`

Render：`False`

比较表达式本身很少直接输出。

它们主要用于下一节将学习的：

- if

- elif

- else

条件判断。

## Built-in Filters

除了表达式，Jinja2 还提供了大量内置过滤器（Filters）。

Filter 的作用是：对变量进行简单转换。

基本语法：`{{ variable | filter }}`

例如：`{{ hostname | upper }}`

如果：`hostname = "r1"`

Render：`R1`

全部转为小写：`{{ hostname | lower }}`

输入：`R1`

输出：`r1`

去除首尾空格：`{{ description | trim }}`

输入：`"  WAN Link  "`

输出：`WAN Link`

首字母大写：`{{ hostname | capitalize }}`

输入：`branch01`

输出：`Branch01`

这些转换不会修改原始数据，只影响渲染结果。

## Default Values

企业网络中，有些字段可能是可选的。

例如：`description = None` 或者某些设备没有配置描述（Description）。

这时可以使用：`{{ description | default("No Description") }}`

如果：`description` 不存在，

Render：`No Description`

如果：`description = "WAN Link"`

Render：`WAN Link`

这样可以避免模板因为缺少可选数据而产生空输出。

>**注意：**
>default 用于提供合理的默认值，而不是掩盖 Inventory 中缺失的必需字段。对于 hostname、IP 地址等关键参数，仍应在数据准备阶段进行验证。

## Chaining Filters

多个 Filter 可以连续使用。

例如：`{{ hostname | trim | upper }}`

输入：`"  r1 "`

Render：`R1`

执行顺序：trim ➡ upper

即：先去除空格，再转换为大写。

## Keep Logic Simple

Jinja2 支持较复杂的表达式。

例如：`{{ (vlan_id + 100) * 2 }}`

甚至：`{{ hostname | upper | trim }}`

这些语法都是合法的。

但是，企业工程中应遵循一个原则：

>Template 负责展示（Presentation），Python 负责计算（Logic）。

例如不推荐：`{{ ((base_vlan + site_id) * 10) + offset }}`

推荐：

Python：

```python
render_data = {
    "vlan_id": calculated_vlan
}
```

Template：`vlan {{ vlan_id }}`

这样：

- Template 更容易阅读

- Python 更容易测试

- 逻辑更集中

- 后期维护成本更低

## Engineering Guidelines

企业项目中，建议遵循以下原则：

| Guideline                        | Description         |
| -------------------------------- | ------------------- |
| Use expressions sparingly        | 表达式应保持简单、直观。        |
| Prefer Python for complex logic  | 复杂计算放在 Python 中完成。  |
| Use filters for formatting       | 格式转换优先使用 Filter。    |
| Keep templates readable          | 模板应主要体现配置结构，而非业务逻辑。 |
| Use default values appropriately | 默认值用于可选字段，不应替代数据验证。 |

## Engineering Summary

表达式（Expressions）扩展了变量的能力，使模板不仅能够输出数据，还能够进行简单的计算、字符串处理和格式转换。Jinja2 还提供了丰富的内置过滤器（Filters），用于完成大小写转换、空白处理和默认值等常见操作。

在企业级模板设计中，应坚持**“Template for Structure, Python for Logic”** 的原则。模板应保持简洁、可读，负责描述配置结构；复杂的数据处理和业务逻辑应放在 Python 程序中完成。这种职责划分能够提高模板的可维护性，并降低长期工程维护成本。

下一节将学习 Control Structures（控制结构），介绍如何在模板中根据不同的数据生成不同的配置内容。