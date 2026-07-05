
# Learning Objectives

完成本节后，你应该能够：

- 理解 Module 的本质

- 学会 `import`

- 理解为什么项目需要拆分多个文件

- 能够组织 Cisco 自动化项目

- 为 Chapter 3 做准备

要学会用模块, 没有正常人写 python 写一万两万行. Module = 一个负责单一职责（Single Responsibility）的代码单元.

## 为什么需要 Module？

简单说代码太长难以维护

真正的企业项目会拆分：

```
project/

├── main.py
├── connection.py
├── backup.py
├── parser.py
├── utils.py
└── devices.py
```

每个文件负责一件事情。

## Cisco Automation 也是这样

以后我们的项目不会 netmiko.py 一千行。而是：

```
project/

├──main.py
├──connection.py
├──inventory.py
├──backup.py
├──config.py
```

是不是非常清晰？

## 第一个 Module

创建 [hello.py](python/hello.py)

内容：

```
def hello():
    print("Hello CCIE")
```

再创建 [main.py](python/main.py)

内容：

```
import hello
hello.hello()
```

输出：`Hello CCIE`

## import 的本质

很多教程说 `import hello` 就是导入模块, 没有错。但是Python 真正做的是找到 hello.py 执行这个文件 创建一个 Module Object 绑定到变量 hello

注意 Module 也是对象。所以 `hello.hello()`

实际上是：

hello（Module Object）

       ⬇

hello() Function

## 为什么可以写 hello.hello()

因为第一个 hello 是模块。第二个：`hello()` 是函数。所以模块.函数()

## 更好的写法

Python 允许 `from hello import hello` 以后直接 `hello()` 不用 `hello.hello()`

Cisco 官方为什么喜欢 `from netmiko import ConnectHandler` 现在是不是明白了？其实就是 `from hello import hello` 完全一样。只是 hello.py 换成：netmiko 函数换成 ConnectHandler

## 企业为什么拆 Module？

例如连接全部放 connection.py `def connect()` 备份全部放 backup.py `def backup()` 解析全部放 parser.py `def parse()` 以后任何人看到文件名就知道职责。

## Cisco Automation Example

以后真正项目长这样：

```
automation/
├──main.py
├──connection.py
├──inventory.py
├──backup.py
├──parser.py
```

## main.py

```
from connection import connect
from backup import backup
from inventory import devices

for device in devices:

    conn = connect(device)

    backup(conn)
```

是不是非常像流程图？

## 为什么不要全部写 main.py？

因为以后如果别人只想调用 `backup()` 怎么办？不用复制。直接 `from backup import backup` 就可以。这就是代码复用（Reuse）。

## Lab 2.12

阅读 [main.py](python/2.12/main.py), [connection.py](python/2.12/connection.py) 两个文件

运行后会看到输出结果 

```
Connecting R1
Connecting R2
```

## Analyze

请注意今天最重要的不是 `import` 而是项目开始拆文件了。以后 Chapter 3 甚至 Chapter 8 全部 保持这个结构。

# CCIE Engineer Insight

这里我要告诉你一个我希望你从今天开始养成的习惯。很多初学者写自动化 backup.py 2000 行。

企业里面看到基本直接要求重构。因为没有任何职责划分。

成熟工程师第一反应是这一段代码属于哪个职责（Responsibility）？

例如：

- 连接设备 → connection.py

- 设备清单 → inventory.py

- 配置备份 → backup.py

- 配置解析 → parser.py

- 通用工具 → utils.py

以后项目越来越大。几乎不用修改主程序。