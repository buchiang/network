# Learning Objectives

完成本节后，你将能够：

- 理解为什么企业自动化脚本需要函数（Function）。

- 理解函数在网络自动化中的真正定位。

- 将 Chapter 3 的 Netmiko 脚本重构为多个可复用能力（Reusable Capabilities）。

- 学会判断哪些代码应该封装成函数，哪些不应该。

- 为后续的 Exception Handling、Logging、Module Design 打下统一的工程基础。

在 Chapter 2，我们学习 Function 时，把它理解为一段可以重复调用的代码。这是 Python 语法层面的定义。到了 Chapter 4，我们重新定义 Function：

Function = 一个可复用的工程能力（Reusable Engineering Capability）。

注意，这是本书后续都会坚持的定义。

## 为什么企业如此强调 Function？

原因不是为了减少代码行数。真正的原因有三个。

### 原因一：减少重复

例如：以后有 100 台设备。每台设备都要：

登录 ➡ Enable ➡ show version

如果没有函数登录流程会复制 100 次。修改一次密码需要修改 100 个地方维护成本极高。

### 原因二：职责单一（Single Responsibility）

观察下面两个函数。

函数 A：

`连接设备`

函数 B：

`执行 Show Command`

职责非常明确。

但是下面这种：

连接 ➡ Enable ➡ show ➡ Configure ➡ Save ➡ Disconnect

全部放进一个函数, 以后修改任何一步，都可能影响整个函数。

因此一个函数应该只完成一种能力。这是企业代码最重要的设计原则之一。

#### 说明（Engineering Note）

在软件工程中，这一思想与 Single Responsibility Principle（单一职责原则） 一致。我们在这里先采用"一个函数只负责一种能力"这一工程实践，不展开更完整的设计原则，相关内容将在更靠后的软件工程章节再系统介绍。

### 原因三：方便测试

假设今天发现 `show version` 执行失败。如果 `execute_show_command()` 是独立函数。

那么我们只需要检查这一个函数, 而不是阅读整个脚本。这就是可测试性（Testability）。

## Cisco Implementation

Cisco 自动化脚本通常都会按照能力划分。

例如：

Inventory ➡ Connect ➡ Execute ➡ Save Result ➡ Disconnect

注意这里不是按照：

第 1 行 ➡ 第 2 行 ➡ 第 3 行

组织代码。而是按照自动化流程中的能力 Python Function 正好可以实现这一目标。

## Verify

思考下面几个问题。

问题一 以后 `Connect` 还会不会继续使用？

答案：一定会。几乎所有网络自动化脚本都会建立连接。因此值得封装。

问题二 以后 `Disconnect` 还会不会继续使用？

答案：一定会。也值得封装。

问题三 以后 `show command` 会不会越来越多？

答案：一定会。因此执行命令也应该独立出来。

## Analyze

经过分析我们决定把脚本拆分成多个能力。规划如下：

```
Main Program
      │
      ├──────────────┐
      │              │
      ▼              ▼
connect_device()  disconnect_device()

      │
      ▼
execute_show_command()
```

这是 Chapter 4 第一次建立 Capability-Based Design（基于能力的设计）。注意 Main Program 不再负责所有细节。它只负责协调这些能力。

## Configure

### 第一步建立连接函数。

```python 
from netmiko import ConnectHandler

def connect_device(device):
    connection = ConnectHandler(**device)
    connection.enable()
    return connection
```

这里没有新增 Python 语法。只是把 Chapter 2 已经学习过的 Function 用在了网络自动化中。

### 第二步建立执行命令函数。

```python
def execute_show_command(connection, command):
    output = connection.send_command(command)
    return output
```

这个函数只负责执行命令。

不负责：

- 登录
- 保存
- 关闭连接

职责保持单一。

### 第三步建立断开连接函数。

```python
def disconnect_device(connection):
    connection.disconnect()
```

职责也非常清晰。

### 第四步：Main Program。

```python 
connection = connect_device(device)

print(execute_show_command(connection, "show version"))

disconnect_device(connection)
```

观察 Main Program。是不是已经开始接近：

Connect ➡ Execute ➡ Disconnect

代码已经越来越像网络自动化流程。

## Verify Again

确认程序输出是否与 Chapter 3 完全一致。应该看到 `show version` 的输出没有变化。

说明重构成功。工程中有一句非常重要的话：Refactoring changes structure, not behavior. 可以理解为重构改变的是代码组织方式，而不是程序功能。这也是本节实验最重要的验证目标。

# Troubleshooting

### 问题一：为什么 connection.enable() 放在 connect_device() 里面？

因为对于本 Workbook 后续的实验来说，大多数自动化任务都需要进入 Privileged EXEC Mode。

把它放在连接函数中，可以避免每次都重复调用。

工程说明：

如果未来需要支持不进入 Enable Mode 的设备或场景，再对函数进行扩展，而不是一开始就为了所有可能性增加复杂度。

### 问题二：为什么 print() 没有写进函数？

例如：

```python 
def execute_show_command(connection, command):
    print(connection.send_command(command))
```

虽然可以运行。但是函数就承担了两种职责：

- 执行命令

- 显示结果

工程上，更好的做法是：

```python 
output = execute_show_command(connection, "show version")
print(output)
```

函数负责获取数据。Main Program 决定如何使用数据。职责更加清晰。

### 问题三：为什么函数返回 connection？

因为后续所有 `show`, `configure`, `save` 都需要使用同一个 SSH Connection。如果不返回。后面的函数无法继续使用它。

## Engineering Notes

这一节建立了一个非常重要的工程思想 Main Program 不负责具体工作 Main Program 应该像项目经理。

它负责：

Connect ➡ Execute ➡ Disconnect

真正完成工作的，是下面这些能力：

```python 
connect_device()
execute_show_command()
disconnect_device()
```

以后：

Logging

Exception

Module

Project Structure

都会采用同样的设计思想。这也是企业网络自动化代码最常见的组织方式之一。