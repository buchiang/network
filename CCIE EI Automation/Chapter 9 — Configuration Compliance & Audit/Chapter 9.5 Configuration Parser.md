上一节, 我们已经能够: 

```
Device
    │
    ▼
Collect Running Configuration
    │
    ▼
Save Backup (.cfg)
```

现在的问题来了. 

假设 R1.cfg 

```
hostname R1

service password-encryption

ip ssh version 2

logging buffered 100000

ntp server 10.1.1.1

banner motd ^
Authorized Access Only
^

interface GigabitEthernet0/0

 ip address 10.1.1.1 255.255.255.0
```

Compliance Module 如何知道 NTP 有没有？

最容易想到的方法很多人第一反应

```python
if "ntp server" in config:
    PASS
```

或者

```python
if "hostname" in config:
    PASS
```

对于实验来说完全可以, 但是企业不会直接这样写. 原因不是不能工作, 而是没有可维护性. 

## Parser 的职责

因此继续保持模块化. 

新增: 

```
modules/

    parser.py
```

Parser 只有一个职责从配置中提取需要的信息. 

它不负责: 

- SSH

- Backup

- Compliance

- Report

## Parser 在整个 Workflow 中的位置

整个流程现在变成: 

```
Device

    │
    ▼

Backup

    │
    ▼

Configuration File

    │
    ▼

Parser

    │
    ▼

Parsed Data

    │
    ▼

Compliance
```

注意 Compliance 不再直接读取配置文件, 而是读取 Parser 的结果. 

## 为什么需要 Parser？

假设以后 Compliance 需要 Hostname. 如果没有 Parser, 每条 Rule 都会自己打开 R1.cfg 然后自己搜索 hostname 几十条 Rule 全部重复相同工作. 

有了 Parser 流程变成: 

Parser ➡ Hostname ➡ Compliance Rule

以后任何 Rule 都直接调用 Parser. 

## Parser 可以理解成什么？

可以理解成一个翻译器. 

输入: 

```
hostname R1

ip ssh version 2

logging buffered 100000

ntp server 10.1.1.1
```

输出: 

```
----------------
Hostname ➡ R1
----------------
SSH Version ➡ 2
----------------
Logging ➡ Enabled
----------------
NTP ➡ Configured
----------------
```

Compliance 不用关心 Cisco CLI. 只关心结果. 

## 第一版 Parser

本 Workbook 保持简单. 

第一版 Parser 只做最基础事情. 

例如提供 `load_configuration()`

负责读取 R1.cfg

再提供 `find_line()`

负责搜索 hostname

例如: `find_line(config, "hostname")`

返回: `hostname R1`

如果没有返回 None 这样所有 Rule 统一使用. 

## 为什么不是 Regex？

很多教材这里马上开始 Regex. 

例如 `re.search(...)` 当然 Regex 很强, 但是本章不会使用.

原因不是 Regex 不好, 而是 Workbook 遵循渐进复杂度(Progressive Complexity). 

目前我们先建立 Framework. 不是学习字符串解析技巧. 因此第一版 Parser 使用 Python 已经学过的 

```python
startswith()

in

split()
```

即可. 以后如果 Parser 越来越复杂再升级. 

## Parser 应该返回什么？

这里很多新人容易犯一个错误. 

例如 Parser 直接打印 `Hostname Found` 这样 Compliance 无法使用.

Parser 应该返回数据. 

例如 `hostname = parser.get_hostname(config)` 返回 "R1" 而不是 `Hostname is R1`

这是 Library 和 Script 最大的区别. 

## Parser 是一个 Library

继续保持 Chapter 4 工程思想, 不要 `print(...)` 而是 `return ...`

例如: 

```python
def get_hostname(config):

    ...

    return hostname
```

以后 Compliance 决定如何使用. 

## Parser 不判断 PASS 或 FAIL

例如 Parser 发现 hostname R1 它不会说 PASS 因为 Parser 不知道企业要求什么. 

例如有的企业要求 hostname 必须 CORE-R1 有的企业要求 R1. Parser 不应该知道 Policy. 它只负责告诉你配置里面是什么,因此职责严格分离. 

```
Parser

↓

Extract Data

Compliance

↓

Evaluate Data
```

这是整个 Framework 最重要设计之一. 

## 一个完整的例子

例如配置: 

```
hostname R1

ip ssh version 2
```

Parser 返回: 

```
hostname = "R1"

ssh_version = "2"
```

Compliance 再比较: 

Expected ➡ 2

Actual ➡ 2

结果 PASS 如果 Parser 没有找到 `ip ssh version` 返回 `None`. 

Compliance 得到: 

Expected ➡ 2

Actual ➡ None

结果 FAIL

注意 **FAIL 是 Compliance 做出的判断, 不是 Parser. **

## 为什么这种设计可以长期扩展？

假设以后新增100条 Rule. 

例如检查: 

- OSPF Router ID

- BGP Neighbor

- TACACS Server

- SNMP Community

- Syslog Host

Parser只需要增加新的 `get_xxx()`, Compliance 不用修改已有代码. 反之如果企业修改 Baseline. 

例如: 

SSH 由 Version 2 改成 Version 3(假设未来存在), Parser 完全不用改. 只修改 Compliance Rule. 

这就是: 

高内聚(High Cohesion)

低耦合(Low Coupling)

## 本节总结

本节建立了 Configuration Parser 的设计原则: 

- parser.py 负责从配置文件中提取数据, 而不是进行 Compliance 判断. 

- Parser 是一个可复用的 Library, 应返回数据, 而不是打印结果. 

- Compliance 基于 Parser 返回的数据进行 PASS / FAIL 判断, 实现职责分离. 

- 第一版 Parser 使用基础字符串处理方法, 不引入正则表达式, 保持 Workbook 的渐进学习路线. 

- Parser 与 Compliance 解耦后, 可以分别扩展解析能力和企业策略, 而互不影响. 