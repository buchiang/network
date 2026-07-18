## Theory

在编写任何 API 自动化代码之前, 我们必须先理解 API 底层所使用的通信协议. 这和 Chapter 3 的设计思想完全一致, 在 Chapter 3 中, 我们并没有一开始就学习 Netmiko, 而是先理解 SSH. 

同样, 在 API Automation 中, 我们也不会一开始就学习 Python 的 requests 库, 而是先理解 HTTP, 这是企业工程中非常重要的一点. 

很多教程都是: 

```python
import requests

requests.get(...)
```

代码马上就能运行, 但是, 当请求失败、认证错误、服务器返回异常状态码时, 很多人就不知道发生了什么. 

企业工程师不能只会调用库, 必须理解底层协议. 因此, 本章首先学习 HTTP, 而不是 Python API. 

## Engineering Discussion

为什么 API Automation 需要 HTTP? 

在前面的几个章节, 我们一直都是通过 SSH 与设备通信. 

整个流程: Python ➡ SSH ➡ Device CLI

Python 建立 SSH Session 随后: 

- 登录设备

- 输入命令

- 接收 CLI 输出

- 解析文本

- 执行业务逻辑

整个过程, 本质上是在模拟一个网络工程师登录终端操作设备, 而 API Automation 完全不同, 它并不会打开一个 Terminal, 它直接与设备（或者服务器）的软件接口通信. 

整个流程变成: Python ➡ HTTP ➡ API Service

此时 Python 不再输入命令, 而是发送一个 HTTP Request, 服务器返回一个 HTTP Response. 

整个通信对象已经从人类使用的 CLI 变成了 软件使用的 API. **这也是 API 自动化最大的变化. **

## CLI 与 API 的本质区别

很多初学者认为 API 就是不用 SSH, 其实这种理解并不准确, 真正的区别在于 
CLI 是为人设计的. 

例如: `show ip interface brief`

返回: 

```
Interface              IP-Address      OK? Method Status
GigabitEthernet0/0     10.1.1.1        YES manual up
```

这是为了方便工程师阅读, 因此: 

- 有表格

- 有空格对齐

- 有缩写

- 有提示信息

这些都适合人类阅读, 却不适合程序处理. 

因此我们在 Chapter 9 才需要: 

Backup ➡ Parser ➡ Compliance

Parser 的存在, 就是因为 CLI 输出本身不是结构化数据. 

API 则不同, API 天生就是给程序调用的. 例如服务器可能返回: 

```
{
    "interface": "GigabitEthernet0/0",
    "ip": "10.1.1.1",
    "status": "up"
}
```

这里已经不存在: 

- 对齐

- 空格

- 表格

- 人类阅读格式

**而是一份结构化数据（Structured Data）.**

Python 可以直接读取其中的字段, 而无需像 Chapter 9 那样先进行文本解析, 这也是 API 自动化相比 CLI 自动化最大的优势之一. 

## HTTP 是什么? 

HTTP（HyperText Transfer Protocol）是一种应用层协议（Application Layer Protocol）. 

它最初用于浏览器访问网页. 

例如: 浏览器 ➡ HTTP ➡ Web Server

后来, 人们发现既然浏览器可以通过 HTTP 与服务器通信, 那么 Python 程序当然也可以. 

于是越来越多的软件开始提供 HTTP 接口. 

今天我们熟悉的: 

- 网络控制器

- 云平台

- Firewall Manager

- 虚拟化平台

- 监控平台

- IPAM

- CMDB

几乎都会提供 HTTP API. 

因此 HTTP 已经成为现代自动化最重要的通信协议之一, HTTP 在 Enterprise Automation Platform 中的位置

这里要特别注意一个工程设计思想, Chapter 8 和 Chapter 9 已经建立了整个平台的分层架构. 

例如: Inventory ➡ Connection ➡ Business Logic

这里的 Connection 并不代表 SSH. 它代表的是自动化平台与外部系统建立通信的一层. 

在 Chapter 3 ~ Chapter 9 中, Connection 的实现方式只有一种: 

Connection ➡ SSH

到了 Chapter 10, 平台架构并不会改变, 只是 Connection 层增加了另一种通信方式. 

```
              Connection
             /          \
            /            \
         SSH            HTTP API
```

也就是说: 

>Business Logic 根本不知道下面到底使用的是 SSH, 还是 HTTP. 

它只知道 "我需要获取数据. " 至于: 

- 是通过 SSH 获取, 

- 还是通过 HTTP 获取, 

这是 Connection 层自己的职责. 

这正是前面几个章节一直坚持的 Single Responsibility Principle（单一职责原则）. 

## Engineering Insight

很多企业在自动化平台演进过程中都会犯一个错误一旦开始学习 API, 就重新设计整个平台. 

例如: 

SSH Project ➡ API Project ➡ REST Project ➡ NETCONF Project

最终形成多个互不关联的小项目, 这并不是企业工程推荐的做法. 

更合理的方式是保持平台架构稳定, 仅替换或扩展 Connection Layer. 

也就是说, 无论未来使用: 

- SSH

- HTTP API

- NETCONF（Chapter 11）

- RESTCONF（后续章节）

- gNMI（后续章节）

对于上层业务逻辑来说, 它们都只是不同的通信方式, 而不是不同的平台. 

这种设计能够保证 Enterprise Automation Platform 在技术演进过程中保持长期稳定, 而不会因为引入新的协议就推倒重来. 

Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么学习 API Automation 要先学习 HTTP, 而不是直接学习 requests? 

- CLI 与 API 的本质区别是什么? 

- 为什么 CLI 输出需要 Parser, 而 API 返回的数据通常不需要? 

- HTTP 在整个 TCP/IP 协议栈中的位置是什么? 

- 在我们的 Enterprise Automation Platform 中, HTTP 应该属于哪一层? 

- 为什么引入 HTTP 后, 平台架构仍然保持不变? 

##Summary

本节建立了 Chapter 10 的核心思想: 

- HTTP 是 API Automation 的基础协议. 

- CLI 面向人, API 面向程序. 

- API 返回的是结构化数据, 而不是终端文本. 

- Connection 是抽象层, 而 SSH、HTTP 只是不同的实现方式. 

- Chapter 10 不会重新设计平台, 而是在现有架构上扩展一种新的通信能力. 

至此, 我们已经完成了 HTTP 的整体定位. 下一节将开始深入分析 HTTP Request 的组成结构, 理解一个 HTTP 请求究竟包含哪些元素, 以及它们各自承担什么职责. 