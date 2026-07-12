# Chapter Objective

在前面的章节中，我们已经学习了：

- Variables

- Expressions

- Control Structures

- Loops

- Conditions

但是，到目前为止，我们一直是在讨论 Template 本身。还有最后一个问题没有回答如何让 Python 使用 Jinja2 模板生成最终配置？

本节将介绍完整的模板渲染（Rendering）流程，包括：

- 加载 Template

- 创建 Jinja2 Environment

- 传入结构化数据

- 渲染（Render）

- 输出生成的配置文件

## The Rendering Workflow

整个渲染过程可以概括为：

```
Inventory (JSON / YAML)
          │
          ▼
Python Dictionary
          │
          ▼
Load Template (.j2)
          │
          ▼
Jinja2 Render
          │
          ▼
Rendered Configuration
          │
          ▼
Write to File
```

整个过程中：

- Inventory 提供数据

- Template 定义配置结构

- Python 协调整个流程

- Jinja2 完成渲染

各组件职责清晰，互不耦合。

## Creating a Template

首先，在 templates/ 目录创建 [hostname.j2](Lab/templates/hostname.j2)

内容如下：

```jinja2
hostname {{ hostname }}

interface Loopback0
 ip address {{ loopback_ip }} {{ subnet_mask }}
```

这是整个 Workbook 的第一个完整 Template。

## Preparing the Data

Python 中准备数据：

```python
device = {
    "hostname": "R1",
    "loopback_ip": "1.1.1.1",
    "subnet_mask": "255.255.255.255"
}
```

注意这里的数据来源并不重要。它可以来自：

- Python Dictionary

- JSON

- YAML

对于 Jinja2 来说，最终看到的都是 Python 对象。

## Creating the Jinja2 Environment

Jinja2 使用 Environment 管理模板。

首先导入：`from jinja2 import Environment, FileSystemLoader`

然后创建：

```python
environment = Environment(
    loader=FileSystemLoader("templates")
)
```

这里 `FileSystemLoader` 告诉 Jinja2 Template 文件存放在哪里。在本 Workbook 中统一使用 `templates/` 作为模板目录。

## Loading the Template

加载模板：

```python
template = environment.get_template(
    "hostname.j2"
)
```

此时 Python 已经读取 `templates/hostname.j2` 但是还没有生成 Configuration。因为还没有提供数据。

## Rendering the Template

调用 `rendered_config = template.render(device)` 这里 device 就是上一节准备的数据：

```python
{
    "hostname": "R1",
    "loopback_ip": "1.1.1.1",
    "subnet_mask": "255.255.255.255"
}
```

Render 后 hostname R1

```
interface Loopback0
 ip address 1.1.1.1 255.255.255.255
```

整个过程只需要一行代码 `template.render(device)` 这是 Jinja2 最核心的 API。

## Writing the Configuration to a File

通常，Render 后不会立即发送到设备。而是先生成配置文件。

例如：

```python
with open(
    "output/R1.cfg",
    "w"
) as file:
    file.write(rendered_config)
```

最终项目目录 

```
automation_project/

templates/
    hostname.j2

output/
    R1.cfg
```

生成：

```
hostname R1

interface Loopback0
 ip address 1.1.1.1 255.255.255.255
```

生成配置文件后，工程师可以：

- 检查配置

- 保存归档

- 与基线配置比较

- 再决定是否部署到设备

这种流程比直接生成后立即下发更容易验证和审查。

## Complete Example

下面是一个完整示例：

```python
from jinja2 import Environment, FileSystemLoader

device = {
    "hostname": "R1",
    "loopback_ip": "1.1.1.1",
    "subnet_mask": "255.255.255.255"
}

environment = Environment(
    loader=FileSystemLoader("templates")
)

template = environment.get_template(
    "hostname.j2"
)

rendered_config = template.render(device)

with open(
    "output/R1.cfg",
    "w"
) as file:
    file.write(rendered_config)

print(rendered_config)
```

程序执行后控制台：

```
hostname R1

interface Loopback0
 ip address 1.1.1.1 255.255.255.255
```

同时 `output/R1.cfg` 也会被创建。

## Rendering Multiple Devices

结合 Chapter 5 的 Inventory，可以渲染多台设备。

例如：

```python
devices = [
    {
        "hostname": "R1",
        "loopback_ip": "1.1.1.1",
        "subnet_mask": "255.255.255.255"
    },
    {
        "hostname": "R2",
        "loopback_ip": "2.2.2.2",
        "subnet_mask": "255.255.255.255"
    }
]
```

然后：

```python
for device in devices:

    rendered_config = template.render(device)

    with open(
        f"output/{device['hostname']}.cfg",
        "w"
    ) as file:

        file.write(rendered_config)
```

最终：

```
output/

R1.cfg

R2.cfg
```

同一个 Template 自动生成多个 Configuration。Template 无需任何修改。

## Engineering Best Practices

企业项目中，建议遵循以下实践：

| Practice                             | Description             |
| ------------------------------------ | ----------------------- |
| Keep templates under `templates/`    | 所有模板统一集中管理。             |
| Keep generated files under `output/` | 渲染结果与模板分离。              |
| Render before deployment             | 先生成配置，再进行检查和部署。         |
| Reuse the same template              | 一个模板服务多个设备。             |
| Keep rendering code simple           | Python 负责协调流程，模板负责生成文本。 |

此外，在团队协作中，还建议：

- 模板文件只保存配置结构。

- Inventory 文件只保存设备数据。

- Python 程序只负责读取、渲染和写出结果。

这样能够保持整个自动化项目具有清晰的职责边界。

## Engineering Summary

渲染（Rendering）是 Template-Driven Automation 的核心步骤。Python 程序负责加载模板和准备数据，Jinja2 根据这些数据生成最终的配置文本，再将结果保存到配置文件中。

通过这一流程，我们实现了从结构化数据到设备配置的自动转换，而无需为每台设备单独编写 CLI。随着设备数量增加，只需扩展 Inventory，即可利用同一份模板生成大量一致、可维护的配置。

至此，本章已经完成了模板语言和渲染流程的介绍。下一节 7.9 Template Refactoring 将总结如何设计更易维护、更具复用性的企业级模板，对本章内容进行工程化整理，并形成一套统一的模板设计规范。