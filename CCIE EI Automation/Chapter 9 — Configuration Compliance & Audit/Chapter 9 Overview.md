```
automation_project/

│
├── inventory/
│
├── templates/
│
├── modules/
│
│    connection.py
│    inventory.py
│    renderer.py
│    compliance.py     ← 新增
│    backup.py         ← 新增
│    parser.py         ← 新增
│
├── backups/
│
├── reports/
│
├── logs/
│
└── scripts/
```

模块职责单一(Single Responsibility). 

例如: 

connection.py 只负责 SSH

renderer.py 只负责 Jinja2

compliance.py 只负责 Compliance

以后不会混合. 

## Chapter 9 Learning Goal

截至 Chapter 8, 我们已经能够: 

- 自动生成配置

- 自动部署配置

- 自动管理 Inventory

- 构建企业级 Automation Framework

但是企业自动化还有一个关键问题如何确认网络始终保持在期望状态(Desired State)？

现实中, 设备配置会不断发生变化: 

- 工程师临时修改配置

- 故障处理后的遗留变更

- 手工配置遗漏

- 配置不一致

- 安全策略漂移(Configuration Drift)

因此, 仅能**部署(Deployment)**是不够的, 还必须能够: 

- 收集设备配置(Collect)

- 与企业 Baseline 比较(Compare)

- 识别 Configuration Drift

- 生成 Compliance Report

- 为后续整改提供依据

这就是 Configuration Compliance & Audit 的核心目标. 

Chapter 9 Objectives

完成本章后, 你将能够: 

- 理解 Desired State 与 Configuration Drift 的概念

- 建立企业 Baseline Configuration

- 自动采集设备配置

- 编写可复用的 Compliance 检查模块

- 比较实际配置与标准配置

- 自动生成 Audit Report

- 将 Compliance 功能集成到现有 Automation Framework 中

- 构建一个企业级 Configuration Audit Workflow

本章仍将完全基于前八章已经建立的 Python, Netmiko, YAML, Jinja2 与工程化框架, 不提前引入 Chapter 10 及之后的任何技术. 