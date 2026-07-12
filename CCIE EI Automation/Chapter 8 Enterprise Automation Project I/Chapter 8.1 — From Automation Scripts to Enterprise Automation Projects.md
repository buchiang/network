截至 Chapter 7，我们已经掌握了构建网络自动化所需的所有基础技术：

- Python

- Netmiko

- Inventory

- JSON / YAML

- Jinja2

现在需要回答一个新的问题：

>为什么企业不会直接运行一个 Python 脚本完成网络自动化？

**答案在于工程化（Engineering）。**

## 单个脚本能够完成任务吗？

假设我们已经完成了一个简单脚本：

inventory ➡ Jinja2 Render ➡ Netmiko Deploy

代码可能只有几十行, 运行 `python3 deploy.py` 所有设备完成配置。

对于 Lab 来说没有任何问题, 但是对于企业网络，很快就会暴露大量问题。

例如：

- 配置生成在哪里？

- 是否检查生成结果？

- 是否有人审核？

- 是否保存历史版本？

- 是否能够回滚？

- 是否知道哪些设备成功？

- 哪些设备失败？

- 是否记录日志？

- 是否能够重复执行？

一个脚本可以完成配置下发，但无法满足企业网络的运维要求。

## 企业关注的是整个流程（Process）

对于实验环境，我们关注的是：

>如何把配置发送到设备。

对于企业环境，更关注的是：

>配置是如何产生的？如何验证？如何部署？如何确认成功？如果失败怎么办？

因此，企业自动化的核心并不是某一个 Python 脚本，而是一套完整的执行流程。

可以将其抽象为：

Inventory ➡ Render Configuration ➡ Review ➡ Deploy ➡ Validate ➡ Archive

可以发现真正运行 Netmiko 的步骤，仅仅占整个流程中的一部分。

## Automation Pipeline

这种按照固定阶段执行的流程，称为-**Automation Pipeline**

Pipeline 表示整个自动化任务被拆分为多个独立阶段。

例如：

```
Stage 1
Load Inventory

↓

Stage 2
Render Templates

↓

Stage 3
Review Configuration

↓

Stage 4
Deploy Configuration

↓

Stage 5
Validate Results

↓

Stage 6
Archive Logs
```

每个阶段都有明确职责。

每个阶段：

输入固定 ➡ 处理固定 ➡ 输出固定

这样整个系统才容易维护。


## 为什么使用 Pipeline？

Pipeline 有几个重要优势。

1. 职责分离（Separation of Responsibilities）

不要让一个函数完成所有事情。

例如错误设计 `deploy()` 里面同时完成：

读取 Inventory ➡ 生成配置 ➡ SSH 登录 ➡ 发送配置 ➡ 验证 ➡ 日志 ➡ 保存文件

这样的函数可能超过几百行, 几乎无法维护。

正确设计：

`load_inventory()` ➡ `render_templates()` ➡ `deploy()` ➡` validate()` ➡ `archive_logs()`

每个函数只完成一件事情, 符合前面 Chapter 4 的 Single Responsibility Principle（单一职责原则）。

2. 容易测试（Testability）

假设今天 Template 出现错误, 如果整个程序只有一个 `deploy()` 很难知道错误发生在哪里。

而 Pipeline 可以快速定位：

Inventory ✓

Render ✗

Deploy 未开始

立即知道问题发生在 Render Stage。

3. 容易扩展（Scalability）

以后增加新的步骤, 例如：

Inventory ➡ Render ➡ Approval ➡ Deploy ➡ Validation

只需要增加一个新的 Stage, 原有代码几乎不用修改, 这就是模块化设计（Modular Design）的优势。

## Automation Project 与 Automation Script 的区别

二者最大的区别，不在于代码长度，而在于设计目标。

| Automation Script | Automation Project |
| ----------------- | ------------------ |
| 完成一次任务            | 支撑长期运维             |
| 通常几十行代码           | 多个模块协同             |
| 可以直接修改代码          | 数据与逻辑分离            |
| 面向个人              | 面向团队               |
| 可以没有日志            | 必须记录日志             |
| 可以人工检查            | 自动验证               |
| 通常没有回滚            | 需要具备回滚能力           |
| Lab 使用            | Production 使用      |

因此：

>企业真正维护的不是某一个脚本，而是一个完整的自动化项目（Automation Project）。

## Chapter 8 的总体架构

本章将逐步构建如下自动化流水线：

```
                 Inventory
                     │
                     ▼
             Load Device Data
                     │
                     ▼
          Render Jinja2 Templates
                     │
                     ▼
      Generate Device Configurations
                     │
                     ▼
              Dry Run (Optional)
                     │
                     ▼
          Deploy via Netmiko (SSH)
                     │
                     ▼
          Validate Deployment Results
                     │
                     ▼
              Save Logs & Outputs
```

这是一个典型的企业级 SSH 自动化流程，也是后续章节继续扩展（例如引入 API、自动化框架和 CI/CD）的基础。

## 本节小结

本节建立了 Chapter 8 的核心思想：

- 自动化脚本（Automation Script）解决的是“如何完成一个任务”。

- 自动化项目（Automation Project）解决的是“如何长期、稳定、安全地完成大量任务”。

- 企业自动化采用 Automation Pipeline，将流程划分为多个职责清晰的阶段。

- Chapter 8 将基于前七章的知识，构建第一个端到端（End-to-End）的企业级自动化项目，而不会引入 Chapter 9 及之后的技术。