前面的 Pipeline 中, 我们故意预留了一个重要阶段: 

Render ➡ Save Configuration ➡ SDry Run ➡ Deploy

很多初学者会认为 Render 完以后, 直接 send_config_set() 就可以了. 对于实验环境(Lab), 这样做通常没有问题, 但是在生产环境(Production), 直接部署是一种高风险操作. 因此, 大多数企业都会提供 Dry Run 机制. 

## 什么是 Dry Run？

Dry Run 的含义是: 

>>完整执行自动化流程, 但不对设备做任何修改. 

也就是说 Pipeline 可以完成 

Load Inventory ➡ Validate Inventory ➡ Render Templates ➡ Save Configurations ➡ Review Output

但是不会执行 `send_config_set()` 因此设备配置保持完全不变. 

## Dry Run 能发现什么问题？

假设: 

```json
Inventory: 

{
    "hostname": "R1",
    "loopback_ip": "1.1.1.100"
}
```

Template: 

```jinja2
hostname {{ hostname }}

interface Loopback0
 ip address {{ loopback_ip }} 255.255.255.255
```

Render 后得到: 

```
hostname R1

interface Loopback0
 ip address 1.1.1.100 255.255.255.255
```

如果工程师发现应该使用 Loopback100 那么问题在 Template, 并不是 Deploy. 此时修改模板即可. 整个网络没有任何设备受到影响. 

## Dry Run 不只是打印配置

很多初学者会写 `print(config)` 认为这就是 Dry Run. 

实际上企业中的 Dry Run 往往包括: 

- Render Configuration

- 保存配置文件

- 检查 Inventory

- 检查模板变量

- 检查输出目录

- 生成执行计划

- 输出部署摘要

只是不会真正连接设备. 因此 Dry Run 是一次完整的模拟执行. 

## Dry Run 在 Pipeline 中的位置

Dry Run 一定发生在 Render 完成之后. 

例如: 

Inventory ➡ Validation ➡ Render ➡ Save Output ➡ Dry Run ➡ Deploy

为什么？因为 Dry Run 需要检查最终生成的配置. 如果还没有 Render, 根本无法确认将要部署什么内容. 

## Dry Run 的输出

一个企业自动化项目, 通常会输出: 

```
========== Deployment Summary ==========

Devices:

R1

R2

R3

----------------------------------------

Configuration Files

output/R1.cfg

output/R2.cfg

output/R3.cfg

----------------------------------------

Mode

DRY RUN

----------------------------------------

Deployment

SKIPPED
```

从这里可以清楚知道: 

- 有哪些设备

- 生成了哪些配置

- 当前运行模式

- 是否真正部署

这样的输出比简单打印配置更适合生产环境. 

## 为什么 Dry Run 如此重要？

假设需要修改300台交换机. 如果直接部署: 

Inventory ➡ Deploy

一旦 Template 出现错误. 300台设备都会受到影响. 而增加 Dry Run

Inventory ➡ Render ➡ Dry Run ➡ Engineer Review ➡ Deploy

整个风险大幅降低. 很多企业要求所有自动化部署, 必须先完成 Dry Run. 经过审核(Review)之后, 才能执行正式部署. 

## Dry Run 与 Review

Dry Run 和人工 Review 经常配合使用. 

例如: 

Render ➡ Generate Configurations ➡ Dry Run ➡ Engineer Review ➡ Deploy

Review 时工程师主要关注: 

- Hostname 是否正确

- Interface 是否正确

- IP 地址是否正确

- Routing Protocol 是否正确

- 是否遗漏配置

- 是否出现多余配置

注意 Review 的对象是 Render 后的配置文件. 不是 Jinja2 Template. 因为最终部署的是生成后的配置. 

## Lab 与 Production 的区别

很多人在 Lab 中 Edit Template ➡ Deploy ➡ Done 这是学习阶段常见的流程. 

企业环境通常采用: 

Edit Template ➡ Render ➡ Dry Run ➡ Review ➡ Deploy ➡ Validate ➡ Archive

虽然步骤更多, 但能够显著降低生产网络中的变更风险. 

## 工程经验

一个成熟的自动化系统通常会提供两种运行模式: 

```
Mode 1

DRY RUN
```

用于: 

- 验证模板

- 检查 Inventory

- 生成配置

- 人工审核

以及: 

```
Mode 2

DEPLOY
```

用于: 

- 建立 SSH 连接

- 下发配置

- 执行验证

- 记录日志

两种模式共享同一条 Pipeline, 唯一的区别在于是否执行 Deployment Stage. 这种设计既避免了代码重复, 又能保证测试环境和生产环境使用相同的流程. 

## 本节小结

本节介绍了企业自动化中非常重要的 Dry Run 机制, 并建立了以下原则: 

- Dry Run 是一次完整的模拟执行, 不会修改任何设备. 

- Dry Run 位于 Render 之后、Deploy 之前. 

- Dry Run 不仅仅是打印配置, 还应完成配置生成、保存、检查和部署摘要等工作. 

- Dry Run 与人工 Review 配合, 可以在部署前发现大多数配置错误. 

- 企业项目通常提供 DRY RUN 和 DEPLOY 两种运行模式, 共享同一 Pipeline, 仅在是否执行部署阶段有所区别. 

下一节将继续完善企业自动化流程, 讨论 Deployment Control(部署控制), 包括如何控制部署顺序、处理失败设备, 以及保证整个部署过程具有可预测性和可恢复性. 