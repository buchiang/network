# Learning Objectives

完成本实验后，你将能够：

* 将 Chapter 4 的所有工程实践整合到一个自动化项目中。

* 使用统一的项目目录组织代码和运行数据。

* 使用模块化设计组织自动化能力。

* 使用异常处理保证程序稳定运行。

* 使用 Logging 记录自动化执行过程。

* 理解一个企业自动化脚本从启动到结束的完整生命周期。


回顾 Chapter 3, 我们的自动化脚本大致如下：

```python
from netmiko import ConnectHandler

device = {
    ...
}

connection = ConnectHandler(**device)

connection.enable()

print(connection.send_command("show version"))

connection.disconnect()
```

它能够完成实验, 但是它缺少：

* 函数封装

* 代码复用

* 异常处理

* 日志记录

* 模块化

* 项目结构

这就是 Chapter 4 要解决的问题。

经过整个 Chapter 4 企业自动化脚本已经逐步演进。

### 第一阶段（Chapter 3）

Main Script ➡ Connect ➡ Show Command ➡ Disconnect

所有逻辑位于一个文件。

### 第二阶段（Lesson 4.2）

Workflow ➡ Functions

能力开始封装。

### 第三阶段（Lesson 4.7）

Workflow ➡ Modules ➡ Functions

代码开始模块化。


### 第四阶段（Lesson 4.8）

```text
Project

├── Source Code
├── Logs
└── Output
```

项目结构形成, 至此自动化脚本已经具备企业项目的基本框架。

## 为什么企业如此重视这些工程实践？

因为真正的软件生命周期通常远远长于开发时间。

例如：

开发 ➡ 上线 ➡ 维护 ➡ 修改 ➡ 维护 ➡ 再次修改 ➡ 持续演进

真正消耗大量时间的是-维护。因此Chapter 4 的所有内容, 本质上都是为了降低未来维护成本。

## Cisco Implementation

假设企业每天凌晨执行：

```text
Configuration Audit
```

整个自动化生命周期通常如下：

Program Start ➡ Initialize Logging ➡ Connect Device ➡ Execute Command ➡ Collect Result ➡ Disconnect ➡ Program End

如果任何一步失败, 程序也应该：

* 记录日志。

* 输出错误。

* 安全退出。

这就是企业自动化的基本要求。

## Observe

确认当前项目目录。

```text
automation/
│
├── automation.py
├── device.py
├── logs/
│   └── automation.log
└── output/
```

目录职责已经清晰。

---

## Verify

检查 Workflow 是否已经足够简单。

例如：

```python
def main():
    connection = connect_device(device)

    output = execute_show_command(
        connection,
        "show version",
    )

    print(output)

    disconnect_device(connection)
```

Main Program 应能够直接体现：

Connect ➡ Execute ➡ Disconnect

而不是 SSH 实现细节。

## Analyze

确认各项能力是否已经分离。

| Capability           | 实现位置       |
| -------------------- | ------------- |
| Connect Device       | device.py     |
| Execute Show Command | device.py     |
| Disconnect Device    | device.py     |
| Workflow             | automation.py |
| Logging              | automation.py |
| Exception Handling   | automation.py |

每项职责都有明确位置。

## Configure

综合整理后的 automation.py

逻辑如下：

```python
import logging

from device import (
    connect_device,
    disconnect_device,
    execute_show_command,
)


def main():
    try:
        logging.info("Connecting to device")

        connection = connect_device(device)

        logging.info("Executing show version")

        output = execute_show_command(
            connection,
            "show version",
        )

        print(output)

        disconnect_device(connection)

        logging.info("Disconnected")

    except Exception as error:
        logging.error(error)


if __name__ == "__main__":
    main()
```

注意：这里没有新增任何 Python 知识, 只是把整个 Chapter 4 的内容整合起来。

## Verify Again

完成以下验证。

### 功能验证

确认能够成功登录 Cisco IOSv。

执行 `show version` 输出正确。

### 日志验证

确认 logs/automation.log 生成。

能够看到：

* Connecting

* Executing

* Disconnected

等事件。


### 异常验证

故意修改设备 IP 确认程序不会异常退出, 能够记录, 错误日志。

### 工程验证

再次检查项目目录确认源码, 日志, 运行数据。已经完全分离。

# Troubleshooting

## 问题一：程序可以运行，但日志为空。

请确认程序开始阶段已经完成：

```python
logging.basicConfig(...)
```

初始化。


## 问题二：程序导入模块时报错。

检查：

```text
automation.py

device.py
```

是否位于同一目录。

---

## 问题三：Workflow 越来越长怎么办？

这是正常现象 Workflow 负责描述业务流程, 真正增长较快的通常是 Capabilities。

如果 Workflow 开始承担大量实现细节, 说明需要再次进行重构。

## Engineering Notes

Chapter 4 建立了整个 Workbook 最重要的工程思想。

以后无论：

* REST API

* NETCONF

* 数据驱动自动化

* 模板化部署

都会继续保持：

Workflow ➡ Capability ➡ Module ➡ Project 这一组织方式, 工程实践不会因为技术变化而改变。