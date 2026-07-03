
# Learning Objectives

完成本节后，你应该能够：

- 理解 Python 是如何执行代码的

- 理解 Python Interpreter 的工作流程

- 掌握 Python 基本语法规则

- 理解为什么 Python 使用缩进（Indentation）

- 学会编写第一个规范的 Python 程序

- 能够阅读 Cisco 官方示例代码


## Python 工作流

Python Source Code

        ⬇

Python Interpreter

        ⬇

Bytecode（Python 字节码）

        ⬇

Python Virtual Machine（PVM）

        ⬇

Operating System

        ⬇

       CPU

*Python Virtual Machine（PVM）不是 VMware、VirtualBox 那种虚拟机。*

*它只是 Python 解释器内部的执行环境，用来运行 Python 字节码。*

## Python 的第一条语法规则

**使用缩进（Indentation）**

Python 与 C、Java、Go 等语言最大的不同：

它不用` {} `表示代码块。

Java

```
if (x > 5) {
    System.out.println("Hello");
}
```

Python

```
if x > 5:
    print("Hello")
```

## 第二条规则

大小写敏感（Case Sensitive）

## 第三条规则

注释（Comments）

单行注释：

`# Connect Device`

多行说明通常使用：

```
"""
Backup Script

Author:
Date:
Purpose:
"""
```

*严格来说，这是多行字符串（Multiline String），常用于模块、函数和类的文档说明（Docstring），并不是专门的多行注释语法。后面学习函数时我们会详细介绍。*

## 第四条规则

一行通常写一条语句

Lab 2.2

[lab02.py](python/lab02.py)

在 linux 中

`python3 lab02.py`

```
user@ubuntu22-desktop:~$ python3 lab02.py
CCIE Enterprise Infrastructure
Python Automation
Chapter 2
```

## Troubleshooting 思维

以后看到 Python 报错，不要第一反应就是改代码。

建议按照固定流程分析：

1. 看最后一行错误类型
    
    - NameError
    
    - SyntaxError

    - TypeError

    - ValueError

    - ModuleNotFoundError

    - …

2. 看错误发生在哪一行

3. 根据错误类型分析原因

这是网络工程师排查 Python 脚本最有效的方法。