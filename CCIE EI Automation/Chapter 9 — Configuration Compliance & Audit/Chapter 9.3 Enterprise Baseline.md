上一节，我们已经知道 Compliance 的依据不是设备当前配置，而是 Enterprise Baseline 那么企业到底如何定义 Baseline？

## 什么是 Baseline？

可以把 Baseline 理解为

>企业批准的一套最低标准（Minimum Standard）。

注意这里是 Minimum Standard 而不是 Ideal Configuration（理想配置）。

例如企业可能有很多型号设备：

- Catalyst 9300

- Catalyst 9500

- ISR 4431

- ASR 1001

- CSR1000v

它们配置不可能完全一样。所以企业不会要求所有设备 Running Config 完全一致。

企业真正要求的是所有设备必须满足某些共同标准。

例如：

- 必须开启 AAA

- 必须配置 NTP

- 必须开启 Logging

- 必须配置 Banner

- 必须启用 SSHv2

这些就是 Baseline。

## Baseline 与 Device Role

另一个重要概念不同角色（Role）的设备 Baseline 可能不同。

例如：

Core：OSPF, BGP, MPLS

Access：STP, VLAN, Port Security

WAN：BGP, IP, SLA DMVPN

因此企业通常不会只有一个 Baseline, 而是：

- Core Baseline

- Access Baseline

- Distribution Baseline

- WAN Baseline

每种设备都有自己的标准。

## 本 Workbook 的范围

为了聚焦于 Configuration Compliance 的核心思想，本章暂时不引入按设备角色分类的 Baseline。

整个实验环境使用一套统一的 Enterprise Baseline，便于理解 Compliance Workflow。

在真实企业中，这套 Baseline 往往会根据设备角色、操作系统、站点等进一步细分。

## 一个简单的 Enterprise Baseline

本章先建立第一版 Enterprise Baseline。

例如：

| Category                    | Requirement  |
| --------------------------- | ------------ |
| Hostname                    | 必须存在         |
| Banner                      | 必须存在         |
| Logging                     | 必须开启         |
| NTP                         | 必须配置         |
| SSH                         | 必须 Version 2 |
| Service Password Encryption | 必须开启         |


注意这些都是企业策略。不是 Cisco 要求。

为什么选择这些？因为它们具有几个特点

第一, 几乎所有企业都会配置。

第二, 容易理解。

第三, 容易验证。

第四, 不依赖拓扑。

例如检查 hostname 无需知道网络结构, 检查 banner motd 同样如此。

因此非常适合作为第一批 Compliance Rules。

## Compliance Rule 长什么样？

可以抽象成：

Rule ➡ Expected State ➡ Actual State ➡ PASS / FAIL

例如：

Rule：Hostname

Expected：必须存在 hostname

Actual：hostname R1

结果：PASS

再例如：

Rule：NTP

Expected：必须存在

Actual：没有任何 ntp server

结果：FAIL

再例如：

Rule：SSH Version

Expected：ip ssh version 2

Actual：ip ssh version 1

结果：FAIL

## Compliance Rule 应该尽量独立

例如不要写：

```
AAA

AND

NTP

AND

Banner

AND

Logging
```

作为一个 Rule, 应该拆开：

```
Rule 1
AAA

Rule 2
Logging

Rule 3
Banner

```

这样任何一条失败, 都不会影响其它 Rule。

## 为什么企业喜欢独立 Rule？

假设今天新增 SNMP 如果 Rule 全部耦合, 需要修改巨大函数风险很高。而如果每条 Rule 独立, 只需要增加 `check_snmp()` 整个系统无需改动。

这就是 Open-Closed Principle（开放-封闭原则）在工程中的体现

>对扩展开放，对修改关闭。

我们的 Compliance Framework 也会遵循这一原则。

## Rule 不一定只有 PASS

很多新人认为 Compliance 只有 PASS, FAIL

实际上企业通常还有 PASS, FAIL, WARNING, NOT APPLICABLE

例如某设备没有 BGP, 那么检查 neighbor password 可能就是 Not Applicable 而不是 FAIL。

不过为了保持 Workbook 的渐进学习路线, 本章统一使用 PASS, FAIL. 以后再逐步扩展。

## Rule 的输出

企业最终关心的是 Report。

例如：

```
Device: R1

Hostname ........ PASS

Banner .......... PASS

Logging ......... PASS

NTP ............. FAIL

SSH ............. PASS

Encryption ...... PASS
```

一眼就知道哪里不符合标准。以后几十条 Rule也仍然保持相同格式。

因此 Rule 必须标准化。

## Baseline 应该稳定

企业还有一个原则不要今天必须开启 AAA 明天可以不开。这样 Compliance 每天都会变化。

因此 Baseline 必须经过审批。

例如：

Architecture Team ➡ Security Team ➡ Approved ➡ Baseline

Automation 只是执行 Baseline。Automation 不是制定 Baseline。

这也是企业自动化中一个非常重要的职责边界：

- Architecture / Security Team 定义标准（What should the network look like?）

- Automation Team 实现标准（How do we verify and enforce it?）

Automation Framework 不应自行决定企业策略，而应忠实地执行已经批准的 Baseline。

## 本章中的 Baseline

为了保持整个 Workbook 的实验一致性，我们将使用如下 Baseline：

| Rule                | Expected                         |
| ------------------- | -------------------------------- |
| Hostname            | 存在 `hostname`                    |
| Banner              | 存在 `banner motd`                 |
| Logging             | 存在 `logging buffered`            |
| NTP                 | 至少存在一个 `ntp server`              |
| SSH                 | 存在 `ip ssh version 2`            |
| Password Encryption | 存在 `service password-encryption` |

这套 Baseline 足以支撑我们完成整个 Compliance Framework 的设计与实现。

## 本节总结

本节建立了 Enterprise Baseline 的设计原则：

- Baseline 是企业批准的最低标准，而不是设备当前配置。

- Baseline 可以按设备角色分类，但本章采用统一 Baseline 简化学习。

- 每条 Compliance Rule 应保持独立，遵循开放-封闭原则，便于扩展。

- Compliance Report 是所有 Rule 的统一输出形式。

- Automation 的职责是执行 Baseline，而不是制定 Baseline。