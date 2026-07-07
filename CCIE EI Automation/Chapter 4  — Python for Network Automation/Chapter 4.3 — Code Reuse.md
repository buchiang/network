# Learning Objectives

完成本节后，你将能够：

- 理解什么是代码复用（Code Reuse）。

- 理解为什么企业自动化项目强调"复用能力"，而不是复制代码。

- 学会识别网络自动化脚本中的重复逻辑（Duplicate Logic）。

- 使用 Chapter 2 已学习的 `function` 提高代码复用率。

- 为后续的 Module Design（模块化设计）做好准备。

### Problem

需要在同一台 Cisco IOSv 上执行三条 Show 命令：

```bash
show version
show ip interface brief
show ip route
```

很多刚开始学习 Netmiko 的工程师会这样写：

```python
connection = connect_device(device)
print(connection.send_command("show version"))
print(connection.send_command("show ip interface brief"))
print(connection.send_command("show ip route"))
disconnect_device(connection)
```

程序完全没有问题。但是，如果以后需要执行 10 条、20 条，甚至 100 条命令呢？Main Program 会越来越长。

更重要的是，`connection.send_command()` 这一能力已经在上一节封装为 `execute_show_command()`，如果继续直接调用 `send_command()`，就绕过了已经建立的工程能力。

这说明：**仅仅写了函数，并不等于真正实现了代码复用**。

很多初学者认为：Code Reuse = 少写代码。实际上，这只是表面现象。

真正的定义应该是：Code Reuse 是复用已经验证过的能力，而不是重复编写相同逻辑。这里有两个概念需要区分。

## 重复代码（Duplicate Code）

例如：

```python
print(connection.send_command("show version"))
print(connection.send_command("show ip interface brief"))
print(connection.send_command("show ip route"))
```

虽然命令不同, 但是真正执行工作的逻辑完全一样。

都是：Send Command ➡ Receive Output ➡ Return Result

这属于重复逻辑。

## 复用能力（Reusable Capability）

如果已经有：

```python
def execute_show_command(connection, command):
    output = connection.send_command(command)
    return output
```

那么以后所有 Show 命令，都应该使用它。

例如：

```python
print(execute_show_command(connection, "show version"))
print(execute_show_command(connection, "show ip interface brief"))
print(execute_show_command(connection, "show ip route"))
```

这样真正发生变化的只有：

show version ➡ show ip interface brief ➡ show ip route

执行命令的方法始终只有一种。

## 为什么企业如此强调 Code Reuse？

### 原因一：统一修改

假设以后 Cisco IOS 升级。所有 Show Command 前都需要增加某些处理逻辑。

如果整个公司有 `connection.send_command(...)` 出现了500次。那么需要修改500个地方。如果全部调用 `execute_show_command()` 只需要修改 `def execute_show_command()` 里面的一次。整个项目都会自动受益。

### 原因二：统一行为

企业自动化希望任何工程师执行 `execute_show_command()` 得到的行为都是一致的。而不是张工程师 `send_command(...)` 李工程师 `print(send_command(...))` 王工程师 `output = send_command(...)` 每个人都采用自己的方式, 统一入口，意味着统一行为。

### 原因三：降低 Bug 数量

软件工程有一句广为流传的话 Don't Repeat Yourself（DRY）意思是不要重复自己. 重复代码越多 Bug 通常越多。

因为修改一个地方, 容易忘记修改另一个地方。统一复用，可以减少这种风险。

### 说明（Engineering Note）

DRY 是软件工程中的经典原则。本章先把它理解为"不要复制同样的业务逻辑"，更深入的软件工程背景将在后续相关章节再介绍。

## Cisco Implementation

观察一个典型的网络自动化流程：

Connect ➡ Execute Show Command ➡ Process Output ➡ Disconnect

这里 "Execute Show Command" 不是一次性的动作。

它可能会执行：

```bash
show version
show ip interface brief
show inventory
show ip route
show vlan
show spanning-tree
```

因此企业不会为每条命令都写一套新的执行逻辑。而是复用同一个执行能力。

# Troubleshooting

### 问题一：为什么还要多写一个函数？不是更麻烦了吗？

对于只有三条命令的小实验，看起来确实增加了几行代码。但是如果以后有50条 Show 命令
100 台设备多个工程师共同维护函数的价值就会非常明显。工程设计关注的是长期维护成本，而不是当前代码行数。

### 问题二：为什么 Main Program 不直接调用 send_command()？

因为 Main Program 应该负责做什么（What）而不是怎么做（How）"How" 已经封装在 `execute_show_command()` 里面。

### 问题三：是不是所有代码都应该封装成函数？

不是。判断标准不是代码长不长。而是是否形成了一项可以重复使用的能力。

例如：

- 建立连接。

- 执行命令。

- 关闭连接。

这些都会不断重复, 因此值得封装。

## Engineering Notes

本节建立第二个重要工程思想。Main Program 应该越来越简单理想情况下。

Main Program 更像：

Connect ➡ Execute ➡ Disconnect

而不是：

SSH ➡ Socket ➡ Authentication ➡ CLI ➡ Send Command ➡ Receive Output

所有实现细节。都应该隐藏在函数内部。这样阅读 Main Program。就可以快速理解整个自动化流程。这也是企业代码 Review 时重点关注的内容之一。