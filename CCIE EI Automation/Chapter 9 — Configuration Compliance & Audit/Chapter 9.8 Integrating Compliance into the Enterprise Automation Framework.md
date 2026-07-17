到目前为止, 我们已经分别完成了 Chapter 8: Deployment Framework 以及 Chapter 9 Compliance Framework 现在的问题是企业是否会维护两个完全独立的 Automation Project？

答案通常是不会. 企业更倾向于维护一个统一的 Automation Platform, 其中包含多个独立的 Workflow. 

## 一个 Automation Platform

回顾 Chapter 8 的项目结构: 

```
automation_project/

├── inventory/
├── templates/
├── modules/
├── scripts/
├── logs/
```

Chapter 9 增加了: 

```
automation_project/

├── inventory/
├── templates/
├── modules/
│
│   connection.py
│   inventory.py
│   renderer.py
│   deployment.py
│
│   backup.py
│   parser.py
│   compliance.py
│
├── backups/
├── reports/
├── logs/
├── scripts/
```

可以看到我们没有重新创建 `compliance_project/` 而是在同一个工程中增加新的能力(Capability). 

## 为什么不用两个 Project？

假设 Deployment 需要: 

Inventory ➡ SSH Connection

Compliance 同样需要: 

Inventory ➡ SSH Connection

如果两个 Project 分别维护 connection.py 以后 SSH 登录方式修改. 需要修改两份代码. 

这是重复维护(Duplication). 而 Chapter 8 建立的 Framework 已经提供 Connection, Inventory, Logging, Exception Handling. Compliance 直接复用. 

这就是代码复用(Code Reuse). 

## Workflow, 而不是 Script

整个 Automation Platform 可以理解为: 

```
                Automation Platform

                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼

Deployment Workflow          Compliance Workflow
```

它们共享基础设施, 但是业务流程彼此独立. 

Deployment: Inventory ➡ Render ➡ Deploy

Compliance: Inventory ➡ ackup ➡ Parse ➡ Audit

互不影响. 

## Script 的职责

继续保持 Chapter 8 建立的规范. 

例如: 

```
scripts/

    deploy.py
    compliance.py
```

注意这里 Script 只是 Workflow 的入口(Entry Point). 

例如运行 `python3 -m scripts.deploy` 执行 Deployment Workflow. 

运行 `python3 -m scripts.compliance` 执行 Compliance Workflow. 

Script 本身不包含业务逻辑. 业务逻辑仍然全部放在 `modules/`

## 一个完整的 Compliance Script

整个流程实际上非常简单. 

Load Inventory ➡ onnect Device ➡ Backup Running Config ➡ Parse Config ➡ Run Compliance Rules ➡ Generate Report

可以看到 Script 更像一个 Coordinator(协调者). 它负责调用各个模块, 而不是实现每个模块. 

## 为什么这样设计？

继续回顾 Chapter 4 介绍过的 Single Responsibility Principle. 

Script 职责只有 Orchestrate

例如它知道先 Backup 再 Parser 最后 Compliance, 但是不知道 Backup 内部如何写文件, 也不知道 Parser 如何提取 Hostname. 

## Framework 的优势

假设半年后企业新增 DNS Compliance 我们无需修改 Deployment, 也无需修改 Parser. 只需要新增 `check_dns()` 然后加入 Workflow, Framework 整体保持稳定. 

再例如以后增加新的 Report 格式. 

例如 CSV 或者 JSON 

Compliance 无需修改, 因为 Business Logic 和 Presentation 已经分离. 

## 一个 Automation Platform 的成长

随着企业需求增加, Platform 可能逐渐变成: 

```
Automation Platform

    │
    ├── Deployment
    ├── Compliance
    ├── Backup
    ├── Audit
    ├── Reporting
    ├── Inventory Management
```

每一个都是独立 Workflow, 但是共享同一个 Framework, 这正是 Chapter 8 和 Chapter 9 想要建立的工程思想. 

## 我们故意没有加入什么？

截至目前, 我们没有加入 Automatic Remediation 原因不是不会, 而是企业通常不会让 Audit 直接修改设备. 

例如: Compliance ➡ 发现 NTP 不存在 ➡ 立即配置 NTP

这种设计风险非常高, 因此 Chapter 9 保持 Detect ➡ Report 结束. 

真正修改配置仍然属于 Deployment Workflow. 这也意味着 Deployment 和 Compliance 虽然共享平台, 但承担不同职责: 

- Deployment: 实施经过批准的配置变更. 

- Compliance: 持续检测网络是否符合企业标准. 

这种职责划分可以减少自动化带来的运维风险, 也更符合企业变更管理流程. 

## Chapter 9 的工程成果

经过本章,我们的 Automation Platform 已经拥有两条核心工作流: 

```
                Automation Platform

                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼

Deployment Workflow          Compliance Workflow

Generate Config             Collect Config

Render                      Backup

Deploy                      Parse

Verify                      Audit

                             Report
```

这是企业网络自动化平台最常见的基础形态. 

## 本节总结

本节完成了 Chapter 9 的最后一步: 

- Compliance Framework 被集成到现有 Automation Project, 而不是单独创建新的项目. 
- scripts/ 作为 Workflow 的入口, modules/ 作为业务逻辑的实现, 继续保持工程分层. 
- Deployment 与 Compliance 共享基础模块, 但保持职责独立. 
- Automation Platform 可以随着企业需求持续扩展新的 Workflow, 而不会破坏已有结构. 
- Chapter 9 坚持 Detect → Report 的设计边界, 不将自动修复混入 Audit 流程. 