经过 Chapter 2，我们已经具备了 Python 基础能力。

现在开始真正进入 Network Automation。

从这一章开始，我们写的每一行代码，都将连接真实 Cisco Router，而不是学习 Python 语法。

本章结束后，你将能够完成一个企业级 SSH 自动化项目，实现：

- SSH 登录 Cisco IOS

- 自动执行 Show Commands

- 自动采集设备信息

- 批量管理设备

- 自动备份配置

- 自动下发配置

- 日志记录

- 异常处理

- 企业目录结构

- GitHub Project

## 为什么 Chapter 3 使用 Netmiko，而不是 Paramiko？

很多教程第一步都会学习 Paramiko。

但是企业 Network Automation Engineer 很少直接使用 Paramiko。

企业通常使用：

Python
    ⬇
Netmiko
    ⬇
Paramiko
    ⬇
SSH
    ⬇
Cisco IOS CLI

也就是说 Netmiko 本身就是建立在 Paramiko 之上的 Cisco 自动化库。

它已经替我们完成了：

- Cisco Prompt 判断

- Enable Mode

- 分页处理

- timing

- command echo

- CLI Buffer

- Cisco Platform Support

因此:
企业里写 Cisco 自动化，首选 Netmiko，而不是直接操作 Paramiko。

Paramiko 以后仍然会学习，但定位是理解 SSH 底层原理，而不是作为 Cisco 自动化的首选工具。

相比很多入门教程，本 Workbook 将顺序调整为：先掌握 Netmiko 完成工程实践，再回过头学习 Paramiko 的底层机制。这更符合企业开发路径。

整个 Chapter 学习路线
Python

⬇

SSH 原理

⬇

Netmiko

⬇

Single Device Automation

⬇

Multi Device Automation

⬇

Backup

⬇

Configuration Deployment

⬇

Logging

⬇

Project Structure

⬇

Enterprise Automation Project

## Chapter Learning Objectives

完成本章以后，应能够独立完成以下任务：

SSH 基础

理解：

- SSH 如何建立连接

- SSH Authentication

- SSH Session

- SSH Channel

- Netmiko

能够：

- 建立连接

- 登录 Cisco

- 自动进入 CLI

- 执行 Show Command

- 获取输出

- Cisco Automation

能够：

- Backup Running Config

- Backup Startup Config

- Save Config

- Deploy Config

- Verify Result

- Enterprise Automation

能够：

- 多设备管理

- Inventory

- Logging

- Exception Handling

- 项目目录设计

- GitHub Project

- Chapter Lab Environment

整个 Chapter 使用统一实验环境。

```
                 Ubuntu

              Python3.10
                 │
           Netmiko Script
                 │ SSH
        ---------------------
        │         │        │
      IOSv1     IOSv2     IOSv3
        │         │        │
           EVE-NG
```

建议实验至少准备三台 Cisco IOSv。

例如：

Device	Management IP
R1	10.10.10.11
R2	10.10.10.12
R3	10.10.10.13

全部开启 SSH。

后续所有实验均基于这一拓扑。

## Enterprise Project Structure（最终目标）

本章最终项目采用如下目录：

```
automation_project/
│
├── inventory/
│      devices.yaml
│
├── backup/
│
├── configs/
│
├── logs/
│
├── output/
│
├── scripts/
│      backup.py
│      deploy.py
│      show.py
│      inventory.py
│
├── utils/
│      logger.py
│      ssh.py
│
├── requirements.txt
└── README.md
```

这是典型的企业自动化项目结构，而不是把所有代码写在一个 main.py 中。

本章章节规划

建议将本章拆分为多个小节，每一节都有完整理论、实验和工程实践。

**Lesson	Topic**

3.1	SSH Fundamentals

3.2	Installing Netmiko

3.3	First SSH Login

3.4	Running Show Commands

3.5	Parsing CLI Output

3.6	Working with Multiple Devices

3.7	Configuration Backup

3.8	Configuration Deployment

3.9	Exception Handling

3.10	Logging

3.11	Enterprise Project Structure

3.12	Final Enterprise Automation Project

后续我们将按上述顺序逐步完成，并在每个实验中遵循统一流程：

Observe → Verify → Analyze → Configure → Verify Again

## Engineering Notes

本章采用以下工程原则：

真实设备优先：所有代码均以 Ubuntu 22.04 + EVE-NG + Cisco IOSv 为目标环境，不使用伪代码。

先验证，再配置：任何自动化脚本执行配置前，应先采集并验证当前设备状态，避免盲目下发命令。

模块化设计：连接、日志、设备清单、业务逻辑分离，避免单文件脚本。

PEP 8 与可维护性：统一命名、函数职责单一、适当添加文档字符串和类型提示（后续章节逐步引入）。

可重复执行（Idempotency）：后续配置部署章节将重点讨论如何避免重复执行导致配置漂移。

安全性：实验阶段可以使用明文凭据；进入工程实践阶段，将逐步迁移到环境变量、配置文件或密钥认证，而不是将密码硬编码到脚本中。

## Chapter 3 Summary

在本章中，我们将从 Cisco CLI Automation 正式过渡到 Network Automation Engineering。

学习重点不再是 Python 语法，而是围绕真实企业网络自动化展开，包括：

理解 SSH 在 Cisco 自动化中的工作机制。

使用 Netmiko 构建稳定的 SSH 自动化连接。

基于 EVE-NG 与 Cisco IOSv 完成真实实验。

建立可扩展、可维护的企业级自动化项目结构。

通过最终项目实现多设备管理、配置备份、配置下发、日志记录与异常处理等核心能力。