# Chapter Objective

上一节介绍了 Control Structures（控制结构）控制结构让 Template 开始具有流程控制能力, 但是，目前仍然存在一个问题。

例如Router 有：

```
Loopback0
Loopback1
Loopback2
Loopback3
```

如果手工编写：

```
interface Loopback0
 ip address ...

interface Loopback1
 ip address ...

interface Loopback2
 ip address ...

interface Loopback3
 ip address ...
```

可以发现大量 Configuration 完全重复。真正变化的只有：

```
Interface Name
IP Address
```

这正是 Loop（循环） 要解决的问题。

## Why Loops?

假设 Inventory 中保存了一台设备的接口信息：

```python
interfaces = [
    {
        "name": "GigabitEthernet0/0",
        "ip": "10.1.1.1",
        "mask": "255.255.255.252"
    },
    {
        "name": "GigabitEthernet0/1",
        "ip": "10.2.2.1",
        "mask": "255.255.255.252"
    },
    {
        "name": "Loopback0",
        "ip": "1.1.1.1",
        "mask": "255.255.255.255"
    }
]

```
如果不用 Loop，只能写三遍 interface ... ip address ..., 如果有100 接口，就需要写100 次。显然这不是企业自动化希望看到的方式。

## The for Statement

Jinja2 使用 `{% for ... in ... %}` 表示遍历一个集合（Collection）。

语法：

```
{% for item in items %}

...

{% endfor %}
```

可以发现与 Python `for item in items:` 几乎完全一致。只是 Python 使用 `:` 结束。Jinja2 使用 `{% endfor %}` 结束。

## First Loop Example

假设Python：

```python
interfaces = [
    "GigabitEthernet0/0",
    "GigabitEthernet0/1",
    "Loopback0"
]
```

Template：

```jinja2
{% for interface in interfaces %}
interface {{ interface }}
{% endfor %}
```

Render：

```
interface GigabitEthernet0/0

interface GigabitEthernet0/1

interface Loopback0
```

可以发现 Template 只有一份。输出可以有很多份。

## Looping Through Dictionaries

企业网络中，通常不会只保存 Interface Name。而是保存多个属性。

例如：

```python
interfaces = [
    {
        "name": "GigabitEthernet0/0",
        "ip": "10.1.1.1",
        "mask": "255.255.255.252"
    },
    {
        "name": "Loopback0",
        "ip": "1.1.1.1",
        "mask": "255.255.255.255"
    }
]
```

Template：

```jinja2
{% for interface in interfaces %}
interface {{ interface.name }}
 ip address {{ interface.ip }} {{ interface.mask }}

{% endfor %}
```

Render：

```
interface GigabitEthernet0/0
 ip address 10.1.1.1 255.255.255.252

interface Loopback0
 ip address 1.1.1.1 255.255.255.255
```

这里 interface.name 表示 Dictionary 中 "name" 对应的值。

>**说明：**
>在 Jinja2 中，interface.name 与 interface["name"] 都可以访问字典键。为了提高模板可读性，本 Workbook 后续统一采用点表示法（Dot Notation）。

## Loop Variables

在 `{% for interface in interfaces %}` 中 interfaces 表示整个列表（List）。而 `interface` 表示当前正在遍历的元素。

例如：

第一次：

```
interface =
{
    "name":"GigabitEthernet0/0",
    ...
}
```

第二次：

```
interface =
{
    "name":"Loopback0",
    ...
}
```

每一次循环，变量 interface 都会自动变化。因此同一个 Template，能够自动生成多个 Interface Configuration。

## Rendering Multiple Routes

Loop 不仅可以生成 Interface。

例如Inventory：

```python
static_routes = [
    {
        "network": "192.168.10.0",
        "mask": "255.255.255.0",
        "next_hop": "10.1.1.2"
    },
    {
        "network": "192.168.20.0",
        "mask": "255.255.255.0",
        "next_hop": "10.2.2.2"
    }
]
```

Template：

```jinja2
{% for route in static_routes %}
ip route {{ route.network }}
         {{ route.mask }}
         {{ route.next_hop }}
{% endfor %}
```

Render：

```
ip route 192.168.10.0 255.255.255.0 10.1.1.2

ip route 192.168.20.0 255.255.255.0 10.2.2.2
```

可以发现 Loop 可以生成任意数量：

- Interface

- Static Route

- VLAN

- ACL Entry

这正是 Template 最大的价值。

## Empty Collections

如果 `interfaces = []` 即没有任何接口。

那么：

```jinja2
{% for interface in interfaces %}
...
{% endfor %}
```

不会报错, 也不会输出任何内容。

Render：(empty) 

这是 Jinja2 默认行为。

因此 Loop 对空列表（Empty List）也是安全的。

不过，在企业项目中，仍建议在数据准备阶段验证关键数据是否为空，而不要依赖模板静默跳过必须生成的配置。

## Keep Loops Focused

虽然 Loop 可以写得非常复杂。

例如：

```jinja2
{% for interface in interfaces %}
...
{% endfor %}
```

里面再：

If ➡ For ➡ If ➡ For ➡ ……

Jinja2 都支持, 但是企业项目通常建议一个 Loop 完成一个任务。

例如：

Interface 一个 Loop。

Static Route 一个 Loop。

ACL 一个 Loop。

不要所有内容全部放到一个巨大 Loop。这样 Template 更容易阅读, 也更容易维护。

## Engineering Example

一个典型的企业 Template：

```jinja2
hostname {{ hostname }}

{% for interface in interfaces %}
interface {{ interface.name }}
 description {{ interface.description }}
 ip address {{ interface.ip }} {{ interface.mask }}
 no shutdown

{% endfor %}
```

可以配合任何 Inventory：

```yaml
hostname: Branch01

interfaces:
  - name: GigabitEthernet0/0
    description: WAN
    ip: 10.1.1.1
    mask: 255.255.255.252

  - name: GigabitEthernet0/1
    description: LAN
    ip: 192.168.1.1
    mask: 255.255.255.0
```

Render：

```
hostname Branch01

interface GigabitEthernet0/0
 description WAN
 ip address 10.1.1.1 255.255.255.252
 no shutdown

interface GigabitEthernet0/1
 description LAN
 ip address 192.168.1.1 255.255.255.0
 no shutdown
```

整个 Template 没有任何修改。只是 Inventory 发生变化。

## Engineering Guidelines

企业项目中，建议遵循以下原则：

| Guideline                               | Description                                 |
| --------------------------------------- | ------------------------------------------- |
| Loop over structured data               | 循环应基于结构化数据（如 List of Dictionaries）。         |
| Keep one purpose per loop               | 每个循环只负责一种配置对象。                              |
| Use meaningful loop variable names      | 使用具有业务含义的循环变量，如 `interface`、`route`、`vlan`。 |
| Avoid deep nesting                      | 避免多层嵌套循环，提高可读性。                             |
| Validate required data before rendering | 对必须存在的数据，在 Python 或 Inventory 校验阶段完成验证。     |


Engineering Summary

循环（Loops）使 Jinja2 模板能够根据结构化数据自动生成重复的配置内容，是模板驱动自动化中最重要的能力之一。通过 for 语句，模板可以遍历接口、静态路由、VLAN 等任意数量的数据对象，而无需重复编写相同的配置结构。

在企业工程中，应优先使用结构化数据 + 简洁循环的设计方式，将一个循环对应一种配置对象，并保持模板层次清晰。这样既提高了模板的复用性，也降低了后期维护的复杂度。

下一节将学习 Conditions（条件），介绍如何根据不同设备的数据动态决定哪些配置需要生成，哪些配置应该被省略。