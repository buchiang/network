# Learning Objectives

完成本节后，你将能够：

- 理解什么是异常（Exception）。

- 理解为什么网络自动化脚本必须进行异常处理。

- 掌握 Python `try` / `except` 的基本用法。

- 学会在 Cisco 自动化场景中处理常见连接失败。

- 理解"失败隔离（Failure Isolation）"这一工程思想。

- 为后续 Logging 打下基础。

Python 在运行过程中如果发生错误。

例如：

- SSH 无法连接

- 用户名错误

- 密码错误

- Timeout

- DNS 无法解析

Python 会抛出一个 Exception（异常）。如果没有处理, 程序立即结束。

为什么 Exception Handling 如此重要？原因并不是 "为了不让程序报错。"真正的原因是让程序能够控制错误，而不是被错误控制。

## Cisco Implementation

Cisco 网络环境中, 最常见的异常包括：

- SSH 无法连接。

- 登录认证失败。

- 网络不可达。

- SSH 超时。

这些问题都属于预期可能发生的运行时错误。因此企业自动化脚本应当能够：

- 捕获错误。

- 记录错误。

- 根据需要决定继续还是终止。

而不是直接崩溃退出。

## EVE-NG Lab

![](<../Chapter 3 — SSH Network Automation with Netmiko/image/3.2-0.png>)

[lab 4.4.py](<LABs/lab 4.4.py>) 把设备 IP：12.1.1.1 故意改成：10.1.1.1（实验环境中不存在该设备。） 

在 EVE-NG 运行 

```bash
Common causes of this problem are:
1. Incorrect hostname or IP address.
2. Wrong TCP port.
3. Intermediate firewall blocking access.

Device settings: cisco_ios 10.1.1.1:22
```

# Troubleshooting

### 问题一：为什么这里使用 `except Exception`？

因为这是 Python 所有标准异常的公共父类。对于刚开始学习异常处理来说，可以先掌握这一种写法, 后续随着课程推进，我们再学习如何捕获更具体的异常类型。

### 问题二：为什么没有立即解决错误？

例如 IP 写错。异常处理不会自动修复错误。它负责的是发现错误并决定程序如何响应。

### 问题三：是不是所有代码都应该放进 `try`？

不是, 工程实践中。应该尽量缩小 `try` 的范围。

但是目前为了帮助理解流程。我们先采用简单写法, 后续会进一步优化。

## Engineering Notes

本节建立一个新的工程思想 Automation Should Be Resilient（自动化应具备韧性）。

企业自动化不是追求永远不会失败。

而是追求即使发生失败，也能够以可控的方式继续运行或安全退出。

这正是异常处理存在的价值。