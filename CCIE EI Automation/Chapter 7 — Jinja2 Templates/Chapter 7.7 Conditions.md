# Chapter Objective

上一节学习了 Loops（循环）

Loop 解决了-重复生成配置（Repeat Configuration Generation）但是，还有一种情况有些配置需要生成。有些配置不需要生成。

例如：

Branch Router 需要 router ospf 1

Data Center Router 可能运行 router bgp 65001

再例如：

某些 Interface 需要 shutdown

而另一些 Interface 需要 no shutdown

这种根据不同数据生成不同配置，就是 Conditions（条件）

## Why Conditions?

假设 Inventory：

```
hostname: R1

ssh_enabled: true
```

如果 SSH 已启用，Template 应生成：

```
ip domain name example.local

crypto key generate rsa modulus 2048

ip ssh version 2
```

如果 SSH 未启用：

```
hostname: R1

ssh_enabled: false
```

则这些配置完全不应该出现。因此 Template 必须具有 "是否生成配置" 的能力。

## The if Statement

Jinja2 使用 `{% if %}` 表示条件判断。

语法：

```
{% if condition %}

...

{% endif %}
```

例如：

```
{% if ssh_enabled %}
ip ssh version 2
{% endif %}
```

如果 `ssh_enabled = True`

Render：`ip ssh version 2`

如果 `ssh_enabled = False`

Render：`(empty)`

整个 Block 不会输出。

## if-else

很多时候，不仅需要生成或者不生成, 而是二选一。

例如Template：

```jinja2
{% if interface.enabled %}
 no shutdown
{% else %}
 shutdown
{% endif %}
```

如果 `enabled = True` 

Render：`no shutdown`

如果 `enabled = False`

Render：`shutdown`

因此同一个 Template，能够自动生成不同 Configuration。

## if-elif-else

对于多个条件，可以使用 elif

例如：

```jinja2
{% if routing_protocol == "ospf" %}

router ospf 1

{% elif routing_protocol == "bgp" %}

router bgp 65001

{% else %}

! Routing protocol not configured

{% endif %}
```

如果 `routing_protocol = "ospf"`

Render：`router ospf 1`

如果 `routing_protocol = "bgp"`

Render：`router bgp 65001`

如果：`routing_protocol = "none"`

Render：`! Routing protocol not configured`

这样 Template 可以根据不同数据，生成不同的配置内容。

## Comparison Expressions

上一节学习了 Expression。Condition 通常配合 Comparison。

例如：`{% if vlan_id == 100 %}` 或者 `{% if ospf_area != 0 %}` 也可以 {`% if interface.name == "Loopback0" %}`

Jinja2 支持常见比较运算：

| Operator | Meaning               |
| -------- | --------------------- |
| `==`     | Equal                 |
| `!=`     | Not Equal             |
| `>`      | Greater Than          |
| `<`      | Less Than             |
| `>=`     | Greater Than or Equal |
| `<=`     | Less Than or Equal    |

这些语法与 Python 保持一致。

## Combining Loops and Conditions

企业模板中，最常见的模式是 Loop, Condition。

例如：

```
{% for interface in interfaces %}

interface {{ interface.name }}

{% if interface.enabled %}
 no shutdown
{% else %}
 shutdown
{% endif %}

{% endfor %}
```

假设 Inventory：

```yaml
interfaces:

  - name: GigabitEthernet0/0
    enabled: true

  - name: GigabitEthernet0/1
    enabled: false
```

Render：

```
interface GigabitEthernet0/0
 no shutdown

interface GigabitEthernet0/1
 shutdown
```

Loop 负责遍历。Condition 负责决定输出。二者结合，构成了企业网络模板最常见的设计模式。

## Optional Configuration

很多企业配置都是 Optional。

例如：Description。

Template：

```jinja2
interface {{ interface.name }}

{% if interface.description %}
 description {{ interface.description }}
{% endif %}
```

如果 Inventory：description: WAN Link

Render：description WAN Link

如果 description 或者没有 Description。

Render：不会生成 description 这一行。

这样可以避免生成 空 Configuration。

## Keep Conditions Simple

例如推荐 `{% if interface.enabled %}`

不要：

`{% if interface.enabled and interface.ip and interface.mask and interface.description %}`

虽然 Jinja2 能够执行, 但是 Template 会越来越难维护。

企业工程建议复杂判断放在 Python。Template 负责最后一步 Configuration Rendering。

例如Python：

```python
render_data = {
    "render_interface": True
}
```

Template：

```jinja2

{% if render_interface %}
...
{% endif %}
```

这种方式更加清晰。

## Engineering Example

一个较完整的 Interface Template：

```jinja2
{% for interface in interfaces %}

interface {{ interface.name }}

{% if interface.description %}
 description {{ interface.description }}
{% endif %}

 ip address {{ interface.ip }} {{ interface.mask }}

{% if interface.enabled %}
 no shutdown
{% else %}
 shutdown
{% endif %}

{% endfor %}
```

对应 Inventory：

```yaml
interfaces:

  - name: GigabitEthernet0/0
    description: WAN
    ip: 10.1.1.1
    mask: 255.255.255.252
    enabled: true

  - name: GigabitEthernet0/1
    ip: 192.168.1.1
    mask: 255.255.255.0
    enabled: false
```

Render：

```
interface GigabitEthernet0/0
 description WAN
 ip address 10.1.1.1 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 ip address 192.168.1.1 255.255.255.0
 shutdown
```

可以看到 Template 完全没有修改, 不同的数据，自动生成不同配置。

## Engineering Guidelines

企业项目中，建议遵循以下原则：

| Guideline                                          | Description            |
| -------------------------------------------------- | ---------------------- |
| Use conditions only when configuration is optional | 条件判断主要用于控制可选配置的生成。     |
| Keep conditions readable                           | 条件表达式应简单、直观。           |
| Prefer Python for complex decisions                | 复杂业务逻辑放在 Python 中完成。   |
| Combine loops and conditions carefully             | 循环负责遍历，条件负责决定输出，职责清晰。  |
| Avoid hidden behavior                              | 模板中的条件应易于理解，不应包含复杂副作用。 |


Engineering Summary

条件（Conditions）使 Jinja2 模板能够根据不同的数据动态决定配置内容，是实现模板驱动自动化的重要组成部分。通过 `if`、`elif` 和 `else`，模板可以灵活处理可选配置、不同协议以及接口状态等场景，而无需维护多个相似的模板。

在企业工程中，循环和条件通常配合使用：循环负责遍历结构化数据，条件负责决定每个对象生成哪些配置。与此同时，应坚持将复杂业务逻辑保留在 Python 中，保持模板简单、清晰且易于维护。

下一节将进入 Rendering Templates，学习如何在 Python 程序中加载 `.j2` 模板、传入结构化数据，并生成最终的 Cisco IOS 配置文件。