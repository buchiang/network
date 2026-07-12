# Chapter Objective

上一节介绍了：

- Variables

- Expressions

- Filters

这些内容解决了：**如何输出数据（Output Data）**

但是，在企业网络中，仅仅输出数据是不够的。

例如：

有些设备需要：`router ospf 1`

有些设备则运行：`router bgp 65001`

有些接口需要：`shutdown`

有些接口需要：`no shutdown`

还有些配置只有满足某个条件才需要生成。

因此，我们需要：

>Control Structures（控制结构）

## What Are Control Structures?

Control Structure 的作用是-控制模板应该生成哪些内容。

Variables 负责输出数据

Control Structures 负责控制输出

因此 Template 不再只是：

Data ➡ Output

而是：

Data ➡ Decision ➡ Output

这也是 Template 开始具有"逻辑能力"的地方。

## Jinja2 Statement Syntax

Variables 使用 `{{ }}`

Control Structures 使用 `{% %}`

例如：`{% if ... %}` 或者 `{% for ... %}` 因此可以区分：

| Syntax  | Purpose           |
| ------- | ----------------- |
| `{{ }}` | 输出变量（Output）      |
| `{% %}` | 执行控制语句（Statement） |

## Output vs Statement

例如 `{{ hostname }}` 会输出 `R1` 但是 `{% if ospf_enabled %}` 不会输出任何内容。它只是告诉 Jinja2 **接下来应该如何处理模板。**因此：

Statement 不产生文本。

Statement 控制文本。

## Block Structure

Jinja2 的 Statement 通常都是 Block（代码块）。

例如：

```jinja2
{% if condition %}
...
{% endif %}
```

或者：

```jinja2
{% for interface in interfaces %}
...
{% endfor %}
```

可以发现都有：开始 ➡ 结束

这种结构与 Python 非常相似。

例如 Python：

```python
if condition:
    print("Hello")
```

Jinja2：

```jinja2
{% if condition %}
Hello
{% endif %}
```

虽然语法不同，但逻辑完全一致。

## Nested Blocks

Block 可以嵌套, 例如：For ➡ If ➡ Output

示意图：

```
For

    If

        Variable

    End If

End For
```

以后我们会看到例如：

遍历所有 Interface ➡ 判断 Interface 是否启用 ➡ 输出配置

这就是企业网络模板最常见的结构。

>本章后续会分别介绍 for 和 if 的具体语法，这里先建立控制结构可以嵌套的概念。

## Statements Are Not Rendered

例如 Template：

```jinja2
{% if enabled %}
hostname {{ hostname }}
{% endif %}
```

最终生成：`hostname R1`

注意下面这些内容：`{% if enabled %}` 以及 `{% endif %}` 不会出现在最终配置中。

Render 后它们已经消失。最终只剩 Cisco CLI。

因此 Template 包含：

- Variables

- Statements

最终 Configuration 只有 Cisco CLI。

## Jinja2 都能够正常 Render。

但是统一的缩进和留白能够：

- 更容易阅读

- 更容易维护

- 更容易排查错误

Template 本质上也是代码（Code）因此 Template 也需要遵循代码规范。

## Template Formatting

建议保持每个逻辑块之间留空行。

例如：

```jinja2
hostname {{ hostname }}

interface Loopback0

 ip address {{ loopback_ip }} {{ subnet_mask }}

router ospf {{ process_id }}

 router-id {{ router_id }}
```

与 Cisco CLI 保持相近的布局。

这样 Render 前 Template ➡ Render 后 Configuration 视觉结构几乎一致, 工程师阅读起来更加自然。

>**说明：**
>空行和缩进主要用于提高模板可读性。实际渲染后的配置格式取决于模板内容，团队应保持统一的排版风格，避免无意义的格式差异。

## Separation of Responsibilities

到目前为止，整个 Template Engine 的职责已经十分清晰。

Inventory 负责提供数据

Template 负责定义配置结构

Control Structure 负责决定生成哪些配置

Variables 负责填充数据

最终生成 Configuration。

整个流程：

Inventory ➡ Variables ➡ Statements ➡ Rendering ➡ Configuration

可以发现整个系统已经开始具有明显的模块化（Modular）设计。

## Engineering Guidelines

企业模板通常遵循以下原则：

| Guideline                             | Description      |
| ------------------------------------- | ---------------- |
| Use statements only for template flow | 控制结构仅用于模板流程控制。   |
| Keep nesting shallow                  | 避免过深的嵌套，提高可读性。   |
| Maintain consistent indentation       | 保持统一缩进风格。        |
| Separate logic from formatting        | 控制逻辑与配置内容保持清晰分离。 |
| Keep templates readable               | 模板应像配置文件一样易于阅读。  |

需要强调的是虽然 Jinja2 支持较复杂的模板逻辑，但企业项目通常不会把业务逻辑全部写进 Template。复杂逻辑仍然放在Python。Template 负责 Configuration Layout。

## Engineering Summary

控制结构（Control Structures）为 Jinja2 模板引入了流程控制能力。与使用 `{{ ... }}` 输出变量不同，控制结构使用 `{% ... %}` 执行语句，它们不会直接出现在最终配置中，而是决定哪些内容需要被渲染。

控制结构与变量各司其职：变量负责填充数据，控制结构负责决定配置的生成流程。随着模板复杂度增加，保持统一的缩进、合理的块结构以及清晰的职责划分，对于企业级模板的可维护性至关重要。

下一节将正式学习 Loops（循环），通过 `for` 语句实现接口、静态路由等重复配置的自动生成，这是模板驱动自动化中最常见、最实用的能力之一。