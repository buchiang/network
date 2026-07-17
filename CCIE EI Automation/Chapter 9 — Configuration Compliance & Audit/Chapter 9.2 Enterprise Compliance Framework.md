上一节, 我们建立了 Compliance 的基本思想: 

>Deployment 不是自动化的终点. 

真正的企业自动化还需要持续验证网络是否仍然符合企业标准, 那么, 一个企业到底如何做 Compliance？

## 最容易想到的方法

很多初学者会想到: 

```python
output = connection.send_command("show running-config")

if "logging buffered" in output:
    print("PASS")
else:
    print("FAIL")
```

对于实验来说没有问题, 但是对于企业来说几乎不可维护. 

假设企业要求检查: 

```
Hostname
Banner
AAA
TACACS
SNMP
Syslog
NTP
SSH
OSPF
BGP
ACL
VLAN
QoS
VRF
Route-map
```

如果全部写成: 

```python
if ...

if ...

if ...

if ...

if ...
```

最后可能变成几千行代码, 这不是工程化. 

## 企业真正关注什么？

企业真正关心的不是: 如何写 if, 而是如何建立一个可以长期维护的 Compliance Framework. 

也就是说 Compliance 应该像 Deployment Framework 一样具有: 

- 可扩展

- 可维护

- 可测试

- 可复用

## Framework 思维

继续沿用 Chapter 8 的思想不要写: Automation Script

而要写: Automation Framework

所以: Compliance 也应该模块化. 

例如: 

```
modules/

    compliance.py

    parser.py

    backup.py
```

每个模块负责自己的职责. 为什么要先 Backup？很多人会问为什么 Compliance Framework 里面会出现 backup.py 原因很简单, Compliance 比较的对象是什么？

不是 SSH Session 真正比较的是 Running Configuration

所以第一步必须获得设备当前配置. 

例如: show running-config

然后: 保存下来. 

例如: 

```
backups/

    R1.cfg

    R2.cfg

    R3.cfg
```

这样以后所有模块都可以直接读取文件. 而不是每次重新 SSH. 

## 为什么企业喜欢 Backup？

这是一个非常重要的工程思想. 如果每一次检查都执行 `show running-config` 那么100台设备. 一天检查20次. 意味着2000次 SSH 很多都是重复工作. 

更合理的方法是: 

Collect Once ➡ Store ➡ Analyze Many Times

即: 

show running-config ➡ Backup ➡ Compliance ➡ Audit ➡ Diff ➡ Report

所有模块共享同一份配置. 

## Separation of Concerns

继续保持 Workbook 的设计原则. 

不要这样: 

SSH ➡ Compare ➡ Generate Report ➡ Backup ➡ Logging

全部放进一个函数, 而应该拆开. 

例如: 

Connection ➡ Backup ➡ Parser ➡ Compliance ➡ Report

每一个模块只负责一件事. Compliance Workflow

整个企业流程可以抽象为: 

```
Inventory
        │
        ▼
Connect Device
        │
        ▼
Collect Running Configuration
        │
        ▼
Save Backup
        │
        ▼
Load Baseline
        │
        ▼
Compare
        │
        ▼
Compliance Result
        │
        ▼
Generate Report
```

注意: 

这里已经出现: Load Baseline

也就是说企业一定要有: Baseline. 

否则不知道到底应该比较什么. 

## Baseline 在哪里？

这里很多新人容易误解. 

他们认为 Baseline 就是 `templates/` 其实不一定. 

例如 Chapter 8 Template: 

```
hostname {{ hostname }}

interface Loopback0

 ip address {{ loopback }}
```

这是: Deployment Template. 

Compliance 比较的是企业标准. 

例如: 

```
AAA

必须开启

----------------

Logging

必须开启

----------------

Banner

必须存在

----------------

NTP

必须配置

----------------

SSH Version

必须 Version 2
```

它们不是 Deployment Template. 而是 Enterprise Policy. 所以不要把 Template 和 Baseline 混为一谈. 

## Baseline 不一定是一整份配置

这是企业里另一个非常重要的概念. 

很多新人认为 Baseline 应该长这样: 

```
hostname R1

logging buffered 100000

snmp-server ...

ntp ...

router ospf ...

...
```

其实很多时候企业并不会维护一整份完整配置. 而是维护很多 Compliance Rules. 

例如: 

Rule 1: 必须开启 AAA

Rule 2: 必须配置 NTP

Rule 3: 必须存在 Banner

Rule 4: SNMP Community, 不能是 public

Rule 5: SSH Version, 必须 Version 2

这比维护几千行 Running Config 容易得多. 

## Compliance Rule

因此以后我们更多讨论的是 Compliance Rule 而不是 Configuration File. 

例如 Rule ➡ Check  ➡ PASS / FAIL

每条 Rule 互相独立. 以后新增100条 Rule. 不会影响前面99条. 这就是模块化. 

## 我们本章的实现方式

为了符合 Workbook 的循序渐进原则, 本章将采用一个逐步演进的设计: 

**第一阶段: **

使用一组简单的 Baseline Rules, 对设备配置进行检查, 理解 Compliance Workflow. 

**第二阶段: **

把这些检查封装到 compliance.py 中, 形成可复用的检查函数. 

**第三阶段: **

生成统一的 Audit Report, 并与 Chapter 8 的工程框架集成. 

这样可以在不引入后续章节(REST API, 数据模型等)的前提下, 完成一个具有企业工程风格的 Configuration Compliance Framework. 

## 本节总结

本节确立了 Configuration Compliance Framework 的工程设计原则: 

Compliance 是一个独立于 Deployment 的长期运行流程. 
配置采集(Backup)与配置分析(Compliance)应解耦, 实现 Collect Once, Analyze Many Times. 
`connection.py`, `backup.py`, `parser.py`, `compliance.py` 各司其职, 保持单一职责原则. 
Baseline 是企业标准, 不等同于 Jinja2 Deployment Template. 
企业更常维护的是一组 Compliance Rules, 而不是一份完整的标准配置. 

下一节, 我们将开始定义本 Workbook 的第一个 Enterprise Baseline, 并设计最基础的一组 Compliance Rules. 