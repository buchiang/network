# Learning Objectives

完成本节后，你将能够：

- 理解什么是 Python 模块（Module）。

- 理解为什么企业自动化项目不会把所有代码写在一个 `.py` 文件中。

- 掌握如何创建自己的 Python 模块。

- 学会使用 `import` 导入自己编写的模块。

- 理解程序入口 `if __name__ == "__main__":` 的工程意义。

- 为下一节 Project Structure 做准备。

经过前几节，我们已经完成了如下代码结构：

```python
def connect_device(device):
def execute_show_command(connection, command):
def disconnect_device(connection):

connection = connect_device(device)
output = execute_show_command(connection, "show version")
print(output)
disconnect_device(connection)
```

代码已经具备：

- Function

- Code Reuse

- Exception Handling

- Logging

但是所有代码仍然放在 automation.py 一个文件中。

如果项目继续增加：

```text
Connect Device

Configure Interface

Backup Config

Save Result

Logging

Exception Handling
```

这个文件最终可能达到 500, 1000 行, 甚至更多. 虽然程序仍然能够运行, 但是维护难度会越来越高。


Python 中有一个重要概念：**Every Python File Is a Module.**

也就是说每一个 `.py` 文件，本质上都是一个 Python 模块。

例如 connect.py 就是一个模块。show_command.py 也是一个模块。

模块的作用是 **将相关能力组织在一起。**

注意模块不是为了减少代码, 而是为了**组织代码（Organize Code）。**

## 为什么企业要拆分模块？

原因主要有三个。

### 原因一：职责清晰

例如连接设备相关 connect.py,

执行 Show Command - show.py, 

Logging - logger.py

不同能力放在不同模块,阅读时更加容易理解。

### 原因二：方便复用

假设今天开发 Backup Script 明天开发 Interface Audit Script 两个程序都会连接设备。如果连接函数已经放在 connect.py 那么两个程序都可以直接使用无需复制代码。

### 原因三：团队协作

企业项目通常由多个工程师共同开发。

例如工程师 A 负责 connect.py

工程师 B 负责 backup.py

工程师 C 负责 logging.py

模块之间职责明确, 能够降低协作冲突。

## Cisco Implementation

假设企业需要开发三个自动化工具：

Inventory Collection

Configuration Backup

Configuration Deployment


虽然业务不同, 但是都需要 Connect Device 因此连接能力通常只维护一份, 多个工具共同调用。这就是模块化设计带来的价值。

### Verify

观察下面三个函数：

```python
connect_device()
execute_show_command()
disconnect_device()
```

它们是否都属于**设备连接能力。**

答案：是。

因此它们适合放在同一个模块。

### Analyze

决定拆分新的结构：

```text
automation/
│
├── device.py
└── automation.py
```

其中 device.py 负责 Connect, Execute Show Command, Disconnect

而 automation.py 负责 Workflow。

## Configure

### 第一步：

创建 device.py 内容：

```python
from netmiko import ConnectHandler

def connect_device(device):
    connection = ConnectHandler(**device)
    connection.enable()
    return connection

def execute_show_command(connection, command):
    return connection.send_command(command)

def disconnect_device(connection):
    connection.disconnect()
```

### 第二步：

修改 automation.py 导入自己的模块。

```python
from device import (
    connect_device,
    execute_show_command,
    disconnect_device,
)
```

注意这与 Chapter 2 学过的：

```python
import time
import logging
```

属于同一种机制。 区别只是 以前导入 Python 标准库。现在导入自己编写的模块。

### 第三步：

保持 Workflow 不变。

```python
connection = connect_device(device)
output = execute_show_command(connection, "show version")
print(output)
disconnect_device(connection)
```

可以发现 Workflow 完全没有变化。 真正变化的是能力已经移动到了独立模块。

# Verification

运行：

```bash
python3 automation.py
```

如果能够正常输出：

```text
show version
```

说明模块拆分成功。程序行为与拆分前保持一致。

# Program Entry Point

现在介绍：

```python
if __name__ == "__main__":
```

为什么现在才讲？

因为现在已经出现两个 Python 文件。Python 文件可能有两种用途：

第一种, 直接运行。

例如：

```bash
python3 automation.py
```

第二种, 被其它程序导入。

例如：

```python
from device import connect_device
```

因此 Python 需要知道 当前文件到底是 Program 还是 Module 于是提供了：

```python
if __name__ == "__main__":
```

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


if __name__ == "__main__":
    main()
```

当：

```bash
python3 automation.py
```

执行时, Python 会调用：

```python
main()
```

但是如果：

```python
import automation
```

Python 就不会自动执行：

```python
main()
```

这就是程序入口（Entry Point）的作用。


# Troubleshooting

## 问题一：为什么提示：

```text
ModuleNotFoundError
```

最常见原因：

```text
device.py
```

与：

```text
automation.py
```

不在同一个目录, 请确认目录结构正确。

## 问题二：为什么导入后程序自动执行？

通常是因为 Workflow 写在 全局作用域没有放入：

```python
main()
```

因此 Python 导入模块时这些代码也会执行。

使用：

```python
if __name__ == "__main__":
```

可以避免这种情况。

## 问题三：为什么不把所有函数拆成很多模块？

模块划分应依据**职责（Responsibility）**。

目前连接相关能力仍然属于 Device Connection 放在一个模块即可, 不要为了拆分而拆分。

## Engineering Notes

本节建立两个新的工程实践。

第一：

> 一个模块负责一个相对完整的能力领域。

第二：

> 程序入口与模块能力分离。

以后 Workflow 位于：

```python
main()
```

能力位于各个模块。这是绝大多数企业 Python 项目的基本组织方式。

