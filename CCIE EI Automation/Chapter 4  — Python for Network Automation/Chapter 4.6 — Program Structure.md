# Learning Objectives

完成本节后，你将能够：

- 理解为什么程序结构（Program Structure）比代码数量更重要。

- 理解 Main Program 的职责。

- 学会区分"流程控制"和"能力实现"。

- 为下一节 User-defined Module 做准备。

- 建立企业自动化脚本的统一组织方式。

经过前几节，我们已经把脚本重构成：

```python
def connect_device(...):
def execute_show_command(...):
def disconnect_device(...):
```

然后：

```python
connection = connect_device(device)
output = execute_show_command(connection, "show version")
print(output)
disconnect_device(connection)
```
已经比 Chapter 3 好很多, 但是企业工程师继续 Review 仍然会说**代码结构还可以继续优化**。为什么？

很多初学者认为程序就是：

第一行 ➡ 第二行 ➡ 第三行 ➡ ……

企业不是这样理解。

企业更关注程序结构（Program Structure）。一个自动化脚本通常可以分成两个部分

能力（Capabilities） ➡ 流程（Workflow）

能力负责怎么做（How）

流程负责做什么（What）

这是本节最重要的思想。

### Capabilities

例如：

```python
Connect Device
Execute Show Command
Disconnect Device
```

这些都是能力。它们负责具体实现。

### Workflow

Workflow 则描述：

Connect ➡ Show Version ➡ Disconnect

Workflow 不关心 SSH, Socket, Authentication, CLI。

它只负责组织整个自动化流程。

## 为什么企业强调 Workflow？

因为阅读程序时。工程师首先想知道这个程序到底干什么？而不是 `send_command()` 有几个参数？

例如下面这个 Workflow：

Connect ➡ Backup Running Config ➡ Save Result ➡ Disconnect

任何网络工程师不用了解实现细节, 就知道这是一个配置备份脚本。

这就是程序可读性（Readability）。

## Cisco Implementation

Cisco 自动化项目中，一个典型脚本通常可以抽象为：

Prepare ➡ Connect ➡ Execute ➡ Collect Result ➡ Disconnect ➡ Finish

真正的 SSH 细节, CLI 细节都隐藏在各个能力内部。

这样 Workflow 十分清晰。

### Observe

观察目前程序, 它实际上已经分成：

Function ➡ main Workflow

### 思考下面哪些属于：Workflow？

```python
connection = connect_device(device)
output = execute_show_command(connection, "show version")
print(output)
disconnect_device(connection)
```
答案全部属于 Workflow。因为它描述程序流程。

再看 `def connect_device(...)` 它属于 Capability。

### Analyze

所以一个企业脚本应该满足：

Workflow ➡ 调用 Capabilities

而不是：

Workflow ➡ SSH ➡ Socket ➡ CLI ➡ Authentication ➡ Output ➡ ……

实现细节应该全部隐藏。

现在已经越来越接近企业 Workflow。

虽然目前仍然位于全局作用域（Global Scope），但这是我们有意保留的状态，因为程序入口（`main()` 与 `if __name__ == "__main__":`）将在下一阶段、结合用户自定义模块一起介绍。

### Verify Again

再次阅读 Main Workflow 问自己：不用进入任何 Function 是否已经知道程序要完成：

Connect ➡ Show Version ➡ Disconnect

如果答案：是。

说明程序结构已经开始符合企业工程实践。

# Troubleshooting

### 问题一：为什么 Main Workflow 这么简单？

因为真正复杂的东西。已经放到 Function. Workflow 越简单, 程序越容易维护。

### 问题二：是不是 Workflow 永远不会变？

不是。Workflow 会根据业务变化, 但是 Capabilities 通常复用很多年。

因此 Workflow 和 Capability 应该分离。

### 问题三：Workflow 与 Function 哪个更重要？

二者缺一不可, 没有 Workflow 程序缺乏整体流程。没有 Function。程序缺乏复用能力, 工程实践要求两者协同工作。

## Engineering Notes

这一节建立了一个贯穿后续 Workbook 的思想 Workflow Orchestrates, Capabilities Execute.

也就是 Workflow 负责组织，Capability 负责实现。

以后：

- Logging

- Exception

- Module

- REST API

- NETCONF

都会遵循这一设计思想。