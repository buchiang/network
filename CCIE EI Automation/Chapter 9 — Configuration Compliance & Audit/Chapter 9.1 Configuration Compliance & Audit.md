## 为什么企业需要 Configuration Compliance

在前面的章节中, 我们已经完成了整个自动化流程: 

Inventory ➡ YAML Variables ➡ Jinja2 Template ➡ Generated Configuration ➡ Deployment ➡ Network Device

这是一个单向流程(One-way Automation). 也就是说 Automation 可以把配置发送到设备, 但是, 一个真正的企业网络不会停留在部署完成的那一刻. 

Deployment 只是开始, 很多初学者会认为自动部署完成, 就说明自动化完成了. 实际上, 企业网络的生命周期更像这样: 

Design ➡ Generate Configuration ➡ Deploy ➡ Operate ➡ Audit ➡ Fix Drift ➡ Repeat

真正占据大部分时间的是 Operate.  

一家大型企业的网络可能连续运行5年, 10年, 15年, 每天都会有人: 

- 登录设备

- 修改配置

- 修复故障

- 更换硬件

- 增加 VLAN

- 修改 ACL

- 调整 OSPF

- 修改 BGP

因此部署完成后的配置, 并不会一直保持不变. 

企业里的一个真实例子

例如最初通过 Automation 部署: 

```
hostname R1

logging buffered 100000

ntp server 10. 1. 1. 1

snmp-server community COMPANY RO

banner motd
Authorized Access Only
```

一周后, 某位工程师为了排障: 

```
conf t

no logging buffered

end
```

然后忘记恢复, Automation 并不会知道 `Logging` 已经被删掉了. 

又过了一周, 另一位工程师: 

```
conf t

snmp-server community public RO
```

结果 Company ➡ public 企业安全策略已经违反, 但是没人知道. 

再过两个月, 又有人 `hostname Router-1`

于是 Inventory: hostname: R1, 设备: hostname Router-1

Automation Framework 已经开始出现混乱, 这就是 Configuration Drift. 

## Configuration Drift

定义: 

>Configuration Drift 是设备实际配置逐渐偏离企业期望配置(Desired State)的过程. 

例如最初: 

```
router ospf 1
 network 10. 0. 0. 0 0. 255. 255. 255 area 0
```

后来: 

```
router ospf 100
 network 10. 0. 0. 0 0. 255. 255. 255 area 0
```

Deployment 从未再次运行, 但是设备已经变了. Automation Project 不知道. 

再例如: 

Baseline `service password-encryption`

设备 `no service password-encryption`

又是 Drift. 

再例如: 

Baseline `logging host 10. 1. 1. 10`

设备 `logging host 10. 1. 1. 20`

依然属于 Drift. 

## Desired State

Configuration Compliance 的核心就是: 

>Desired State(期望状态)

可以理解成: 

>企业希望所有设备最终都符合的一套标准. 

例如: 

```
hostname

AAA

NTP

Logging

Banner

SNMP

Loopback

Routing

Syslog

SSH
```

Desired State 可以来自: 

```
Enterprise Standards

Security Policy

Design Document

Change Management

Architecture
```

而不是来自-设备当前配置.  这一点非常重要. 

## 一个错误的理解

很多新人会说 "设备现在就是这样." 

所以 Running Configuration = Standard

这是错误的, 正确的是: 

Enterprise Standard ➡ 决定 ➡ Running Configuration

而不是: 

Running Configuration ➡ 决定 ➡ Enterprise Standard

也就是说

>企业标准永远高于设备当前状态. 

## Compliance 的目标

Compliance 并不是让配置一样. 而是判断设备是否符合企业标准. 

因此: 

Compliance 实际上是在回答一个问题: 

>Does this device comply with our standard?

而不是: 

>Does this configuration look reasonable?

这是两个完全不同的问题. 

一个简单的 Compliance 流程

整个过程可以抽象成下面的流程: 

```
Enterprise Baseline
          │
          ▼
Collect Device Configuration
          │
          ▼
Parse Configuration
          │
          ▼
Compare
          │
          ▼
Compliance Result
          │
          ├──────── PASS
          │
          └──────── FAIL
```

请注意: 本章我们首先关注检测(Detect). 

对于检测出的问题如何自动修复(Remediation), 属于后续自动化能力的扩展, 不会在本章展开, 以保持与 Workbook 的 Roadmap 一致. 

## 本节总结

本节建立了 Chapter 9 的核心思想: 

- Deployment 负责将配置下发到设备. 

- Compliance 负责验证设备是否仍符合企业标准. 

- Configuration Drift 是企业网络中持续存在的现实问题. 

- Desired State 是所有 Compliance 检查的依据, 而不是设备当前配置. 

- 企业自动化是一个持续循环的过程: Deploy → Operate → Audit → Correct → Repeat. 

下一节, 我们将开始设计整个 Configuration Compliance Framework, 把它集成到前一章已经构建好的企业级 Automation Framework 中, 而不破坏现有模块化结构. 