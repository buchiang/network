# Chapter Objective

经过前面的学习，我们已经能够：

- 编写 Variables

- 使用 Expressions

- 编写 Loops

- 编写 Conditions

- Render Template

- 自动生成 Configuration

到这里，一个功能完整的 Jinja2 Template 已经可以工作, 但是能工作（Works）并不代表易维护（Maintainable）。

企业自动化项目通常会维护：

- 数十个 Template

- 数百台设备

- 多年的配置演进

因此，模板不仅要能够生成配置，更要具备良好的可维护性和可复用性。

本节将总结前面所有内容，并形成一套适用于整个 Workbook 的 Template Engineering Principles。

## From Working Templates to Engineering Templates

假设下面的 Template 可以正常工作：

```jinja2
hostname {{ hostname }}
interface {{ interface_name }}
 description {{ description }}
 ip address {{ ip }} {{ mask }}
 no shutdown
```

它已经能够：

✓ Render

✓ Generate Configuration

✓ Deploy

但是企业工程还需要考虑：

- 是否容易阅读？

- 是否容易修改？

- 是否容易复用？

- 是否容易扩展？

- 是否容易排查问题？

因此Template Design ≠ Template Engineering

## Keep Templates Focused

不要让一个 Template 承担过多职责。

例如不建议：

base.j2 ➡ Hostname ➡ Interfaces ➡ OSPF ➡ BGP ➡ ACL ➡ NAT ➡ QoS ➡ SNMP ➡ Logging

这样 Template 很快会达到几百行。维护难度急剧增加。

建议按照配置对象组织模板。

例如：

```
templates/

hostname.j2

interfaces.j2

ospf.j2

bgp.j2

static_routes.j2
```

每个 Template 只负责一种 Configuration 职责更加清晰。

>**说明：**
>本章保持模板相互独立，重点学习 Jinja2 基础。后续章节如果需要组合多个模板，会在对应章节介绍，不在本章提前展开。

## Keep Variable Names Consistent

Template：`hostname {{ hostname }}`

Inventory：`hostname: R1`

Python：`device["hostname"]`

三者保持一致。

不要：

Template：`{{ router_name }}`

Inventory：`hostname: R1`

Python：`device["device_name"]`

这种命名会导致阅读困难, 维护困难。企业项目建议统一命名规范。

## Keep Logic in Python

前面已经介绍过 Jinja2 支持

- 运算

- 条件

- 循环

但是 Template 不是 Business Logic Engine。

例如不要：`{{ ((base_vlan + site_id) * 100) + offset }}`

建议 Python：

```python
device = {
    "vlan_id": calculated_vlan
}
```

Template：`vlan {{ vlan_id }}`

这样

Python 负责 Logic。

Template 负责 Presentation。

职责更加明确。

## Avoid Hardcoding

Template:
不要 `hostname R1` 而应该 `hostname {{ hostname }}`

不要 `router-id 1.1.1.1` 应该 `router-id {{ router_id }}`

任何设备相关数据。都应该来自 Inventory。

Template 只保存 Configuration Structure。

## Keep Templates Readable

例如推荐：

```jinja2
interface {{ interface.name }}
 description {{ interface.description }}
 ip address {{ interface.ip }} {{ interface.mask }}
 no shutdown
```

不要：

```jinjia2
interface {{interface.name}}
description {{interface.description}}
ip address {{interface.ip}} {{interface.mask}}
no shutdown
```

统一缩进, 空行, 变量命名, 对于长期维护非常重要。

Template 本身也是 Code, 因此同样需要 Code Style。

## Validate Data Before Rendering

Template 应该假设输入的数据已经准备好。

例如不要依赖：`{% if hostname %}` 来判断 Hostname 是否存在。

更推荐 Python 先验证：

```python
required_fields = [
    "hostname",
    "loopback_ip",
    "subnet_mask"
]

for field in required_fields:
    if field not in device:
        raise ValueError(
            f"Missing required field: {field}"
        )
```

之后再 Render。这样 Template 只负责 Generate。

Python 负责 Validation。

# A Recommended Project Layout

结合 Chapter 4、5、6 和本章，一个典型的工程目录如下：

```
automation_project/

├── automation/
│   └── render_config.py
│
├── inventory/
│   ├── devices.yaml
│   └── devices.json
│
├── templates/
│   ├── hostname.j2
│   ├── interfaces.j2
│   ├── ospf.j2
│   └── static_routes.j2
│
├── output/
│   ├── R1.cfg
│   └── R2.cfg
│
├── modules/
│
└── logs/
```

职责划分：

| Directory     | Responsibility |
| ------------- | -------------- |
| `inventory/`  | 保存结构化数据        |
| `templates/`  | 保存模板           |
| `automation/` | Python 渲染程序    |
| `output/`     | 保存生成的配置        |
| `modules/`    | 可复用 Python 模块  |
| `logs/`       | 日志文件           |

这种结构与前几章保持一致，符合整个 Workbook 的工程规范。

## Engineering Principles

整个 Chapter 7 可以总结为以下工程原则：

| Principle                    | Description                      |
| ---------------------------- | -------------------------------- |
| Separate data from templates | 数据与模板分离                          |
| Keep templates simple        | 模板保持简单                           |
| Keep logic in Python         | Python 负责业务逻辑                    |
| Reuse templates              | 一个模板适用于多个设备                      |
| Use structured data          | 使用 JSON、YAML 或 Python Dictionary |
| Keep naming consistent       | 保持统一命名                           |
| Validate before rendering    | 渲染前完成数据校验                        |
| Keep project organized       | 保持统一工程目录                         |


这些原则贯穿整个 Workbook，也适用于大多数企业自动化项目。

## Chapter Summary

本章回答了一个核心工程问题：

How can we generate network configurations automatically from structured data?

答案是：

Structured Data ➡ Jinja2 Template ➡ Rendering ➡ Configuration

相比手工编写 CLI：

Engineer ➡ CLI ➡ Device

模板驱动方式实现了：

Inventory ➡ Template ➡ Rendered Configuration

这种方式具有：

- 更高的一致性（Consistency）

- 更好的可维护性（Maintainability）

- 更强的可扩展性（Scalability）

- 更低的人为错误率（Reduced Human Error）

至此，Chapter 7 完整建立了Template-Driven Automation 的基础能力，为后续更复杂的自动化流程奠定了坚实基础。