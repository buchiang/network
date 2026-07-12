# Chapter Objective

在前面的章节中，我们已经能够：

- 从 JSON 读取设备信息

- 从 YAML 读取配置参数

- 遍历 Inventory

- 批量连接设备

- 批量执行 Show Command

- 批量下发 Configuration

虽然已经能够自动化管理多台设备，但还有一个非常明显的问题：

>我们仍然需要手工编写每一份配置（Configuration）。

本节将回答本章最重要的第一个问题：

>Why do we need Templates?

## The Traditional Way

假设需要配置一台新的 Cisco IOSv Router。

最常见的方式是直接编写 CLI：

```
hostname R1

interface Loopback0
 ip address 1.1.1.1 255.255.255.255

router ospf 1
 router-id 1.1.1.1

network 1.1.1.1 0.0.0.0 area 0
```

这没有任何问题, 但是，当企业网络开始扩大时，情况就完全不同了。

例如100台 Router, 每台 Router：

- Hostname 不同

- Loopback 不同

- Router ID 不同

- Interface IP 不同

如果仍然采用手工方式，就必须维护大量几乎相同的配置。

例如：

R1：

```
hostname R1

interface Loopback0
 ip address 1.1.1.1 255.255.255.255
```

R2：

```
hostname R2

interface Loopback0
 ip address 2.2.2.2 255.255.255.255
```

R3：

```
hostname R3

interface Loopback0
 ip address 3.3.3.3 255.255.255.255
```
……

可以发现99%的配置完全一样。真正变化的只有几个字段。

## The Problem of Copy-and-Paste

很多工程师会采用下面的方法：

复制 ➡ 修改 ➡ 复制 ➡ 修改 ➡ 复制 ➡ 修改

看起来效率很高, 实际上这是大型网络中最容易引发错误的方式之一。

例如：

```
hostname R8

interface Loopback0
 ip address 7.7.7.7 255.255.255.255
```

这里忘记修改 Loopback 地址。

结果：Hostname：R8

但是：Loopback：7.7.7.7

这种错误在实际工程中非常常见。

复制配置时，一个字段遗漏修改，就可能导致：

- IP 地址冲突

- Router ID 重复

- OSPF 邻居无法建立

- BGP 邻居建立失败

- ACL 配置错误

- VLAN 编号错误

这些问题往往不是 CLI 语法错误，而是逻辑错误（Logical Errors），设备通常不会主动提示。

## Configuration Is Mostly Repetition

观察企业网络中的配置，会发现一个规律, 真正变化的内容很少。

例如：

hostname R1 只有 R1 发生变化。

接口配置：

```
interface GigabitEthernet0/0
description WAN
ip address 10.1.1.1 255.255.255.252
```

真正变化的是：10.1.1.1

OSPF：

```
router ospf 1
router-id 1.1.1.1
```

变化的是：1.1.1.1

BGP：

```
router bgp 65001
neighbor 10.0.0.2 remote-as 65002
```

变化的是：

- Neighbor IP

- AS Number

其它 CLI 完全一致。因此可以得到一个非常重要的工程观察

>网络配置的大部分内容是固定结构，只有少量参数会因设备而变化。

## Separating Structure from Data

既然配置结构基本固定只有数据不同, 那么最自然的工程思路就是不要重复写整个配置。而是把固定部分和变化部分分离。

例如不要写：

```
hostname R1
hostname R2
hostname R3
```

而是写：`hostname {{ hostname }}` 这里 `{{ hostname }}` 不是 Cisco CLI。

它表示将变量 hostname 的值插入到这里。

如果数据为：hostname = "R1", 生成：hostname R1

如果数据变成：hostname = "R2", 生成：hostname R2

同一个模板可以用于任意数量的设备。

## From Static Configuration to Templates

传统方式：

```
hostname R1
interface Loopback0

 ip address 1.1.1.1 255.255.255.255
```

模板方式：

```
hostname {{ hostname }}

interface Loopback0

 ip address {{ loopback_ip }} 255.255.255.255
```

然后准备数据：

```python
{
    "hostname": "R1",
    "loopback_ip": "1.1.1.1"
}
```

模板引擎（Template Engine）会自动生成：

```
hostname R1

interface Loopback0

 ip address 1.1.1.1 255.255.255.255
```

如果数据变成：

```python
{
    "hostname": "R25",
    "loopback_ip": "25.25.25.25"
}
```

同一个模板立即生成：hostname R25

```
interface Loopback0

 ip address 25.25.25.25 255.255.255.255
```

整个模板无需任何修改。

## Template-Driven Automation

回顾前几章，我们已经建立了这样的工程流程：

JSON / YAML ➡ Python Program ➡ Connect Device ➡ Deploy Configuration

现在，引入模板后，流程变为：

Structured Data ➡ Jinja2 Template ➡ Rendered Configuration ➡ Python Program ➡ Deploy Configuration

模板成为连接**结构化数据（Structured Data）与设备配置（Configuration）**之间的桥梁。

## Engineering Benefits

| Benefit                | Description          |
| ---------------------- | -------------------- |
| Reusability            | 一个模板可用于大量设备。         |
| Consistency            | 所有设备遵循统一的配置结构。       |
| Maintainability        | 修改模板即可影响所有生成的配置。     |
| Scalability            | 新增设备只需提供数据，无需重新编写配置。 |
| Reduced Human Error    | 避免复制粘贴导致的配置错误。       |
| Separation of Concerns | 模板负责结构，数据负责内容，职责清晰。  |

# Engineering Summary

模板并不是为了让配置“更炫”，而是为了**将固定结构与变化数据解耦**。

在企业网络中，配置的大部分内容具有高度重复性。模板通过把可变参数抽象为变量，使同一份配置结构能够适用于大量设备。这不仅减少了重复劳动，更重要的是降低了人为错误，提高了配置的一致性和可维护性。

从本节开始，Workbook 的自动化流程正式从 Data-Driven Automation 演进到 Template-Driven Automation。接下来的章节将使用 Jinja2 将结构化数据渲染（Render）为最终的 Cisco IOS 配置，实现真正意义上的自动生成网络配置。