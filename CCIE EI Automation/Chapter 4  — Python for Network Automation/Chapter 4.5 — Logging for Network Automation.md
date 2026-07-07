# Learning Objectives

完成本节后，你将能够：

- 理解为什么企业自动化不能依赖 `print()`。

- 理解什么是日志（Log）。

- 学会使用 Python 标准库 `logging`。

- 在网络自动化脚本中记录关键运行事件。

- 理解 `Logging` 与 Exception Handling 的关系。

目前我们的脚本可能是这样的：

```python
try:
    connection = connect_device(device)

    print(execute_show_command(connection, "show version"))

    disconnect_device(connection)

except Exception as error:
    print(error)
```

程序能够运行。如果失败也能看到 Authentication failed 看起来已经不错。但是假设昨天晚上 02:00。自动化程序自动运行。今天上午 09:00 主管问昨天晚上哪台设备登录失败？你还能回答吗？

不能, 因为昨天终端输出已经没有了。

### 什么是 Log？

Log（日志）就是程序运行过程中的事件记录（Event Record）。注意不是程序输出（Output）。

例如下面这些都属于日志。

- Program Started

- Connect R1

- Enable Mode

- Execute show version

- Disconnect R1

- Program Finished

这些信息即使程序执行成功, 以后仍然可以查看。这就是日志。

## 为什么企业自动化一定需要 Logging？

### 原因一：可追溯性（Traceability）

假设凌晨自动执行100台 Router 上午有人说 R37 没有完成备份。如果没有日志。没人知道程序到底运行到了哪里。

如果有日志。可以立即看到：

```bash
09:12:31 Connect R37
09:12:36 Authentication Failed
```

问题马上定位。

### 原因二：故障分析（Troubleshooting）

Exception 告诉我们程序发生错误。Logging 告诉我们错误发生之前程序做了什么。

例如：

Connect R1 ➡ Enable ➡ show version ➡ Timeout

这比一句 Timeout 有价值得多。

### 原因三：长期维护

企业自动化通常不是运行一次。而是每天, 每周, 每月持续执行。日志就是程序的运行历史。很多企业保留自动化日志数月甚至数年，以满足审计、问题追踪和运维分析的需要。

## Cisco Implementation

假设每天凌晨自动采集 `show version`

企业通常希望看到

```bash
2026-07-08 02:00:01 Connect R1
2026-07-08 02:00:03 Execute show version
2026-07-08 02:00:05 Disconnect
```

如果失败

```bash
2026-07-08 02:00:01 Connect R2
2026-07-08 02:00:06 Authentication Failed
```
注意日志记录的是 事件（Event）。

不是 CLI 输出。CLI 输出属于业务数据。日志属于运行记录, 这是两个不同概念。

**Engineering Note**

后续章节中，我们会把设备输出（如 `show version` 的结果）保存到专门的数据文件，而运行日志继续由 `logging` 管理。不要把这两类信息混在一起。

## EVE-NG Lab

本实验第一次使用 Python 标准库：

`import logging`

目前程序使用 `print(...)` 输出信息, 关闭终端以后所有信息都会消失。

运行一次程序观察终端, 关闭终端再次尝试查看昨天执行过程。发现无法查看。

说明 `print()` 适合人与程序即时交互。不适合长期记录自动化执行历史。

## Configure

### 第一步：

导入标准库 `import logging` 注意这是 Python 标准库无需安装。

### 第二步：

初始化 Logging。

```python
logging.basicConfig(
    filename="automation.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
```

这里先理解三个最重要参数 

- `filename` 日志保存位置。例如：automation.log

- `level`记录什么级别的信息。本章先统一使用 logging.INFO

    日志级别的详细分类（如 DEBUG、WARNING、ERROR、CRITICAL）将在后续专门讨论，目前先掌握 INFO 即可。

- `format` 定义日志格式。例如：

    - 时间

    - 日志级别

    - 消息内容

### 第三步：

开始记录事件。

例如：

`logging.info("Connecting to device")` 登录成功

`logging.info("Connected successfully")` 执行命令

`logging.info("Executing show version")` 断开连接

`logging.info("Disconnected")` 异常

```python
except Exception as error:
    logging.error(error)
```

注意这里第一次出现 `logging.error()`  因为错误属于 Error Event。

## Verify Again

运行程序, 当前目录应该出现 automation.log 打开可以看到类似：

```
2026-07-07 21:30:01 INFO Connecting to device
2026-07-07 21:30:03 INFO Connected successfully
2026-07-07 21:30:05 INFO Executing show version
2026-07-07 21:30:07 INFO Disconnected
```

说明日志已经开始记录程序运行过程。

# Troubleshooting

### 问题一：为什么还有 `print()`？

目前保留 `print(output)` 因为用户仍然希望立即看到 CLI 输出。但是程序运行过程应该交给 `logging` 二者职责不同。

### 问题二：为什么日志文件没有生成？

常见原因：

- 程序没有运行到 `logging.info()`。

- 当前目录没有写权限。

- `basicConfig()` 没有在第一次记录日志之前执行。

按照本章实验环境（Ubuntu 22.04 普通用户目录），默认应能够正常创建 automation.log。

### 问题三：为什么不把 Show Command 输出全部写进日志？

因为日志记录的是程序运行过程 CLI 输出属于设备业务数据。

后续章节会学习如何保存 show version 结果。

不要混在运行日志里面。

## Engineering Notes

本节建立一个新的工程思想：

Logs Describe What Happened（日志描述程序发生了什么）。

而不是 Logs Store Everything（日志保存所有内容）。

因此日志应该记录：

- 程序开始。

- 建立连接。

- 执行操作。

- 发生异常。

- 程序结束。

而不是把所有 CLI 输出全部写进去。