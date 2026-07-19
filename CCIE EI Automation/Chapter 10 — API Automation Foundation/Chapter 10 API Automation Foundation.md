# 10.1 HTTP Fundamentals for Automation Engineers

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

## Summary

本节建立了 Chapter 10 的核心思想: 

- HTTP 是 API Automation 的基础协议. 

- CLI 面向人, API 面向程序. 

- API 返回的是结构化数据, 而不是终端文本. 

- Connection 是抽象层, 而 SSH、HTTP 只是不同的实现方式. 

- Chapter 10 不会重新设计平台, 而是在现有架构上扩展一种新的通信能力. 

至此, 我们已经完成了 HTTP 的整体定位. 下一节将开始深入分析 HTTP Request 的组成结构, 理解一个 HTTP 请求究竟包含哪些元素, 以及它们各自承担什么职责. 

# 10.2 HTTP Request Structure

## Theory

每一次 API 通信, 都始于一个 HTTP Request(HTTP 请求). 

可以把它理解为客户端向服务器发送的一份标准格式的请求. 

无论你以后使用: 

- Python

- curl

- Postman

- 浏览器

发送的实际上都是 HTTP Request, 不同工具只是生成 Request 的方式不同. 因此, 学习 HTTP 的第一步, 就是理解一个 Request 到底由哪些部分组成. 

## Engineering Discussion

一个 HTTP Request 包含什么? 从工程角度来看, 一个 HTTP Request 可以抽象为四个部分: 

```
HTTP Request
│
├── Method(请求方法)
├── URL(请求地址)
├── Headers(请求头)
└── Body(请求内容)
```

几乎所有 HTTP API, 都离不开这四个组成部分. 以后学习任何 API(无论是 Cisco、VMware、AWS 还是其他平台), 都会看到它们. 

**因此, 这四个概念必须牢固掌握. **

## 第一部分: Method(请求方法)

Method 用来告诉服务器"我希望你执行什么操作. "

例如: 

- 获取信息

- 创建对象

- 修改配置

- 删除资源

Method 描述的是动作(Action), 而不是数据本身. 

例如: GET

表示: 我想读取数据. 

而 POST

表示: 我想提交新的数据. 

注意 Method 并不是 API 自己发明的, 它属于 HTTP 协议的一部分. 后面我们会专门学习各种 HTTP Method. 

## 第二部分: URL(统一资源定位符)

URL(Uniform Resource Locator)用于告诉服务器: "我要访问哪个资源. "

例如: `https://server.example.com/interfaces`

服务器看到这个地址, 就知道客户端希望访问 interfaces 这个资源. 

这里要注意一个概念, 很多初学者喜欢说调用 API. 实际上, 更准确的说法应该是访问 API 提供的 Resource(资源), 这是 REST 风格 API 的核心设计思想, 也是现代 HTTP API 的基本理念. 

目前, 我们只需要理解 URL 决定了请求发送到哪里. 

## 第三部分: Headers

很多初学者第一次看到 Header 时, 会觉得它很神秘. 其实可以把它理解成**附加说明(Metadata). **

例如: 

客户端可能告诉服务器我发送的是 JSON

或者这是我的身份认证信息. 

或者我希望服务器返回中文. 

这些都属于 Header. 

可以理解成真正的数据还没开始发送, Header 只是告诉服务器**"关于这次请求, 还有一些额外的信息. "**

因此 Header 本身通常不是业务数据, 而是描述请求本身的数据. 

## 第四部分: Body(请求体)

Body 是真正携带业务数据的地方. 

例如: 假设要创建一个新的 Loopback Interface. 

真正的接口信息: 

- Interface Name

- IP Address

- Description

都会放在 Body 中. 

例如(这里只是示意, 不讨论具体格式): 

```
Interface = Loopback0
IP = 10.1.1.1
Description = Management
```

真正的数据就在这里, 而不是放在 Header. 

因此: 

Header 描述请求. 

Body 描述业务数据. 

两者职责完全不同. 

## HTTP Request 的整体结构

综合起来, 一个 HTTP Request 可以表示为: 

```
                HTTP Request
                      │
      ┌───────────────┼───────────────┐
      │               │               │
   Method            URL          Headers
                                      │
                                      ▼
                                   Body
```

也可以理解为: 

客户端 ➡ 我要做什么? (Method) ➡ 访问哪里? (URL) ➡ 还有什么需要说明? (Headers) ➡ 真正的数据是什么? (Body) ➡ 服务器

这个流程几乎适用于所有现代 HTTP API. 

## 与 SSH Automation 的对比

为了帮助理解, 我们可以把 HTTP Request 与之前学习的 SSH Automation 做一个对照. 

| SSH Automation  | HTTP API Automation |
| --------------- | ------------------- |
| 登录设备            | 建立 HTTP 请求          |
| 输入 CLI 命令       | 指定 Method           |
| 登录目标设备          | 指定 URL              |
| SSH 参数（用户名、密码等） | Headers（认证、格式等）     |
| CLI 命令中的参数      | Body（业务数据）          |

需要注意的是, 这个表格只是帮助建立概念, 并不是一一对应的技术实现. 

例如, SSH 登录和 HTTP 请求生命周期并不完全相同, 但它们都承担了"建立通信并传递操作意图"的作用. 

## Engineering Insight

对于网络工程师来说, 一个重要的思维转变是在 CLI 中, 我们思考的是我要输入哪条命令? 

而在 API 中, 我们思考的是我要向哪个资源发送什么样的请求? 

例如, 在 CLI 中可能会想 `show ip interface brief`

而在 API 中, 更接近的思考方式是 读取 Interfaces Resource

可以发现, API 更关注资源(Resource), 而不是命令(Command). 

这种设计使得不同厂商的 API 更容易保持一致, 也更适合软件自动处理. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 一个 HTTP Request 包含哪四个组成部分? 

- Method 的职责是什么? 

- URL 的职责是什么? 

- Header 与 Body 的区别是什么? 

- 为什么 Header 不应该承载业务数据? 

- 为什么 API 更强调 Resource, 而不是 Command? 

## Summary

本节介绍了 HTTP Request 的标准结构, 并建立了四个核心概念: 

- Method: 定义要执行的操作. 

- URL: 定位要访问的资源. 

- Headers: 携带请求的元数据, 如认证信息、数据格式等. 

- Body: 承载真正的业务数据. 

理解这四个部分后, 我们已经具备了阅读任何 HTTP API 文档的基础. 下一节将深入讨论 HTTP Methods, 分析 GET、POST、PUT、DELETE 等方法各自的语义和在自动化中的典型应用. 

# 10.3 HTTP Methods

## Theory

在上一节中, 我们知道一个 HTTP Request 的第一部分就是 Method. 

Method 用来告诉服务器: 

>客户端希望执行什么操作. 

HTTP 协议定义了多种 Method. 

不过, 对于网络自动化工程师来说, 真正需要掌握的主要有以下几种: 

- GET

- POST

- PUT

- PATCH

- DELETE

它们几乎覆盖了绝大多数企业 API 的使用场景. 

## Engineering Discussion

为什么需要 Method? 假设没有 Method, 会发生什么? 

例如: `https://controller.company.com/interfaces`

服务器只能知道客户端访问了 interfaces, 但是服务器不知道客户端到底想干什么. 

例如是不是: 

- 查询接口? 

- 创建接口? 

- 删除接口? 

- 修改接口? 

同一个 URL, 可以执行很多不同的操作. 因此 HTTP 使用 Method 来表达动作(Action). 

于是: GET /interfaces

表示: 获取接口信息. 

而: POST /interfaces

表示: 创建新的接口. 

URL 不变, 动作发生变化, 这就是 Method 存在的意义. 

## GET

GET 的作用, GET 表示: 

>读取(Read)资源. 

GET 不应该修改服务器上的数据, 它只是请求服务器返回已有的信息. 

例如: GET /interfaces

可以理解成: 请把所有接口信息返回给我. 

或者: GET /devices

表示: 获取设备列表. 

对于网络工程师来说, GET 最接近 CLI 中的 `show`

例如: 

```
show version

show ip interface brief

show inventory
```

这些命令都是读取信息, 不会修改设备. 因此在自动化中, 大量的查询操作都会使用 GET. 

### GET 的工程特点

GET 通常具有以下特点: 

- 不修改数据

- 可以重复执行

- 主要用于查询

- 返回服务器已有的数据

因此 GET 非常适合: 

- Inventory 查询

- Compliance 数据获取

- 状态检查

- 监控系统

- Dashboard

## POST

POST 表示: 

>创建(Create)新的资源. 

例如 POST /interfaces 并不是读取接口, 而是创建一个新的 Interface. 服务器真正的数据放在 Body. 

例如: 

```
{
    "name": "Loopback100",
    "ip": "10.100.100.1"
}
```

服务器收到以后创建新的资源. 因此 POST 更接近企业中的 Provisioning. 

### POST 的工程特点

POST 通常: 

- 创建资源

- 提交数据

- 可能产生新的对象

- 服务器状态发生变化

因此 POST 不适合无限重复执行. 

因为: 

第一次, 创建成功. 

第二次, 可能会创建第二个对象. 

或者服务器返回 `Already Exists`. 

## PUT

PUT 表示: 

>整体替换(Replace)资源. 

例如服务器原来保存 

```
Interface

Name = Loopback0

Description = Old

IP = 1.1.1.1
```

客户端发送 PUT: 

```
Name = Loopback0

Description = New

IP = 2.2.2.2
```

服务器通常会认为用新的内容替换整个对象. 而不是只修改 Description. 因此 PUT 更像重新提交整个配置. 

### PUT 的工程特点

PUT 通常: 

- 更新整个对象

- 完整覆盖资源

- 客户端发送完整内容

因此如果遗漏字段, 服务器可能会把遗漏内容删除, 这一点需要特别注意. 

## PATCH

PATCH 与 PUT 很容易混淆. 

PATCH 表示: 局部修改(Partial Update). 

例如原来的配置: 

```
Hostname = R1

Location = DC1

Owner = Network Team
```

如果只想修改 Location. 

PATCH 可以发送 Location = DC2

服务器只修改 Location. 

其他字段保持不变. 

因此 PATCH 更接近日常运维中的修改一个配置项. 而不是重新提交整个配置. 

## PUT 与 PATCH 的区别

这是企业面试中经常出现的问题, 举一个简单例子. 

假设服务器保存: 

```
{
    "hostname":"R1",
    "location":"DC1",
    "owner":"Network"
}
```

PUT: 

```
{
    "hostname":"R1"
}
```

服务器可能认为整个资源就是 hostname 另外两个字段被覆盖掉. 

而 PATCH: 

```
{
    "hostname":"R2"
}
```

服务器通常理解为只修改 hostname, 其他内容保持不变. 

因此 PUT 是 Replace, PATCH 是 Update, 这是最大的区别. 

## DELETE

DELETE 表示删除资源. 

例如: `DELETE /interfaces/Loopback100`

表示删除: Loopback100. 

服务器执行完成后资源消失. 

对于网络工程来说 DELETE 往往对应: 

- 删除对象

- 删除策略

- 删除接口

- 删除 ACL

- 删除配置项

因此 DELETE 操作通常需要更加谨慎. 

## CRUD 思维

在企业开发中, 经常会看到一个术语: 

>CRUD. 

它表示四种最基本的数据操作. 

| Operation | HTTP Method |
| --------- | ----------- |
| Create    | POST        |
| Read      | GET         |
| Update    | PUT / PATCH |
| Delete    | DELETE      |

可以发现 HTTP Method 与 CRUD 几乎是一一对应的. 因此很多 API 文档都会按照 CRUD 来组织. 理解 CRUD, 也就理解了绝大多数 HTTP API 的基本设计. 

## HTTP Methods 与 CLI 的思维差异

在 CLI 中, 我们通常通过不同的命令表达不同的动作: 

`show running-config`

`interface Loopback0`

`no interface Loopback0`

每条命令都包含了: 

- 操作

- 对象

而在 HTTP 中动作与对象被分离. 

例如 GET /interfaces

动作是: GET. 

对象是: interfaces. 

或者 DELETE /interfaces/Loopback0

动作: DELETE. 

对象: Loopback0. 

这种设计使 API 更加统一, 也便于程序自动生成和处理请求. 

## Engineering Insight

对于有 CLI 背景的网络工程师来说, 最大的思维转变之一就是不要把 HTTP Method 理解成命令. 

Method 并不是命令名称, 它表达的是操作语义(Operation Semantics). 

真正的业务对象由 URL 指定, 而 Method 只是说明"对这个对象执行什么操作". 

这种动作(Method)与资源(Resource)分离的设计, 是现代 HTTP API 能够保持一致性和可扩展性的关键原因. 

后续无论学习 Cisco、VMware、AWS 还是其他平台的 API, 你都会不断看到这种模式. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么 HTTP 需要 Method, 而不能只依赖 URL? 

- GET 与 POST 的职责分别是什么? 

- PUT 与 PATCH 的本质区别是什么? 

- 为什么 DELETE 操作通常需要更加谨慎? 

- CRUD 与 HTTP Method 是如何对应的? 

- 为什么说 Method 表达的是操作, 而不是资源? 

## Summary

本节建立了 HTTP Method 的核心工程模型: 

- GET: 读取资源, 不修改服务器状态. 

- POST: 创建新的资源, 通常会新增对象. 

- PUT: 整体替换资源, 提交完整内容. 

- PATCH: 局部更新资源, 仅修改指定字段. 

- DELETE: 删除资源, 需要谨慎使用. 

从这一节开始, 我们已经能够理解绝大多数 API 文档中的请求语义. 下一节将继续学习 HTTP Status Code(HTTP 状态码), 理解服务器如何通过状态码反馈请求的执行结果, 以及自动化程序应如何根据不同状态进行处理. 

# 10.4 HTTP Status Code

很多教程都会把 HTTP Status Code 当成一张需要死记硬背的表格, 但从企业自动化的角度来看, 更重要的是理解: 

>Status Code 不是给人看的, 而是给程序做决策（Decision Making）的. 

Chapter 9 中, 我们通过 Parser 判断 CLI 输出是否符合预期；到了 API 自动化中, 我们首先会根据 Status Code 判断这次请求是否成功, 再决定是否继续后续流程. 

## Theory（理论）

当客户端发送一个 HTTP Request 后, 服务器不会只返回数据, 它还会返回一个 HTTP Status Code（HTTP 状态码）. 

Status Code 的作用是: 

>告诉客户端, 这次请求执行的结果. 

例如: 

- 请求是否成功? 

- 请求格式是否正确? 

- 是否需要身份认证? 

- 请求的资源是否存在? 

- 服务器是否发生异常? 

对于自动化程序来说, Status Code 是判断请求结果的第一依据. 

## Engineering Discussion

### 为什么需要 Status Code? 

假设没有 Status Code. 

客户端发送: GET /devices

服务器返回: {}

这时客户端无法判断这是因为: 

- 没有任何设备? 

- 查询失败? 

- 权限不足? 

- URL 写错? 

- 服务器内部异常? 

仅凭返回的数据, 很难判断真正发生了什么. 

因此, HTTP 协议规定: 

>服务器必须先返回一个状态码. 

例如: 200 OK

表示: 请求已经成功处理. 

或者: 404 Not Found, 表示: 请求的资源不存在. 

因此, 一个 HTTP Response 可以简化表示为: 

```
HTTP Response
│
├── Status Code
├── Headers
└── Body
```

其中, Status Code 永远是自动化程序首先关注的内容. 

## Status Code 的分类

HTTP 状态码采用三位数字, 真正重要的是第一位数字. 第一位数字决定了这一类状态码的含义. 

| 范围  | 含义                  |
| --- | ------------------- |
| 1xx | 信息（Informational）   |
| 2xx | 成功（Success）         |
| 3xx | 重定向（Redirection）    |
| 4xx | 客户端错误（Client Error） |
| 5xx | 服务器错误（Server Error） |

对于网络自动化来说真正需要重点掌握的是: 

- 2xx

- 4xx

- 5xx

1xx 和 3xx 在大多数 API 自动化场景中较少直接处理, 因此本章不深入展开. 

### 2xx —— Success（成功）

2xx 表示: 服务器已经成功处理请求. 

其中最常见的是: 200 OK

表示: 请求成功. 

例如: GET /devices

服务器: 200 OK

随后返回设备列表. 

这表示请求已经完成, 程序可以继续处理返回的数据. 

另一个常见状态码是: 201 Created

表示: 服务器成功创建了新的资源. 

例如: POST /interfaces

服务器: 201 Created

说明: Loopback Interface 已经成功创建. 

还有: 204 No Content

表示: 请求成功, 

但是没有返回任何数据. 

例如删除一个对象: DELETE /interfaces/Loopback100

服务器可能返回: 204 No Content

表示: 删除成功. 

只是没有内容需要返回. 

### 4xx —— Client Error（客户端错误）

4xx 并不是服务器坏了, 它表示客户端发送的请求存在问题. 也就是说服务器能够正常工作, 但是客户端请求不正确. 因此自动化程序首先应该检查自己. 

最常见的是: 400 Bad Request

表示: 请求格式错误. 

例如: JSON 格式不正确. 

或者: 缺少必须字段, 服务器无法解析请求. 

另一个非常重要的是: 401 Unauthorized

表示: 身份认证失败. 

例如: 用户名或 Token 错误. 

服务器不会执行请求. 这里需要注意401 表示尚未通过身份认证. 它通常意味着: 程序需要提供正确的认证信息. 

还有: 403 Forbidden

表示: 已经完成身份认证, 

但是: 没有权限执行当前操作. 

例如: 普通用户尝试删除系统配置. 服务器知道你是谁, 但拒绝执行, 这与 401 有本质区别. 

再来看: 404 Not Found

表示: 请求的资源不存在. 

例如: GET /devices/R100

而服务器只有: 

- R1

- R2

- R3

那么服务器可能返回: 404 Not Found

说明: URL 本身是正确的, 

但是目标资源不存在. 

## 5xx —— Server Error（服务器错误）

5xx 表示: 服务器在处理请求时发生了异常. 这里的问题通常不在客户端, 而是在服务器. 

例如: 500 Internal Server Error

表示: 服务器内部发生异常. 

可能是: 

- 软件 Bug

- 后端数据库异常

- 服务崩溃

- 未处理的程序错误

对于自动化程序来说, 通常应该: 

- 记录日志

- 重试（根据业务场景决定）

- 终止当前工作流或进入异常处理流程

而不是盲目继续执行. 

另一个常见状态码是: 503 Service Unavailable

表示: 服务暂时不可用. 

例如: 服务器正在维护. 

或者: 负载过高. 

这种情况往往是临时性的. 

与 500 不同, 503 在很多企业系统中适合结合有限次数的重试机制, 但具体的重试策略属于后续章节讨论的内容. 

## Status Code 与 Enterprise Workflow

回顾 Chapter 9. 我们当时是这样工作的: SSH ➡ CLI Output ➡ Parser ➡ Compliance

因为 CLI 没有统一的状态反馈, 所以必须先解析输出. 

而在 API 中第一步通常变成: 

HTTP Request ➡ Status Code ➡ Body ➡ Business Logic

也就是说只有当 Status Code 表明请求成功时, 程序才会继续处理 Body 中的数据. 这是一种更加稳定、更加标准化的工作流程. 

## Engineering Best Practice

在企业自动化开发中, 不建议: 发送请求 ➡ 直接解析返回数据

更推荐: 发送请求 ➡ 检查 Status Code ➡ 确认请求成功 ➡ 解析 Body ➡ 执行业务逻辑

原因很简单, 假设服务器返回 404 Not Found.

Body 中可能只有: 

```
{
    "error":"Device Not Found"
}
```

如果程序直接把它当作正常业务数据处理, 就可能产生错误的判断. 

因此先检查 Status Code, 再处理数据, 应当成为整个自动化平台的统一规范. 

## Engineering Insight

对于网络工程师来说, Status Code 可以理解为 CLI 世界中的命令是否执行成功, 但两者并不完全相同. 

CLI 通常依赖: 

- 输出内容

- 错误提示

- 关键字匹配

来判断执行结果. 

而 HTTP 提供了统一的状态反馈机制. 

这意味着自动化程序无需解析错误提示文本, 只需根据标准化的 Status Code, 就能快速决定下一步如何处理. 这也是 HTTP API 比 CLI 更适合程序自动化的重要原因之一. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- HTTP Status Code 的作用是什么? 

- 为什么程序应先检查 Status Code, 而不是直接解析返回数据? 

- 2xx、4xx、5xx 分别表示什么类型的结果? 

- 401 与 403 有什么区别? 

- 404 表示什么? 它一定意味着服务器不可用吗? 

- 为什么 5xx 错误通常意味着需要记录日志并进入异常处理流程? 

## Summary

本节建立了 HTTP Status Code 的工程模型: 

- 2xx: 请求成功, 可以继续处理返回数据. 

- 4xx: 客户端请求存在问题, 应检查请求内容、认证或资源路径. 

- 5xx: 服务器处理异常, 应进行日志记录和错误处理, 而不是继续执行业务逻辑. 

至此, 我们已经理解了 HTTP 通信中的两个核心元素: 

- Request: 客户端如何表达自己的请求. 

- Status Code: 服务器如何反馈请求结果. 

# 10.5 URL, Endpoint & Resource

## Theory

上一节我们学习了 HTTP Method. 

Method 决定我要做什么, 但是服务器仍然不知道我要操作什么. 

例如：GET

仅仅说明：读取数据, 但是读取：

- 哪个设备? 

- 哪个接口? 

- 哪个 VLAN? 

- 哪个用户? 

这些信息由 URL 提供. 

因此：

> 一个完整的 HTTP Request 至少需要回答两个问题：

我要做什么?  ➡ Method ➡ 我要操作什么? ➡ URL

Method 与 URL 共同决定了一次请求的含义. 

## Engineering Discussion

### URL 的作用

URL（Uniform Resource Locator, 统一资源定位符）的作用非常简单告诉服务器, 请求发送到哪里. 

例如：`https://controller.company.com/devices`

表示：客户端希望访问 devices 这一类资源. 

如果：`https://controller.company.com/interfaces`

那么请求的对象变成了 interfaces

可以发现 Method 决定动作, URL 决定对象, 二者缺一不可. 

## 从网络工程师的角度理解 URL

回忆一下 CLI, 我们通常这样操作：`show ip interface brief` 这里实际上包含了两个信息：

第一：动作 show

第二：对象 ip interface

CLI 把动作, 对象写在一条命令里面, 而 HTTP 将它们进行了分离. 

例如：GET ➡ /interfaces

动作：GET

对象：interfaces. 

这种设计更加规范, 也是现代 API 的基本思想. 

## 什么是 Resource（资源）? 

Resource 是整个 API 世界最重要的概念之一. 

可以简单理解成：API 所管理的对象. 

例如一个网络控制器可能管理：

- Device

- Interface

- VLAN

- ACL

- User

- Policy

这些都是 Resource. 

注意 Resource 不是一个命令, 而是一个对象. 

例如：

Device 就是一种 Resource. 

Interface 也是一种 Resource. 

## Resource 与 CLI 的区别

CLI 更关注如何操作. 

例如：

```
show interface

configure terminal

interface GigabitEthernet0/0
```

API 更关注操作哪个对象. 

例如：/interfaces

表示：接口资源. 

而：/acl

表示：ACL 资源. 

这种设计意味着不同的操作可以作用于同一个 Resource. 

例如：GET /interfaces 读取接口. 

POST /interfaces 创建接口. 

DELETE /interfaces/Loopback0 删除接口. 

可以发现真正变化的是 Method. 

Resource 一直都是 interfaces. 

## Endpoint（接口端点）

很多 API 文档都会反复出现 Endpoint. 

例如：

```
GET /devices

POST /devices

GET /interfaces
```

每一个都可能被称为一个 Endpoint. 从工程角度, 可以把 Endpoint 理解为服务器提供的一个可访问接口. 

例如：

/devices 就是一个 Endpoint. 

/interfaces 也是一个 Endpoint. 

客户端可以向这些位置发送请求. 

服务器会根据：

```
Method

URL
```

共同决定执行什么操作. 

## URL 与 Endpoint 的关系

很多初学者会把 URL, Endpoint 认为完全一样. 实际上它们并不是同一个概念. 

例如：`https://controller.company.com/api/v1/interfaces`

完整的是 URL

而 `/api/v1/interfaces`

通常称为 API Endpoint. 

也就是说 Endpoint 更强调服务器暴露出来的 API 接口, URL 更强调客户端访问资源所使用的完整地址, 在很多日常交流中, 两者经常混用, 但理解它们的侧重点, 有助于阅读正式的 API 文档. 

## 一个完整请求是如何定位资源的? 

现在, 我们已经具备了三个核心概念：

Method ➡ Resource ➡ Endpoint

例如：

GET ➡ /devices 

表示：读取所有 Device Resource. 

如果 GET ➡ /devices/R1

则表示：读取编号为 R1 的 Device Resource. 

如果 DELETE ➡ /devices/R1

则表示：删除 R1

因此 Method 决定做什么, URL / Endpoint 决定作用于哪个 Resource. 

## Engineering Architecture

站在 Enterprise Automation Platform 的角度来看, HTTP Request 可以进一步抽象成：

Business Logic ➡ Operation ➡ Method ➡ Resource ➡ Endpoint ➡ HTTP Request

例如：

Business Logic 获取所有设备

最终可以转换为：GET ➡ /devices

Business Logic 删除接口

最终可以转换为：DELETE ➡ /interfaces/Loopback0

注意业务逻辑描述的是"我要完成什么业务"; HTTP Request 描述的是"如何向服务器表达这个业务". 

这是 Layered Architecture 的体现：上层关注业务, 下层关注通信细节. 

## Engineering Insight

阅读 API 文档时, 不要先看代码示例, 而应先识别三个问题：

- Resource 是什么? 

- 这个 Resource 对应哪些 Endpoint? 

- 每个 Endpoint 支持哪些 Method? 

只要回答了这三个问题, 就已经理解了一个 API 的基本结构. 

不同厂商的 API 在命名和组织方式上会有所差异, 但这种围绕 Resource + Method 的设计思想在现代 HTTP API 中非常普遍. 

## Engineering Checklist

完成本节后, 应能够回答以下问题：

- URL 在 HTTP Request 中承担什么职责? 

- Resource 与 CLI 中的命令有什么区别?

- Endpoint 可以如何理解? 

- URL 与 Endpoint 的侧重点有什么不同? 

- 为什么同一个 Resource 可以对应多个不同的 Method? 

- 如何从 Business Logic 映射到 HTTP Request? 

## Summary

本节建立了 HTTP API 中用于定位操作对象的核心概念：

- URL：客户端访问资源的完整地址. 

- Endpoint：服务器暴露出的可访问 API 接口. 

- Resource：API 所管理的业务对象, 如 Device、Interface、VLAN 等. 

至此, 我们已经理解了一个 HTTP Request 的三个关键组成部分：

- Method：执行什么操作. 

- URL / Endpoint：操作哪个资源. 

- Resource：被操作的业务对象. 

# 10.6 HTTP Headers

Theory

在上一节中, 我们已经知道, 一个 HTTP Request 主要包含四个组成部分: 

```
HTTP Request
│
├── Method
├── URL
├── Headers
└── Body
```

Method 决定做什么, URL 决定操作哪个资源, 那么Headers 又负责什么? 答案是描述这次通信, 而不是描述业务. 这是理解 HTTP Header 最重要的一句话. 

## Engineering Discussion

### Header 的职责

可以把 Header 理解成请求的元数据(Metadata). 它不会告诉服务器创建哪个接口. 也不会告诉服务器接口 IP 地址是多少. 

这些属于业务数据(Business Data). Header 负责的是告诉服务器, 如何理解这次请求. 

例如: 

- 数据是什么格式? 

- 客户端希望接收什么格式的数据? 

- 身份认证信息是什么? 

- 是否启用压缩? 

- 使用什么语言? 

这些信息都属于 Header. 

一个生活中的例子

假设我们要寄一个包裹. 包裹里面放的是: 

- Loopback0

- IP Address

- Description

这些就是真正的业务数据, 而快递单上写的是: 

- 寄件人

- 收件人

- 联系电话

- 是否加急

这些并不是包裹里面的内容, 它们只是帮助快递公司完成运输, HTTP Header 的作用与此类似, 它不是业务内容, 而是帮助服务器正确处理请求. 

## Header 与 Body 的职责划分

这是企业开发中非常重要的一条原则. 

可以简单总结为: 

| Header   | Body          |
| -------- | ------------- |
| 描述通信     | 描述业务    |
| Metadata | Business Data |
| 请求如何处理   | 请求处理什么        |

例如: 假设我们希望创建一个新的 Interface. 

真正的接口信息: 

```
Interface = Loopback100

IP = 10.1.1.1

Description = Management
```

应该放在 Body, 而不是 Header. 

如果告诉服务器我是 JSON 格式. 

这属于 Header. 因为它描述的是数据格式. 而不是接口配置. 

## 为什么要区分 Header 与 Body? 

很多初学者会问既然都是发送给服务器, 为什么还要分两个地方? 

原因在于职责不同. 

例如: 服务器收到请求以后, 首先需要回答我应该如何解析这些数据? 

如果不知道数据到底是什么格式, 服务器甚至无法读取真正的数据. 

因此 Header 通常会先被处理. 随后服务器再解析 Body. 

整个流程可以表示为: 

HTTP Request ➡ 读取 Headers ➡ 确定通信方式 ➡ 解析 Body ➡ 执行业务逻辑

因此 Header 更接近通信层, Body 更接近业务层. 

## 常见 Header 类型

虽然 HTTP Header 有很多种, 但对于自动化工程师来说, 最常见的几类只有以下几种. 

### Content-Type

Content-Type 告诉服务器请求体(Body)采用什么数据格式. 

例如: 后续章节中, 我们会大量使用: application/json

表示: Body 是 JSON. 

服务器收到以后, 就会按照 JSON 进行解析. 

如果: Content-Type 与实际数据格式不一致, 服务器可能无法正确处理请求. 

### Accept

Accept 表示客户端希望服务器返回什么格式的数据. 

例如: 客户端可以告诉服务器请返回 JSON. 

服务器如果支持, 就会按照请求的格式返回数据. 

这里要注意: 

- Content-Type 描述的是"我发送给你的数据是什么格式". 

- Accept 描述的是"我希望你返回给我的数据是什么格式". 

它们分别对应请求和响应, 职责不同. 

### Authorization

很多企业 API 都需要身份认证. 

客户端需要告诉服务器我是谁. 

这类认证信息通常放在 Authorization Header. 

至于: 

- 用户名密码

- Token

- 其他认证机制

不同平台实现不同, 本章只建立概念. 具体认证方式将在后续章节结合实际 API 介绍. 

## Header 在 Enterprise Automation Platform 中的位置

回到我们的平台架构. 

Business Logic: 创建 Device 并不会关心 Header 如何构造. 它只关心
业务. 真正负责组织 HTTP Request 的, 应该是 Connection Layer. 

例如: 

Business Logic ➡ Connection Layer ➡ Method ➡ URL ➡ Headers ➡ Body

可以看到 Header 属于通信层的一部分, 而不是业务逻辑的一部分. 

这与前面一直强调的 Business Logic Separation 完全一致. 

如果未来认证方式发生变化, 

例如: Token 更新, 或者需要增加新的 Header, 理论上 Business Logic 不需要修改, 只需要调整 Connection Layer 的实现即可. 

## Engineering Best Practice

在企业项目中, 不建议让业务代码到处拼接 Header. 

例如: 

```python
#不推荐(示意)

create_device()

↓

手动添加 Authorization

↓

手动添加 Content-Type

↓

发送请求
```

更合理的做法是由 Connection Layer 统一负责构建 Header. 

业务模块只描述我要完成什么业务. 

这样可以避免

- 重复代码

- Header 不一致.

- 认证方式分散

- 后期维护困难

这种职责划分, 与我们在 Chapter 8 和 Chapter 9 中建立的工程思想保持一致. 

## Engineering Insight

对于网络工程师来说, 可以把 Header 理解为通信协议的配置, 而不是网络设备的配置. 配置设备接口、ACL、路由等属于业务数据, 应放在 Body 中, 而认证方式、数据格式、压缩方式等属于通信行为, 应放在 Header 中. 这种区分不仅符合 HTTP 协议的设计原则, 也有助于保持自动化平台各层职责清晰. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- Header 的职责是什么? 

- 为什么说 Header 描述的是通信, 而不是业务? 

- Header 与 Body 的职责有什么区别? 

- Content-Type 与 Accept 分别表示什么? 

- Authorization Header 的作用是什么? 

- 为什么 Header 应由 Connection Layer 统一管理, 而不是由 Business Logic 自行构造? 

## Summary

本节建立了 HTTP Header 的工程模型: 

- Header: 承载请求的元数据(Metadata), 描述通信方式. 

- Body: 承载真正的业务数据(Business Data). 

- Content-Type: 声明请求体的数据格式. 

- Accept: 声明客户端期望的响应格式. 

- Authorization: 携带身份认证信息. 

到目前为止, 我们已经完整理解了一个 HTTP Request 的四个组成部分: 

- Method: 执行什么操作. 

- URL / Endpoint: 操作哪个资源. 

- Headers: 如何进行通信. 

- Body: 传递什么业务数据. 

# 10.7 HTTP Body & JSON Payload

## Theory

在前面的内容中, 我们已经学习了一个 HTTP Request 由四个部分组成: 

```
HTTP Request
│
├── Method
├── URL
├── Headers
└── Body
```

其中: 

- Method 表示执行什么操作. 

- URL 表示操作哪个资源. 

- Headers 描述如何通信. 

那么真正的业务数据放在哪里? 

答案就是 HTTP Body(请求体). 

## Previous Chapter Review

在 Chapter 6 — YAML / JSON 中, 我们已经学习了 JSON. 当时, JSON 的定位是一种通用的数据交换格式(Data Exchange Format). 

当时我们主要用于: 

- 保存 Inventory

- 保存变量

- 文件之间交换数据

例如: inventory/ ➡ JSON File ➡ Python

JSON 的作用是存储数据. 到了 Chapter 10 JSON 的角色发生了变化, 它不再只是保存在磁盘上的文件, 而是作为 HTTP Body 在网络上传输. 

## Engineering Discussion

### HTTP Body 的职责

HTTP Body 可以理解成真正承载业务数据的地方. 

例如: 创建一个新的设备. 

真正需要告诉服务器的信息包括: 

- Hostname

- Management IP

- Location

这些都属于业务数据(Business Data). 

因此它们应该放入 HTTP Body, 而不是 Headers. 

### 什么是 Payload? 

阅读 API 文档时, 你会经常看到一个术语 Payload

很多初学者会疑惑 Payload 和 Body 是不是两个不同的概念? 

实际上在 HTTP API 的上下文中, 通常可以简单理解为 Payload 就是 Body 中承载的业务数据. 

例如: 发送一个创建设备请求Body 中包含: 

```json
{
    "hostname": "R1",
    "management_ip": "10.1.1.1"
}
```

这里的 JSON 内容, 就是 Payload. 因此可以简单记住: 

HTTP Request ➡ Body ➡ Payload(真正的数据)

虽然在更广义的网络通信中, Payload 的含义更宽泛, 但在本 Workbook 当前阶段, 将其理解为 HTTP Body 中承载的业务数据即可. 

## 为什么 API 普遍使用 JSON? 

HTTP 协议本身并没有规定 Body 必须使用 JSON. 

理论上 Body 可以是: 

- XML

- JSON

- HTML

- Plain Text

- Binary Data

- 图片

- 文件

HTTP 并不关心. 

真正决定格式的是 Content-Type. 

例如: Content-Type: application/json

表示: Body 是 JSON. 

现代 API 之所以大量采用 JSON, 主要有以下几个原因: 

- 结构清晰, 适合表示对象关系. 

- 体积相对较小, 传输效率较高. 

- 人类容易阅读. 

- 几乎所有编程语言都原生支持 JSON. 

- 与 JavaScript 天然兼容, 因此 Web 技术生态广泛采用. 

因此 JSON 已逐渐成为现代 HTTP API 最常见的数据交换格式. 

需要强调的是这是行业实践, 而不是 HTTP 协议的强制要求. 

## JSON 在 Enterprise Automation Platform 中的位置

回顾 Chapter 6. JSON 的位置是: 

Inventory File ➡ JSON ➡ Python

而现在 JSON 出现在: 

Python ➡ HTTP Body ➡ API Server

可以发现 JSON 没有改变. 改变的是它所处的位置. 以前JSON 是文件中的数据. 现在 JSON 是网络上传输的数据. 

因此 Chapter 10 并没有学习新的 JSON, 而是学习JSON 在 API 通信中的作用. 

## 一个完整的 HTTP Request

到目前为止我们已经能够完整描述一个 HTTP Request. 

例如: 

```
HTTP Request

Method
    │
    ▼
POST

URL
    │
    ▼
/devices

Headers
    │
    ▼
Content-Type: application/json

Body
    │
    ▼
JSON Payload
```

可以看到四个组成部分各司其职: 

- Method: 描述操作. 

- URL: 定位资源. 

- Headers: 描述通信方式. 

- Body: 承载业务数据. 

这也是现代 HTTP API 最典型的请求结构. 

## 与前面章节的联系

现在, 把 Chapter 6、Chapter 8、Chapter 9 和 Chapter 10 联系起来, 就可以看到整个知识体系的演进. 

```
Chapter 6

JSON
↓
Python Object
────────────────────────────
Chapter 8

Inventory
↓
Renderer
↓
Deployment
────────────────────────────

Chapter 9

CLI Output
↓
Parser
↓
Compliance

────────────────────────────

Chapter 10

Python Object
↓
JSON Payload
↓
HTTP Body
↓
API Server
```

可以看到, 前面的知识并没有被推翻. 而是在新的通信方式中得到了复用. 这也是整个 Workbook 一直坚持的知识递进, 而不是知识重复. 

## Engineering Best Practice

在企业项目中, 业务模块应尽量关注我要发送哪些业务数据. 

而不要关心: 

- JSON 如何序列化. 

- HTTP Body 如何构造. 

- Content-Type 如何设置. 

这些工作更适合由 Connection Layer 或 API Client 统一完成. 

这样做有两个好处: 

1. Business Logic 保持简洁, 只描述业务. 

2. 如果未来数据格式发生变化(例如某些 API 使用 XML), 只需调整通信层, 而无需修改业务逻辑. 

这也是 Layered Architecture 带来的长期维护优势. 

## Engineering Insight

很多网络工程师认为学 API 就是在学 JSON. 实际上并非如此, JSON 只是数据表示方式(Representation). 

真正需要理解的是: 

- 如何组织请求(Method、URL、Headers、Body)

- 如何表达业务(Payload)

- 如何建立通信(HTTP)

即使未来某些平台使用 XML 或其他格式, 这套通信模型依然成立. 

因此, 在自动化平台中, 我们关注的是通信模型, 而不是某一种具体的数据格式. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- HTTP Body 的职责是什么? 

- Payload 与 Body 在当前阶段可以如何理解? 

- 为什么现代 API 普遍采用 JSON? 

- JSON 在 Chapter 6 与 Chapter 10 中分别承担什么角色? 

- 为什么 JSON 不是 HTTP 协议唯一支持的数据格式? 

- 为什么 Business Logic 不应该直接负责构造 HTTP Body? 

## Summary

本节完成了 Chapter 6 与 Chapter 10 的知识衔接: 

- Body: 承载业务数据. 

- Payload: 通常指 Body 中真正传输的业务内容. 

- JSON: 在 Chapter 10 中作为 HTTP Body 的主要数据格式, 而不是新的知识点. 

- Connection Layer: 负责将业务数据组织成 HTTP 请求. 

- Business Logic: 只关注业务对象和业务含义, 而不关心底层通信细节. 

# 10.8 Python HTTP Client

Theory

到目前为止, 我们已经完整学习了 HTTP 通信模型. 

一个 HTTP Request 包括 Method ➡ URL ➡ Headers ➡ Body 但是还有一个问题没有回答. 

Python 如何发送一个 HTTP Request? 仅仅理解 HTTP 协议还不够, 我们还需要一个能够代表客户端(Client)与服务器通信的工具. 

这就是 HTTP Client. 

## Engineering Discussion

### Client 与 Server

HTTP 是一种典型的 Client-Server Architecture(客户端-服务器架构). 

例如: 

Python ➡ HTTP Client ➡ Internet / Network ➡ HTTP Server

其中 Python 程序属于 Client. 

API 所在的软件属于 Server. 

整个通信都是由 Client 发起, Server 响应. 这一点与 SSH Automation 非常类似. 

例如 Chapter 3: 

Python ➡ Netmiko ➡ SSH ➡ Network Device

这里 Netmiko 就充当了 SSH Client. 

同样 HTTP Automation 也需要 HTTP Client. 

## 什么是 HTTP Client? 

HTTP Client 可以理解为: 

>负责发送 HTTP Request, 并接收 HTTP Response 的软件组件. 

它负责完成: 

- 建立 TCP 连接

- 发送 HTTP Request

- 接收 HTTP Response

- 解析 HTTP 协议细节

- 将结果返回给 Python

因此我们的 Python 代码并不会直接操作 TCP, 也不会自己拼接 HTTP 报文. 这些工作全部由 HTTP Client 完成. 

## 为什么需要 HTTP Client? 

理论上 Python 完全可以自己构造: 

```
GET /devices HTTP/1.1
Host: server.example.com
...
```

然后通过 Socket 发送, 但是这样开发效率极低, 而且需要自己处理: 

- TCP

- HTTP

- Header

- 超时

- 重定向

- SSL

- 编码

因此几乎所有 Python 项目, 都会使用成熟的 HTTP Client Library. 

这与 Chapter 3 中几乎没有人自己实现 SSH 协议, 而是使用 Netmiko 的原因完全一致. 

## Python 的 HTTP Client

Python 标准库已经提供了 HTTP Client, 但是标准库更偏向底层, 代码通常比较繁琐. 因此企业开发中, 几乎都会使用 requests 作为 HTTP Client Library. 

需要强调的是 requests 不是 HTTP 协议, 它只是 HTTP 的一个 Python 实现. 就像 Netmiko 不是 SSH, 只是 SSH Client Library. 因此不要把 HTTP 和 requests 混为一谈. 

二者关系可以表示为: 

HTTP ➡ 通信协议 ➡ requests ➡ Python Library

## requests 在平台中的定位

回顾之前的章节. 

Chapter 3: 

Business Logic ➡ Connection Module ➡ Netmiko ➡ SSH

可以发现 Business Logic 不知道 Netmiko. 真正知道 Netmiko 的, 是 Connection Module. 

API Automation 也是一样, 未来的平台: 

Business Logic ➡ Connection Module ➡ requests ➡ HTTP

Business Logic 仍然不知道 requests, 它只知道获取设备, 或者创建接口. 真正负责 HTTP 通信的, 应该仍然是 Connection Layer. 

## 为什么不能到处调用 requests? 

很多初学者会写: 

```python
requests.get(...)

requests.post(...)

requests.put(...)
```

散落在整个项目里面. 这种方式虽然可以运行, 但是工程上存在很多问题. 

例如: 认证方式发生变化. 

需要修改几十个文件. 

或者统一增加 Timeout. 

又需要修改所有 requests. 

随着项目越来越大, 维护成本会快速增加. 因此企业工程更推荐: 

Business Logic ➡ API Client ➡ requests ➡ HTTP

Business Logic 只调用: 

```python
get_device()

create_vlan()

delete_acl()
```

至于里面到底调用了 requests, 还是其他 HTTP Client 业务层完全不需要知道. 

## API Client 的职责

因此, 在 Enterprise Automation Platform 中, API Client 更适合承担以下职责: 

- 构造 HTTP Request

- 添加统一的 Headers

- 处理认证信息

- 设置 Timeout

- 发送请求

- 接收 Response

- 检查 Status Code

- 返回处理结果

而 Business Logic 继续保持只关注业务. 这与前面章节建立的 Layered Architecture 保持完全一致. 

与 SSH Automation 的对比现在可以发现, SSH 与 HTTP 的整体架构非常相似. 

| SSH Automation    | API Automation |
| ----------------- | -------------- |
| SSH Protocol      | HTTP Protocol  |
| Netmiko           | requests       |
| Connection Module | API Client     |
| Business Logic    | Business Logic |

虽然通信协议不同, 但是整个工程设计没有发生变化. 这正是我们一直强调的平台稳定, 通信方式可替换. 

## Engineering Insight

这里需要特别强调一个容易混淆的概念. 很多教程会说 "requests 就是 API. " 这种说法并不准确. 

实际上: 

HTTP API ➡ 通信规范 ➡ requests ➡ Python 工具

requests 并不会定义 API. 真正定义 API 的是服务器. requests 只是帮助客户端按照 HTTP 协议去访问这些 API. 

理解这一点, 有助于后续阅读不同厂商的 API 文档, 也能避免把某个 Python 库与协议本身混为一谈. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 什么是 HTTP Client? 

- 为什么 Python 不直接操作 TCP 来发送 HTTP 请求? 

- HTTP 与 requests 的关系是什么? 

- requests 与 Netmiko 在整个 Workbook 中分别承担什么角色? 

- 为什么 Business Logic 不应该直接调用 requests? 

- API Client 在 Enterprise Automation Platform 中应承担哪些职责? 

## Summary

本节建立了 Python HTTP Client 的工程定位: 

- HTTP: 通信协议. 

- requests: HTTP 的 Python 客户端库. 

- API Client: 平台中的通信组件, 统一管理 HTTP 请求. 

- Business Logic: 不直接依赖 requests, 而是通过 API Client 完成通信. 

至此, 我们已经完成了从 HTTP 协议 → HTTP 请求 → HTTP 响应 → JSON Payload → HTTP Client 的理论基础. 

# Lab 1 Use Requests send first HTTP Request

## Theory

在 [Chapter 10.8](<Chapter 10.8 Python HTTP Client.md>) 已经介绍了: 

- HTTP 是通信协议

- requests 是 Python 的 HTTP Client Library

这一节开始, 我们第一次使用 requests. 

目标只有一个**完成一次 HTTP GET 请求**. 

暂时不考虑: 

- 身份认证

- JSON Payload

- POST

- PUT

- DELETE

- 企业 API

我们只关注 **Python 如何发送 HTTP Request, 并接收 HTTP Response.**

## Engineering Discussion

### 为什么选择 GET? 

HTTP Method 有很多: 

- GET

- POST

- PUT

- PATCH

- DELETE

其中 GET 最容易理解, 因为 GET 不会修改服务器的数据, 它只是读取资源. 

这与我们在 CLI 中执行: 

```
show version

show interface

show inventory
```

非常类似. 

因此第一段代码选择 GET, 是最自然的学习路径. 

### 为什么暂时使用公共测试 API? 

目前我们的 Enterprise Automation Platform 还没有接入任何真实的网络控制器. 

如果直接使用某个厂商的 API: 

- 需要账号

- 需要认证

- 需要实验环境

- 需要提前介绍厂商平台

这违反了 Workbook 的 Roadmap. 

因此我们先使用一个公开提供的测试 API. 

它的唯一作用就是**帮助我们理解 HTTP 通信.**

后面学习具体网络平台时, 再替换为真实的 API Endpoint. 

## Hands-on Lab

### 安装 requests

首先确认已经安装 requests. 

```bash
pip install requests
```

安装完成后, 可以验证版本: 

```bash
pip show requests
```

### 第一个程序

创建: `scripts/http_get.py`

代码如下: 

```
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

print(response)
```

运行: `python3 scripts/http_get.py`

输出类似: `<Response [200]>`

## Engineering Analysis

虽然只有一行输出: `<Response [200]>`

但实际上已经完成了一次完整的 HTTP 通信. 

整个过程如下: 

```
Python Program
        │
        ▼
requests.get()
        │
        ▼
HTTP Request
        │
        ▼
Internet
        │
        ▼
API Server
        │
        ▼
HTTP Response
        │
        ▼
Response Object
```

需要注意返回的并不是 JSON

而是 Response Object

也就是说服务器返回的数据, 已经被 requests 封装成了一个 Python 对象. 这一点与 Netmiko 十分相似. 

例如: `output = connection.send_command(...)`

返回的是: CLI 输出. 

而: `response = requests.get(...)`

返回的是: Response Object. 

后续所有信息例如: 

- Status Code

- Headers

- JSON Body

都是从这个对象中获取. 

## 查看 Status Code

上一节学习过 Status Code 是程序首先应该检查的内容. 

因此修改程序: 

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

print(response.status_code)
```

运行: `python3 scripts/http_get.py`

输出: 200

说明服务器已经成功处理请求. 

这里再次验证了上一节建立的工程原则: 

HTTP Request → Status Code → Business Logic

程序首先获得: Status Code. 

然后才决定是否继续处理数据. 

## 查看 Response Body

服务器真正返回的数据位于 Response Body. 

可以使用 `print(response.text)`

输出类似: 

```
{
  "userId": 1,
  "id": 1,
  "title": "...",
  "body": "..."
}
```

可以发现 Body 中保存的是 JSON 数据. 

这正好对应上一节学习的: 

HTTP Response → Body → JSON Payload

## Response Object 提供了什么? 

目前我们已经接触到三个最重要的属性. 

| 属性                   | 作用          |
| -------------------- | ----------- |
| response.status_code | 获取 HTTP 状态码 |
| response.text        | 获取响应内容（字符串） |
| response.headers     | 获取响应头       |

后续章节还会介绍: 

- `response.json()`

- `response.content`

- `response.raise_for_status()`

目前无需提前学习, 保持知识递进. 

## 与 Enterprise Automation Platform 的关系

目前代码直接写成: 

```python
response = requests.get(url)
```

只是为了帮助理解 requests 的基本使用. 这不是最终的工程实现. 

按照前面建立的架构: 

Business Logic → API Client → requests → HTTP

未来: `requests.get()`

不会散落在业务代码中, 而是统一封装到 `modules/` 中的 API Client 模块. 

本节只是验证 Python 已经具备发送 HTTP Request 的能力. 

## Engineering Best Practice

虽然目前代码非常简单: 

```python
response = requests.get(url)
```

但在企业项目中, 应逐步养成以下习惯: 

- 始终检查 status_code, 不要假设请求一定成功. 

- 不要立即解析返回内容, 先确认请求是否成功. 

- 避免在业务代码中大量直接调用 requests.get(), 后续将统一封装到 API Client 中. 

- 保持通信逻辑与业务逻辑分离, 继续遵循 Workbook 的 Layered Architecture. 

这些原则将在后续实验中不断强化. 

## Engineering Checklist

完成本实验后, 应能够回答以下问题: 

- `requests.get()` 的作用是什么? 

- `requests.get()` 返回的是 JSON, 还是 Response Object? 

- 如何获取 HTTP Status Code? 

- 如何获取 Response Body? 

- 为什么程序应先检查 `status_code`, 再处理响应内容? 

- 为什么当前示例代码不是最终的企业工程实现? 

## Summary

本实验完成了 Chapter 10 的第一次 HTTP 通信: 

- 使用 `requests` 发送了一个 GET Request. 

- 获得了 Response Object. 

- 读取了 Status Code. 

- 查看了 Response Body. 

- 验证了 HTTP Request → HTTP Response 的完整流程. 

# Lab 2 parse HTTP Response

Theory(理论)

上一节我们使用：

```python
response.text
```

查看了服务器返回的数据. 

虽然看到的是 JSON 格式：

```json
{
    "userId": 1,
    "id": 1,
    "title": "...",
    "body": "..."
}
```

但是需要注意 response.text 返回的是字符串(String). 而不是 Python Dictionary, 这一点非常重要. 

## Engineering Discussion

### 为什么不能直接处理 response.text? 

假设服务器返回：

```json
{
    "hostname": "R1",
    "ip": "10.1.1.1"
}
```

如果：`print(response.text)`

Python 得到的是：`'{"hostname":"R1","ip":"10.1.1.1"}'`

注意两边的：`'`

说明这是一个字符串, 字符串虽然可以打印, 但是不能直接：`response.text["hostname"]`

因为字符串没有 hostname 这个字段. 因此自动化程序真正需要的是 Python Object. 而不是 JSON String. 

### requests 如何处理 JSON? 

requests 已经帮我们准备好了一个非常方便的方法：

```python
response.json()
```

它的作用不是获取 JSON. 而是将 Response Body 中的 JSON 转换成 Python 对象, 这一点要特别注意. 

很多初学者容易认为：`response.json()` 返回 JSON. 实际上 JSON 是一种文本格式. Python 并不存在 JSON 类型. 真正返回的是 Python Object. 

通常是：

- dict

- list

取决于服务器返回的数据. 

## Hands-on Lab

修改程序：

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

data = response.json()

print(data)
print(type(data))
```

运行：`python3 scripts/http_get.py`

输出: `<class 'dict'>`

可以看到 requests 已经把 JSON 自动转换为了 Python Dictionary. 

## 访问数据

现在 data 已经不是字符串, 因此可以直接访问字段. 

例如：

```python
print(data["id"])
print(data["title"])
print(data["body"])
```

输出类似：

```
1

sunt aut facere...

quia et suscipit...
```

这里已经完全没有 JSON Parser. 因为 requests 已经完成了转换. 

## 与 Chapter 6 的联系

现在回顾 Chapter 6

当时：

JSON File ➡ json.load() ➡ Python Dictionary

例如：

```python
with open("inventory.json") as file:
    inventory = json.load(file)
```

整个过程是：磁盘 ➡ JSON ➡ Python

现在 HTTP 通信也是一样, 只是 JSON 来源发生了变化. 

API Server ➡ JSON ➡ `response.json()` ➡ Python

可以发现 JSON 始终只是一种数据交换格式. 无论来自文件, 还是来自网络. 最终都会变成 Python Object, 这正是 Chapter 6 提前学习 JSON 的意义. 

## Response 生命周期

现在可以完整描述一次 API 返回的数据流. 

```
HTTP Response
        │
        ▼
Response Body
        │
        ▼
JSON
        │
        ▼
response.json()
        │
        ▼
Python Dictionary
        │
        ▼
Business Logic
```

Business Logic 永远处理 Python Object, 而不是 JSON 字符串. 这符合我们一直坚持的分层思想. 

## 与 CLI Automation 的比较

回顾 Chapter 9 CLI 返回 `show ip interface brief`

得到文本

然后：

Parser ➡ Python Object ➡ Compliance

而 API 返回：

HTTP Response ➡ JSON ➡ response.json() ➡ Python Object ➡ Business Logic

两种方式最终都会得到 Python Object. 区别在于 CLI 需要我们自己编写 Parser. HTTP API 因为采用了结构化数据, 大部分情况下可以直接转换. 这也是 API 自动化相比 CLI 自动化的重要优势. 

## Engineering Best Practice

在企业项目中, 建议形成固定的处理流程：

发送 Request ➡ 检查 Status Code ➡ 确认请求成功 ➡ response.json() ➡ Business Logic

而不是：

发送 Request ➡ response.json() ➡ 开始处理

原因很简单, 如果服务器返回：`500 Internal Server Error` 或者 `404 Not Found` Body 中的数据可能并不是业务数据. 

因此检查状态码仍然应该放在 JSON 解析之前, 这也是企业项目中最常见的处理顺序. 

## Engineering Insight

这里有一个容易混淆的地方. 很多人说 "API 返回的是 JSON. " 更准确地说应该是 HTTP Response Body 中包含 JSON 文本. 

而 `response.json()`

返回的是：Python Object. 

自动化程序真正处理的, 

始终都是 Python 的数据结构. 

这一点解释了为什么前面章节一直强调：

>Business Logic 应尽量使用 Python Object, 而不是直接处理原始通信数据. 

## Engineering Checklist

完成本实验后, 应能够回答以下问题：

- response.text 与 response.json() 有什么区别? 

- response.json() 返回的是 JSON, 还是 Python Object? 

- 为什么 response.text 不适合直接进行业务处理? 

- 本实验与 Chapter 6 的 json.load() 有什么共同点? 

- API 自动化相比 CLI 自动化, 为什么通常不需要编写复杂的 Parser? 

- 企业项目中, 为什么应先检查 status_code, 再调用 response.json()? 

## Summary

本实验完成了从 HTTP Response 到 Python Object 的转换过程：

- `response.text`：返回响应内容的字符串表示. 

- `response.json()`：将 JSON 响应解析为 Python 对象. 

- Business Logic：应处理 Python Object, 而不是 JSON 字符串. 

至此, 我们已经具备了读取 API 数据的基本能力. 下一节将开始学习如何向服务器发送业务数据, 即使用 POST Request 与 HTTP Body, 将 Python 数据转换为 JSON Payload 并发送给 API 服务, 这将与本节形成完整的双向数据流. 

# Lab 3 Use POST Request send data

## Theory

前两个实验中, 我们一直使用 GET

GET 的特点是读取资源. 

因此客户端几乎不用向服务器发送业务数据. 

真正需要发送业务数据的是: 

- POST

- PUT

- PATCH

它们都会涉及 HTTP Body. 

本实验首先学习最常见的 POST. 

## Previous Lab Review

上一节的数据流是: 

API Server ➡ JSON ➡ response.json() ➡ Python Object

这是: 服务器 ➡ 客户端 的数据流. 

现在我们要学习相反的方向: 

Python Object ➡ JSON ➡ HTTP Body ➡ API Server

可以发现整个过程正好相反. 

## Engineering Discussion

### POST 与 GET 的区别

回顾上一节. 

GET: `GET /devices`

客户端只是: 请求数据, 几乎没有业务数据需要发送. 

而 POST: `POST /devices`

服务器一定会问: "你准备创建什么设备? "

因此客户端必须把设备信息发送给服务器. 

这些数据就位于 HTTP Body. 

### Python 如何发送 Body? 

我们已经知道 HTTP Body 中通常保存的是 JSON Payload. 

而 Business Logic 一直使用 Python Dictionary. 

例如: 

```python
device = {
    "hostname": "R1",
    "management_ip": "10.1.1.1"
}
```

那么 Python Dictionary 如何变成 HTTP Body? 

这就是 requests 负责完成的工作. 

## Hands-on Lab

为了演示 POST, 我们继续使用公开测试 API. 

创建`scripts/http_post.py`

代码如下: 

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"

payload = {
    "title": "Automation Workbook",
    "body": "Chapter 10",
    "userId": 1
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())
```

运行 `python3 scripts/http_post.py`

输出类似 `201`

随后: 

```
{
    "title": "...",
    "body": "...",
    "userId": 1,
    "id": 101
}
```

## Engineering Analysis

注意这一行: 

```python
response = requests.post(url, json=payload)
```

这里出现了新的参数 `json=payload`

它并不是 HTTP Method, 也不是 JSON 文件. 

它表示把 Python Dictionary 作为 JSON Payload 发送. 

requests 会自动完成以下工作: 


Python Dictionary ➡ JSON Serialization ➡ HTTP Body ➡ 发送 HTTP Request

整个过程无需我们手工转换. 

## 为什么使用 json=? 

很多初学者会问为什么不是 

```python
data=payload
```

或者: 

```python
body=payload
```

对于当前阶段, 只需要理解当使用 `json=payload` requests 会自动: 

- 将 Python Object 序列化为 JSON. 

- 将 JSON 放入 HTTP Body. 

- 设置正确的 `Content-Type`. 

因此对于发送 JSON 数据的 API, 这是最常见、也是最推荐的写法. 

至于 `data=` 与 `json=` 的区别, 我们将在后续介绍不同数据格式时再深入讨论, 避免一次引入过多概念. 

## 数据流分析

现在可以完整描述一次 POST 请求. 

```
Business Logic
        │
        ▼
Python Dictionary
        │
        ▼
requests.post(json=...)
        │
        ▼
JSON Payload
        │
        ▼
HTTP Body
        │
        ▼
API Server
```

服务器收到请求以后, 再返回: 

```
HTTP Response

↓

Status Code

↓

Response Body

↓

response.json()

↓

Python Dictionary
```

整个流程形成了一个完整的数据闭环. 

## 与前面章节的联系

回顾 Workbook 前面的内容. 

Chapter 6: 

JSON File ➡ Python Dictionary

Chapter 10(GET): 

HTTP Response ➡ JSON ➡ Python Dictionary

Chapter 10(POST): 

Python Dictionary ➡ JSON ➡ HTTP Request

可以发现, 无论数据来自: 

- 文件

- 网络响应

- 网络请求

Business Logic 始终使用 Python Dictionary. JSON 只是交换格式. 

这一设计保持了整个 Enterprise Automation Platform 的一致性. 

## Engineering Best Practice

在企业项目中, 建议遵循以下职责划分: 

Business Logic ➡ 构造 Python Object ➡ API Client ➡ 转换为 JSON ➡ 发送 HTTP Request

Business Logic 不应关心: 

- JSON 如何序列化. 

- Header 如何设置. 

- HTTP Body 如何构造. 

这些工作都属于 API Client(Connection Layer). 这样可以保证当通信细节发生变化时, 业务逻辑无需修改. 

## Engineering Insight

请注意一个容易混淆的概念很多人会说: "我发送了 JSON."

更准确的描述应该是: 

>Business Logic 构造了 Python Object；HTTP Client 将它序列化为 JSON, 并作为 HTTP Body 发送给服务器. 

这种描述明确区分了: 

- 业务数据(Python Object)

- 交换格式(JSON)

- 传输载体(HTTP Body)

这种分层思维, 将贯穿整个 Workbook. 

## Engineering Checklist

完成本实验后, 应能够回答以下问题: 

- 为什么 POST 通常需要 HTTP Body?

- json=payload 中的 payload 是什么类型?

- requests 在发送请求时自动完成了哪些工作?

- 为什么 Business Logic 应构造 Python Object, 而不是直接拼接 JSON 字符串?

- 本实验的数据流与上一节(GET)有什么区别?

- 为什么 JSON 应被视为数据交换格式, 而不是业务对象?

## Summary

本实验完成了客户端向服务器发送业务数据的全过程: 

- 使用 POST 创建资源. 

- 使用 Python Dictionary 描述业务数据. 

- 使用 json=payload 将业务数据发送给服务器.

- 理解了 requests 自动完成 JSON 序列化与 HTTP Body 构造的过程. 

至此, 我们已经掌握了 HTTP API 最核心的两种数据流: 

- GET: 服务器 → JSON → Python Object. 

- POST: Python Object → JSON → 服务器. 

# Lab 4 API Client Module

这里开始, 我认为应该进入 Chapter 10 最重要的工程部分. 

前面的内容都是在学习 HTTP 和 requests, 但是, 这本 Workbook 的目标一直不是教大家如何调用 requests. 而是构建一个 Enterprise Automation Platform. 

因此, 从这里开始, 我们要把零散的实验代码, 重新整理成符合前面章节架构的工程代码. 

## Theory

到目前为止, 我们已经完成了三个实验. 

例如: 

```python
response = requests.get(url)
```

以及: 

```python
response = requests.post(url, json=payload)
```

这些代码能够正常工作, 但是它们还不能称为企业工程, 原因很简单. 

目前: 

- Business Logic

- HTTP Communication

- requests Library

全部写在同一个文件里面, 随着项目越来越大, 这种写法将难以维护. 因此, 我们需要重新思考 HTTP 通信应该放在哪一层? 

## Previous Chapter Review

回顾 Chapter 8, 当时我们建立了: 

Inventory ➡ Renderer ➡ Deployment

其中 Deployment Module 负责: 

- 建立 SSH Connection

- 下发配置

- 返回执行结果

Business Logic 并不知道 Netmiko. 

Chapter 9 也是一样. 

Inventory ➡ Connection ➡ Backup ➡ Parser ➡ Compliance

Compliance Module不会自己 `ConnectHandler(...)` 而是调用 Connection Module. 

因此 Chapter 10 应继续保持一致. 

## Engineering Discussion

### 为什么不能在 Business Logic 中直接调用 requests? 

假设未来我们有一个模块: `generate_report()`

里面直接写 `requests.get(...)`

另外 `deploy_device()` 

也写 `requests.post(...)`

还有 `sync_inventory()`

再次 `requests.get(...)`

项目会变成: 

Business Logic ➡ requests ➡ HTTP

随着模块越来越多: 

- requests 到处出现

- Header 到处复制

- URL 到处复制

- Timeout 到处复制

- Authentication 到处复制

维护成本会越来越高. 这与前面 Workbook 一直坚持的 Business Logic Separation 完全相违背. 

## API Client 应承担什么职责? 

因此我们引入一个新的模块: 

```
modules/

    api_client.py
```

注意增加模块并不是为了增加模块, 而是因为它拥有独立职责. 

API Client 的职责可以总结为: 

- 建立 HTTP 请求

- 调用 requests

- 添加统一 Header

- 添加认证信息

- 设置 Timeout

- 检查 Status Code

- 返回 Python Object

可以看到这些全部属于通信层, 并不是业务层. 因此它应该独立存在. 

## Layered Architecture

新的架构变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
requests
        │
        ▼
HTTP
        │
        ▼
API Server
```

这里有一个非常重要的变化, Business Logic 已经不知道 requests. 甚至不知道 HTTP. 它只知道调用: 

```python
get_devices()

create_device()

delete_device()
```

至于里面如何通信, 完全交给 API Client. 

## API Client 的接口设计

从 Business Logic 的角度, API Client 应提供简单, 稳定, 可读的接口. 

例如: 

```python
get(url)
```

或者: 

```python
post(url, payload)
```

注意这里仍然保持通用. 因为本章尚未涉及任何厂商 API. 因此 API Client 目前只是 HTTP Communication Layer, 而不是 Cisco Client. 

也不是 DNA Center Client. 

保持 Vendor Neutral(厂商中立)是本章的重要原则. 

## Hands-on Lab

创建新的模块: automation_project/[api_client.py](vscode-remote://ssh-remote%2B192.168.178.144/home/user/automation_project/modules/api_client.py)

```
modules/

    api_client.py
```

第一版代码: 

```python
import requests


def get(url):
    """
    Send an HTTP GET request.

    Args:
        url (str): API endpoint.

    Returns:
        requests.Response: HTTP response object.
    """
    return requests.get(url)


def post(url, payload):
    """
    Send an HTTP POST request.

    Args:
        url (str): API endpoint.
        payload (dict): Request payload.

    Returns:
        requests.Response: HTTP response object.
    """
    return requests.post(url, json=payload)
```

这一版实现非常简单. 原因是目前我们的目标不是增加功能. 而是建立正确的工程结构. 

## 修改 Workflow

现在脚本 `scripts/http_get.py`

可以改成: 

```python
from modules import api_client

url = "https://jsonplaceholder.typicode.com/posts/1"

response = api_client.get(url)

print(response.status_code)
print(response.json())
```

可以发现 Workflow 已经不再直接使用 `requests.get()` 而是 `api_client.get()`

Business Logic 与 requests 彻底解耦. 

## Engineering Analysis

很多人可能会觉得这里不过是 `requests.get()` 外面包了一层, 是不是没有意义? 

实际上这一层正是企业工程最重要的一层. 

例如: 以后如果需要统一增加 `timeout=10`

只需要修改 api_client.py

如果需要统一增加 `verify=True`

仍然修改一个地方. 

如果未来所有 API 都需要 Authorization Header. 

依然修改一个地方. 

Business Logic 完全不用修改. 

这就是集中管理(Centralized Management) 的价值. 

## Engineering Best Practice

API Client 在当前阶段应保持轻量(Lightweight). 

它的职责是统一通信, 而不是实现复杂业务. 

例如下面这些职责属于 API Client: 

- 发起请求

- 返回响应

- 设置超时

- 设置公共 Header

而下面这些职责不属于 API Client: 

- 判断设备是否符合 Compliance

- 计算业务逻辑

- 渲染配置模板

- 生成报表

这些仍然属于各自的业务模块. 

保持这种职责边界, 有助于避免模块不断膨胀, 形成"万能工具类". 

## Engineering Insight

这一节实际上完成了 Workbook 的一个重要目标截至 Chapter 10, 我们已经拥有了两种通信方式: 

```
Connection Layer
        │
        ├── SSH (Netmiko)
        │
        └── HTTP (requests)
```

虽然底层协议完全不同, 但是对于整个 Enterprise Automation Platform 而言, 它们都只是 Connection Layer 的不同实现. 

这意味着随着后续章节加入新的通信方式, 平台的总体架构无需改变. 我们扩展的是能力, 而不是推倒重建系统. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么不能在 Business Logic 中直接调用 requests? 

- 为什么需要单独的 api_client.py? 

- API Client 应承担哪些职责? 

- 哪些职责不应该放入 API Client? 

- 为什么说当前的 API Client 是一个通信层, 而不是业务层? 

- 这一设计与 Chapter 8, Chapter 9 的分层思想有什么一致性? 

## Summary

本节完成了 Chapter 10 从"学习 `requests`"到"工程化使用 `requests`"的重要转变: 

- 新增 `modules/api_client.py`, 作为统一的 HTTP 通信模块. 

- 将 `requests` 封装在 Connection Layer 中, 而不是直接暴露给 Business Logic. 

- 保持了 Single Responsibility Principle, Layered Architecture 和 Business Logic Separation. 

- 为后续逐步加入认证, 超时, 错误处理, 日志等能力预留了统一扩展点, 而不会影响上层业务代码. 

到这里, HTTP 已经不再只是一个协议, 而已经成为 Enterprise Automation Platform 中的一种标准通信能力. 

# Lab 5 API Client Error Handling

很好, 现在应该继续完善 `api_client.py`, 而不是立即进入认证(Authentication)或具体厂商 API. 

原因很简单, 目前我们的 `api_client.py` 只是一个"转发器": 

```python
def get(url):
    return requests.get(url)
```

虽然完成了解耦, 但是距离企业工程还有一步, 这一节, 我们开始加入统一错误处理(Error Handling). 注意, 这里说的是HTTP 通信层的错误处理, 不是业务错误处理, 这是 API Client 最重要的职责之一. 

## Theory

目前我们的 API Client: 

```python
def get(url):
    return requests.get(url)
```

能够正常工作, 但是它假设了一件事情 HTTP Request 一定能够成功发送, 现实情况并非如此. 

例如: 

- API Server 宕机

- DNS 无法解析

- 网络中断

- TCP Connection Timeout

- SSL 建立失败

这些情况都属于通信失败(Communication Failure). 

注意它们与上一节学习的: 

```
404

500
```

不是同一种错误. 

## Engineering Discussion

### 两类完全不同的错误

很多初学者容易把所有错误混在一起, 实际上HTTP 自动化至少存在两类错误. 

第一类: **通信错误(Communication Error)**

例如: 

Python ➡ 无法连接服务器

这种情况下 HTTP Request 根本没有成功发送, 服务器甚至没有收到请求. 

因此不会存在: 

```
200

404

500
```

这些 Status Code. 

第二类: **HTTP 错误(HTTP Error)**

例如: 

Python ➡ HTTP Request ➡ API Server ➡ 404 Not Found

这里说明通信已经成功, 服务器已经收到请求. 只是服务器返回了错误结果. 

因此通信成功, 业务失败. 

整个流程可以表示为: 

```
                API Request
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
Communication Failed      HTTP Response Received
         │                       │
         ▼                       ▼
Exception              Status Code
```

这是后续整个 API 自动化中最重要的错误分类. 

## 为什么 API Client 要处理通信错误? 

假设: 

Business Logic: `generate_report()`

里面直接: `requests.get(...)`

如果服务器断网, 程序可能直接抛出异常. 

Business Logic 突然开始处理: 

- Timeout

- DNS

- SSL

- Socket

这显然违反了 Single Responsibility Principle. 

Business Logic 应该只关心: 

>"设备信息是否获取成功? "

而不是 TCP 为什么建立失败. 

因此通信异常, 应该首先由 API Client 负责. 

## Hands-on Lab

修改: `modules/api_client.py`

第一版错误处理:

```python
import requests


def get(url):
    """
    Send an HTTP GET request.
    """
    try:
        return requests.get(url)

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None


def post(url, payload):
    """
    Send an HTTP POST request.
    """
    try:
        return requests.post(url, json=payload)

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

这里第一次出现 `requests.RequestException`

它是 requests 提供的通用异常类型, 能够覆盖绝大多数通信错误. 目前我们不展开各种具体异常, 保持本章的学习节奏.

## 修改 Workflow

由于 API Client

现在可能返回 `None`

Workflow 需要进行简单检查. 

例如: 

```python
from modules import api_client

url = "https://jsonplaceholder.typicode.com/posts/1"

response = api_client.get(url)

if response is None:
    print("Request failed.")
else:
    print(response.status_code)
```

这里要注意, Workflow 仍然没有处理 Timeout, DNS, SSL. 它只知道请求失败, 真正的通信细节仍然隐藏在 API Client. 

## Engineering Analysis

现在整个平台的数据流已经发生变化. 

以前: 

Business Logic ➡ requests ➡ HTTP

现在: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
Communication Error Handling
        │
        ▼
requests
        │
        ▼
HTTP
```

Business Logic 根本不知道 requests 抛出了什么异常. 它只知道请求成功, 或者失败.

这就是 Layered Architecture 最大的价值.

为什么这里只处理通信异常?

很多读者可能会问为什么 404 没有在 API Client 里面处理? 

答案是因为 404 并不是通信失败. 

例如: 

Python ➡ HTTP Request ➡ Server ➡ 404

整个通信完全成功. 

只是服务器告诉客户端资源不存在. 

因此 404 属于 HTTP Response, 而不是 Communication Exception. 

后面我们会讨论如何统一处理 Status Code. 目前 API Client 只负责确保请求能够正常发送. 

## Engineering Best Practice

在企业项目中, 可以遵循如下职责划分: 

| 类型               | 处理位置             |
| ---------------- | ---------------- |
| 网络中断             | API Client       |
| DNS 失败           | API Client       |
| Timeout          | API Client       |
| SSL 异常           | API Client       |
| HTTP Status Code | API Client(统一检查) |
| 业务逻辑判断           | Business Logic   |

这样做的好处是整个项目中所有通信问题, 都集中在一个模块. 而不是散落在几十个业务脚本里面. 

## Engineering Insight

这里需要注意一个容易混淆的地方. 很多教程会说 "404 是 Exception. " 实际上并不是. 对于 requests 来说服务器正常返回 404 默认不会抛出通信异常. 因为 HTTP 协议已经完成, TCP 已经建立, 服务器已经响应. 

404 只是服务器返回的一种结果. 因此在工程上通信异常(Exception)与 HTTP Status Code 应作为两类不同的问题进行处理. 

这种区分能够让 API Client 的职责更加清晰, 也符合我们一直坚持的分层设计. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 通信错误与 HTTP 错误有什么区别? 

- 为什么 API Client 应负责处理通信异常? 

- requests.RequestException 的作用是什么? 

- 为什么 Workflow 不需要知道 Timeout、DNS 等细节? 

- 为什么 404 不属于通信异常? 

- 为什么通信错误应集中在 API Client 中统一处理? 

## Summary

本节进一步完善了 `api_client.py`: 

- 引入了统一的通信异常处理. 

- 使用 requests.RequestException 捕获 HTTP 请求过程中的通信错误.

- 将网络异常与 HTTP Status Code 明确区分. 

- 保持 Business Logic 与底层通信实现解耦. 

至此, api_client.py 已经不仅仅是 requests 的简单封装, 而开始承担 Connection Layer 的职责. 下一节我们将在此基础上加入统一的 Status Code 检查, 形成完整的请求生命周期: 发送请求 → 处理通信异常 → 检查 HTTP Status Code → 返回响应对象. 这样, 一个企业级 API Client 的基本框架就初步建立起来了. 

# Lab 6 API Client Return Contract

这里不继续堆功能(例如 raise_for_status(), 认证, Session 等). 

按照我们 Workbook 前面几章的风格, 这里应该先统一设计 API Client 的返回契约(Return Contract). 

这是企业开发里比 requests 本身更重要的一件事情. 

很多教程都会直接继续讲: `response.raise_for_status()` 但是企业项目真正首先讨论的是 API Client 应该向上层返回什么? 

因为一旦接口设计好了, 后面加入认证, Session, 日志, Retry 都不会影响 Business Logic. 

所以这一节应该放在这里. 

## Theory

目前我们的 `api_client.py`: 

```python
def get(url):
    try:
        return requests.get(url)

    except requests.RequestException:
        return None
```

Business Logic: 

```python
response = api_client.get(url)

if response is None:
    ...
```

虽然已经能够工作. 但是这里仍然存在一个设计问题. 

>API Client 到底应该返回什么? 

这是所有通信模块都会遇到的问题. 不仅仅是 HTTP, SSH, NETCONF, RESTCONF, gRPC 都会面对同一个问题. 

## Engineering Discussion

### API Client 是谁的接口? 

很多人容易误认为 API Client 是 requests 的封装, 实际上不是. 它真正的消费者(Consumer)是 Business Logic. 

因此设计时首先应该考虑 Business Logic 最希望得到什么, 而不是 requests 返回什么. 

例如 requests 返回: `<Response [200]>`

这是 requests 的设计, 并不是我们的设计. 

### 为什么不能完全暴露 requests? 

假设以后 requests 升级, 或者整个项目改成其他 HTTP Library. 

例如: (这里只讨论概念, 不引入新的库. )

如果 Business Logic 到处都是: 

```python
response.status_code

response.headers

response.cookies
```

那么整个项目都会受到影响. Business Logic 实际上已经依赖 requests, 而不是 API Client. 因此 API Client 应该成为整个平台唯一知道 requests 存在的地方. 

## 什么是 Return Contract? 

Return Contract 就是 API Client 向外承诺我一定返回什么. 

例如下面三种设计. 

方案一: 始终返回 Response Object. 

```python
response = api_client.get(...)
```

优点: 最简单

缺点: Business Logic

知道: requests. 

方案二: 始终返回 Python Object. 

例如: `device = api_client.get(...)`

Business Logic 直接得到: Dictionary. 

完全不知道: HTTP. 

方案三: 返回统一结果对象. 

例如: 

```
Request Result

├── success
├── status
├── data
└── message
```

这是很多大型项目采用的方法, 但是目前对于 Workbook 来说复杂度过高. 

因此暂不采用. 

## 为什么目前继续返回 Response? 

本 Workbook 当前阶段. 

推荐继续返回 `requests.Response` 原因有三个. 

第一, 学习成本最低. 

目前读者正在学习 HTTP, 如果再引入自己的 Response Class 反而会增加理解难度. 

第二, 后面可以逐步演进.

例如未来:

Response ➡ Enterprise Response ➡ Business Object

架构可以自然升级, 不用推倒重来. 

第三, 保持 Connection Layer. 

只负责通信. Business Layer 负责业务. 

这种边界目前最清晰. 

## Layered Architecture

目前的数据流保持: 

```
Business Logic
        │
        ▼
Response Object
        │
        ▼
API Client
        │
        ▼
requests
        │
        ▼
HTTP
```

注意 Business Logic 依赖的是 API Client. 不是 requests, 这一点非常重要. 虽然目前 Response 来自 requests, 但是所有创建, 异常处理, 发送, 接收. 全部隐藏在: API Client. 

## Engineering Analysis

很多初学者会认为 

```ptyhon
return requests.get(...)
```

和 

```python
response = requests.get(...)
return response
```

没有区别. 实际上真正重要的是返回行为由 API Client 定义. 

例如以后如果需要统一 `response.raise_for_status()` 或者统一记录: 

```
Request Time

Response Time
```

Business Logic 完全不用修改. 因为 Contract 没有变化. 这就是 API Interface稳定的重要性. 

## 为什么现在不直接返回 `response.json()`? 

很多教程喜欢这样写: 

```python
def get(url):
    response = requests.get(url)
    return response.json()
```

看起来很方便, 但是这样做会丢失很多重要信息. 

例如: Business Logic

无法获得: `response.status_code`

也无法获得: `response.headers`

更无法知道服务器到底返回了什么, 因此目前阶段. 仍然保留完整 Response Object. 让 Business Logic 根据需要读取: 

```python
response.json()

response.status_code
```

这样接口保持最大灵活性. 

## Engineering Best Practice

企业项目中, 一个通信模块应首先保证: 

- 返回行为稳定. 

- 接口尽可能简单. 

- 不要让上层依赖底层通信库的实现细节. 

- 未来能够平滑扩展, 而不是频繁修改接口. 

目前的 `api_client.py` 已经满足这些目标: 

- 统一发送请求. 

- 统一处理通信异常. 

- 统一返回 `Response` 对象. 

后续新增认证, 超时, 日志, 重试等能力, 都可以在保持接口不变的前提下完成. 

## Engineering Insight

这一节虽然没有增加新的代码, 却完成了一个比代码更重要的设计决策: 

>API Client 的价值, 不在于包装了多少 requests 函数, 而在于它定义了整个 Enterprise Automation Platform 与 HTTP 通信之间的契约(Contract). 

前面的章节, 我们已经分别建立了: 

- Inventory Contract: Inventory Module 提供统一的设备数据. 

- Renderer Contract: Renderer Module 提供统一的配置渲染结果. 

- Connection Contract: SSH Connection Module 提供统一的设备连接能力. 

现在API Client 建立了 HTTP Communication Contract. 所有上层模块都通过这一契约访问 HTTP 服务, 而无需了解底层实现细节. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 什么是 API Client 的 Return Contract? 

- 为什么 API Client 的接口应面向 Business Logic, 而不是面向 requests? 

- 为什么目前保留 Response 对象, 而不是直接返回 response.json()? 

- 返回契约稳定对后续扩展有什么好处? 

- API Client 在整个 Enterprise Automation Platform 中承担什么角色? 

## Summary

本节没有增加新的 HTTP 功能, 而是确定了 api_client.py 的接口设计原则: 

- API Client 是 Business Logic 与 HTTP 通信之间的统一接口. 

- 当前阶段保持返回 Response 对象, 以兼顾学习目标和接口灵活性. 

- 通过稳定的返回契约, 为后续加入认证, 日志, 超时, 状态码检查, 重试等功能奠定基础, 而无需修改上层业务代码. 

- 这一步完成后, 我们再继续完善 api_client.py 的能力, 就能够始终保持整个平台的分层架构和接口稳定性. 

# Lab 7 HTTP Status Code Validation

很好, 到这里, 我们已经完成了 `api_client.py` 的整体框架设计. 接下来, 就应该真正完善这个模块. 

按照企业项目的请求生命周期, 现在缺少的一步是: 

Send Request ➡ Communication Exception ➡ HTTP Status Code Validation ➡ Return Response

前一节已经完成了: 

- 发送请求

- 通信异常处理

- 返回契约

现在应该加入: 

>统一的 HTTP Status Code Validation. 

这是一个企业 API Client 必须具备的能力. 

## Theory

在 Chapter 10 前半部分, 我们已经学习了 HTTP Status Code 分为: 

- 2xx —— Success

- 4xx —— Client Error

- 5xx —— Server Error

但是, 到目前为止, 我们的 API Client 并没有真正使用这些知识. 

例如: 

```python
response = api_client.get(url)

print(response.status_code)
```

Business Logic 仍然需要自己判断: 

```python
if response.status_code == 200:
    ...
```

或者: 

```python
if response.status_code == 404:
    ...
```

这样做虽然没有问题, 但是随着项目越来越大, 这种判断会不断重复. 

## Engineering Discussion

### 谁应该检查 Status Code? 

这里有两个方案. 

方案一, 每个业务模块自己检查. 

例如: 

```python
response = api_client.get(url)

if response.status_code != 200:
    ...
```

Compliance 检查一次. 

Inventory 检查一次. 

Deployment 检查一次. 

Monitoring 再检查一次. 

整个项目到处都是 `if response.status_code ...` 

这种设计违反了

>Don't Repeat Yourself(DRY)

方案二, 统一交给 API Client. 

流程变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ├── Send Request
        ├── Handle Exception
        ├── Validate Status Code
        └── Return Response
```

Business Logic 不用重复编写 HTTP 判断逻辑. 这更加符合 Layered Architecture. 

## 什么叫 Success? 

很多初学者容易认为 200 才代表成功. 

实际上, HTTP 定义的是整个 2xx 都属于 Success. 

例如: 

| Status Code | 含义       |
| ----------- | ---------- |
| 200         | OK         |
| 201         | Created    |
| 202         | Accepted   |
| 204         | No Content |


因此企业项目一般不会写: `if response.status_code == 200:`

而是判断是否属于 2xx. 

## Hands-on Lab

首先新增一个内部函数: 

```python
import requests


def _check_status(response):
    """
    Validate HTTP status code.

    Args:
        response (requests.Response): HTTP response.

    Returns:
        bool: True if request succeeded.
    """
    return 200 <= response.status_code < 300
```

这里使用 `_check_status()`

注意前面的: `_` 表示这是 API Client 内部使用的辅助函数. 

Business Logic 不应该直接调用. 

修改: 

```python
def get(url):
    try:
        response = requests.get(url)

        if not _check_status(response):
            print(f"HTTP Error: {response.status_code}")
            return None

        return response

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

POST 同样: 

```python
def post(url, payload):
    try:
        response = requests.post(url, json=payload)

        if not _check_status(response):
            print(f"HTTP Error: {response.status_code}")
            return None

        return response

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

## 为什么使用内部函数? 

很多人可能会写 `if 200 <= response.status_code < 300:`

然后复制到GET, POST, PUT, PATCH, DELETE. 以后如果修改判断逻辑, 需要修改五个地方. 

因此封装成 `_check_status()` 以后整个项目只有一个地方负责 Status Code Validation. 这也是 DRY Principle 的体现. 

## Workflow 的变化

现在 Business Logic 进一步简化. 

例如: 

```python
response = api_client.get(url)

if response is None:
    print("Request failed.")
else:
    data = response.json()
    print(data)
```

Business Logic 已经不知道失败原因到底是: 

- Timeout

- DNS

- 404

- 500

它只知道请求成功, 或者失败. 这种抽象正是 Connection Layer 存在的意义. 

## Engineering Analysis

现在 API Client 已经形成完整流程. 

```
Business Logic
        │
        ▼
api_client.get()
        │
        ▼
requests.get()
        │
        ▼
Communication Exception?
        │
    Yes │ No
        ▼
     Return None
        │
        ▼
Status Code Validation
        │
    Fail │ Pass
        ▼
 Return None   Response
```

Business Logic 完全不用关心 HTTP 细节, 所有通信相关工作. 已经全部收敛到 API Client. 

## 为什么这里没有使用 `raise_for_status()`? 

requests 提供了 `response.raise_for_status()` 它可以把 4xx 和 5xx 转换成异常, 这是一个很方便的功能, 但是当前 Workbook 暂时不使用,原因有两个. 

第一, 目前我们希望明确区分: 

- 通信异常

- HTTP 响应错误

如果立即使用 `raise_for_status()`, 这两类情况都会表现为异常, 不利于初学者理解整个请求生命周期. 

第二, 自己实现 `_check_status()`, 能够更清楚地体现 API Client 拥有 Status Code Validation 的职责, 而不是完全依赖第三方库提供的默认行为. 在读者理解了这一设计之后, 再介绍 raise_for_status() 会更加自然. 

## Engineering Best Practice

企业项目中, 一个成熟的 API Client 通常负责: 

- 统一发送请求. 

- 统一处理通信异常. 

- 统一验证 HTTP Status Code. 

- 统一返回结果. 

Business Logic 只负责业务流程. 而不是通信流程. 

这种职责划分, 使得整个系统更容易维护, 也便于未来统一加入日志、认证、重试和监控. 

# Engineering Insight

到目前为止, 我们已经逐步把一个简单的 `requests.get(url)` 演化成了一个真正具有工程意义的通信组件. 

这个演化过程体现了一个重要思想:

>企业工程并不是不断增加新功能, 而是不断把重复的、共性的能力向下沉淀到基础模块. 

`api_client.py` 现在已经不仅是一个 `requests` 包装器, 它开始承担整个平台 HTTP 通信入口的职责. 未来无论增加认证、Session、日志还是重试, 都将在这个统一入口中完成, 而不会扩散到业务代码中. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么不建议每个业务模块自行检查 status_code? 

- 为什么 _check_status() 使用 2xx 范围, 而不是只判断 200? 

- 为什么 _check_status() 设计为 API Client 的内部函数? 

- 通信异常与 HTTP Status Code Validation 在请求生命周期中的顺序是什么? 

- 为什么本章暂时没有使用 response.raise_for_status()? 

- API Client 当前已经承担了哪些统一职责? 

## Summary

本节进一步完善了 api_client.py: 

- 新增统一的 HTTP Status Code Validation. 

- 使用内部辅助函数 _check_status() 避免重复代码. 

- 将 HTTP 成功定义为整个 2xx 状态码范围, 而不仅是 200. 

- 保持 Business Logic 与 HTTP 通信细节完全解耦. 

至此, api_client.py 已经具备了一个企业级通信模块的基本能力: 发送请求 → 处理通信异常 → 验证 HTTP 状态码 → 返回统一结果. 后续章节将在此基础上继续加入认证、超时配置、日志记录和会话管理, 而无需改变上层业务代码. 

# Lab 8 Request Timeout

到这里, 我们已经完成了一个能够工作的 `api_client.py`. 但是, 如果直接把它放到企业项目中, 还存在一个明显的问题 `response = requests.get(url)` 这里没有任何限制. 

如果服务器一直没有响应, 会发生什么? 

答案是程序可能一直等待对于自动化平台而言, 这是不可接受的. 

因此, 下一步应该加入: Timeout(超时控制)这是企业 HTTP Client 的基本能力之一. 

## Theory

目前 `response = requests.get(url)` requests 会等待服务器返回结果. 

如果: 

- 网络非常慢

- API Server 无响应

- TCP 已建立但服务器没有返回数据

程序可能等待很长时间. 

在自动化平台中, 这意味着 Inventory ➡ API Request ➡ 一直等待…… ➡ 整个 Workflow 被阻塞

因此企业项目通常都会设置 Timeout. 

## Engineering Discussion

### Timeout 的意义

很多人认为 Timeout 是为了提高速度, 实际上不是. Timeout 的真正目的只有一个防止程序无限等待. 它保护的是整个 Workflow. 

例如: 

Generate Report ➡ Get Device Inventory ➡ Get Interface Information ➡ Generate Report

如果第二步一直等待, 那么整个流程都会停止. Timeout 可以让程序在合理时间内结束等待, 并决定下一步如何处理. 

Timeout 属于哪一层? 

根据前面建立的架构: 

Business Logic ➡ API Client ➡ requests ➡ HTTP

Timeout 属于 HTTP Communication. 

因此它应该由 API Client 统一设置. 

Business Logic 不应该写 `requests.get(url, timeout=10)` 否则 Timeout 又会散落到整个项目. 

## Hands-on Lab

修改: 

```python
import requests

DEFAULT_TIMEOUT = 10


def get(url):
    try:
        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT
        )

        if not _check_status(response):
            print(f"HTTP Error: {response.status_code}")
            return None

        return response

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

POST 同样: 

```python
def post(url, payload):
    try:
        response = requests.post(
            url,
            json=payload,
            timeout=DEFAULT_TIMEOUT
        )

        if not _check_status(response):
            print(f"HTTP Error: {response.status_code}")
            return None

        return response

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

## 为什么使用常量? 

这里没有直接写 `timeout=10` 而是 `DEFAULT_TIMEOUT = 10` 原因是 Timeout 属于整个 API Client 的配置. 

以后如果需要调整例如 10秒 ➡ 30秒. 只需要修改一个地方. 

而不是搜索整个项目. 

## Timeout 应该由 Business Logic 决定吗? 

很多项目容易出现: 

```python
api_client.get(url, timeout=5)

api_client.get(url, timeout=20)

api_client.get(url, timeout=60)
```

虽然这种设计很灵活, 但是对于当前 Workbook 的平台来说统一策略更加重要. 

Business Logic 应该表达获取设备信息, 而不是获取设备信息, 并等待 17 秒. 

等待多久-属于通信策略. 因此应该由 API Client 统一决定. 如果未来确实出现特殊需求, 再扩展接口, 而不是一开始就增加复杂度. 

## Workflow 的变化

现在一次请求的完整生命周期变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ├── Build Request
        ├── Apply Timeout
        ├── Send Request
        ├── Handle Communication Exception
        ├── Validate Status Code
        └── Return Response
```

Business Logic 仍然只有一句 `response = api_client.get(url)` 通信策略已经进一步下沉. 

## Engineering Analysis

注意 Timeout 与: 

```
404

500
```

完全不同. 

Timeout 发生在服务器返回 Response 之前. 因此属于 Communication Exception. 而 404 说明服务器已经成功收到请求. 

因此属于 HTTP Response 整个流程可以表示为: 

```
Send Request
      │
      ▼
Timeout ?
 │        │
Yes      No
 │        ▼
Exception  Receive Response
              │
              ▼
       Status Code Validation
```

这再次验证了前面建立的错误分类模型. 

## Engineering Best Practice

企业项目通常遵循以下原则: 

- 每个 HTTP 请求都应设置 Timeout. 

- Timeout 应由通信层统一管理. 

- 不要依赖第三方库的默认等待行为. 

- 避免在 Business Logic 中重复指定 Timeout. 

这样既保证了代码一致性, 也方便后续根据生产环境统一调整通信策略. 

## Engineering Insight

Timeout 看似只是增加了一个参数 `timeout=10` 实际上, 它体现的是一种设计原则通信策略应集中管理, 而不是由业务代码决定. 

前面我们已经统一了: 

- 请求发送

- 通信异常

- 状态码验证

现在Timeout 也加入了统一管理. 

可以看到, api_client.py 正在逐步成为整个平台唯一负责 HTTP 通信策略的模块, 而不是简单地包装几个 requests 函数. 

Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么企业项目应始终设置 Timeout?

- Timeout 与 HTTP 404 有什么本质区别?

- 为什么 Timeout 应由 API Client 统一管理?

- 为什么使用 DEFAULT_TIMEOUT 常量, 而不是直接写数字?

- Timeout 属于通信策略还是业务逻辑?

- 当前 API Client 已经统一管理了哪些通信策略? 

## Summary

本节为 api_client.py 增加了统一的超时控制: 

- 引入 DEFAULT_TIMEOUT 作为统一配置. 

- 为所有 HTTP 请求设置 Timeout, 避免无限等待. 

- 将 Timeout 明确归类为通信策略, 由 API Client 集中管理. 

- 保持 Business Logic 与通信实现进一步解耦. 

至此, 我们的 API Client 已经具备了发送请求、异常处理、状态码验证和超时控制等基础能力. 下一步, 将继续完善这一模块, 引入统一日志记录(Logging), 使每一次 HTTP 请求都能够被自动记录, 为后续故障排查和审计提供支持. 这也将与前面章节建立的日志体系保持一致. 

# Lab 9 API Request Logging

实际上，Logging 不应该只是"打印信息", 它应该与 Chapter 8 建立的日志体系保持一致. 这样，整个 Enterprise Automation Platform 才只有一套 Logging Architecture. 

## Theory

目前，我们的 `api_client.py` 已经具备: 

- Send Request

- Communication Exception

- Status Code Validation

- Timeout

但是整个通信过程仍然是不可观察(Unobservable)的. 

例如程序失败以后,我们不知道: 

- 请求发送到了哪个 URL? 

- 使用了什么 Method? 

- 请求什么时候发生? 

- 返回了什么 Status Code? 

- 请求耗时多久? 

如果没有日志这些信息都会丢失. 

## Previous Chapter Review

回顾 Chapter 8, 当时我们建立了统一日志模块. 

例如: 

```
modules/

    logger.py
```

所有业务模块: 

```
Deployment

Compliance

Inventory
```

都通过 `logger.info(...)` 记录运行信息, Chapter 10 不应该重新设计日志. HTTP Communication 也应该使用同一套 Logging Framework. 

## Engineering Discussion

### 为什么不能使用 print()? 

目前 API Client 仍然有 `print(f"HTTP Error: {response.status_code}")` 虽然可以工作, 但是企业项目几乎不会这样做. 

原因有很多, 例如程序后台运行时 `stdout` 可能根本没人看. 

另外 `print` 没有:

- Timestamp

- Log Level

- Module Name

因此无法用于生产环境. 

### HTTP Log 应记录什么? 

很多初学者喜欢记录整个 Response. 

例如 `print(response.text)` 实际上真正有价值的是通信信息. 

例如: 

```
GET

https://server/api/devices

200
```

这些信息能够帮助工程师快速定位通信是否成功. 至于业务数据属于   Business Logic, 不应该全部写入 Communication Log. 

## Logging Scope

建议 API Client 只记录通信信息. 

例如: 

```
Timestamp

Method

URL

Status Code

Result
```

而不是: 

```
JSON Payload

Business Data

Configuration

Device Inventory
```

这样日志职责保持单一. 

## Hands-on Lab

首先导入 Chapter 8 的 Logger `from modules.logger import logger`

修改: 

```python
def get(url):
    try:

        logger.info(f"HTTP GET {url}")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT
        )

        logger.info(
            f"HTTP Response {response.status_code}"
        )

        if not _check_status(response):
            logger.error(
                f"HTTP Error {response.status_code}"
            )
            return None

        return response

    except requests.RequestException as error:

        logger.error(
            f"HTTP Request Failed: {error}"
        )

        return None
```

POST保持一致 `logger.info(f"HTTP POST {url}")`

随后记录: 

```python
logger.info(
    f"HTTP Response {response.status_code}"
)
```

保持统一格式. 

## 为什么记录两次? 

有人可能觉得只记录 200 是不是够了? 实际上一次请求包含两个重要事件. 

第一, 请求发送 `GET /devices`

第二, 服务器响应 `200`

如果第二条日志没有出现, 说明请求可能超时. 或者程序异常退出. 

因此请求响应分别记录, 更容易排查问题. 

## Layered Architecture

现在完整的数据流变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ├── Write Request Log
        ├── Apply Timeout
        ├── Send Request
        ├── Handle Exception
        ├── Validate Status
        ├── Write Response Log
        └── Return Response
```

可以看到 Logging 属于 Communication Layer. 

Business Layer 无需重复记录 HTTP. 

## Engineering Analysis

目前 API Client 已经承担: 

Communication Strategy ➡ Logging ➡ Exception Handling ➡ Status Validation ➡ Timeout

Business Logic 越来越简单. 

例如: 

```python
response = api_client.get(url)

if response:
    devices = response.json()
```

整个 HTTP 生命周期已经完全封装. 

## 这正是 Layered Architecture 带来的价值. 

为什么暂时不记录 Response Body? 

很多教程喜欢 `logger.info(response.text)` 但是企业项目通常不会默认这样做. 

原因包括: 

第一, Response Body 可能非常大. 

例如: 几百 KB, 甚至几十 MB. 

第二, Body 可能包含敏感信息. 

例如: Token, Password, API Key. 

第三, 绝大多数通信故障只需要 Method, URL, Status Code 即可定位. 

因此默认 Communication Log 应保持精简. 真正需要分析业务数据时再由 Business Logic 根据需要记录. 

## Engineering Best Practice

通信日志建议保持统一格式. 

例如: 

```
INFO HTTP GET https://server/api/devices

INFO HTTP Response 200

ERROR HTTP Request Failed:
Connection timed out

ERROR HTTP Error 404
```

这种格式便于: 

- 阅读. 

- 搜索. 

- 后续导入日志分析平台. 

更重要的是整个项目都保持一致. 

## Engineering Insight

到目前为止，我们已经完成了一个典型企业 HTTP Client 的五项核心能力: 

```
API Client

├── Request
├── Timeout
├── Exception Handling
├── Status Validation
└── Logging
```

注意这里没有增加任何业务功能, 我们一直在完善通信能力. 这正体现了 Workbook 一直强调的思想: 

>优秀的基础模块，不是因为功能复杂，而是因为它把所有共性的能力都集中管理，并以稳定, 统一的接口提供给整个系统. 

未来加入认证(Authentication), Session, 重试(Retry)等能力时，仍然会沿着这一思路继续扩展，而不需要修改任何业务模块. 

## Engineering Checklist

完成本节后，应能够回答以下问题: 

- 为什么 API Client 应使用统一的 Logger，而不是 print()? 

- 为什么请求日志和响应日志应分别记录? 

- Communication Log 应记录哪些信息? 

- 为什么默认不记录完整的 Response Body? 

- Logging 属于 Communication Layer 还是 Business Layer? 

- 当前 API Client 已经集中管理了哪些通信能力? 

## Summary

本节将 Logging 纳入了 api_client.py 的统一职责: 

- 复用了 Chapter 8 建立的统一日志体系. 

- 在请求发送和响应返回两个关键节点记录日志.

- 将日志内容聚焦于通信信息，而非业务数据. 

- 保持 Logging, Timeout, Exception, Status Validation 等通信策略全部集中在 API Client 中. 

至此，api_client.py 已经具备了一个企业级 HTTP 通信模块的基础框架. 接下来，我们将进一步引入Session(会话管理)，解决每次请求重复建立连接的问题，为后续学习认证机制和企业 API 平台打下基础. 

# Lab 10 HTTP Session

这里进入 Session(会话管理). 这是 Chapter 10 中第一个真正体现企业级 HTTP Client 与"教程代码"差异的主题. 

很多入门教程一直使用: 

```python
requests.get(...)
requests.post(...)
```

实际上, 这只是 `requests` 提供的便捷函数. 企业项目几乎都会进一步封装 `requests.Session()`

不过, 这一节我们仍然保持 Vendor Neutral, 不涉及任何具体网络控制器. 

## Theory

到目前为止, 我们一直使用 `requests.get(...)` 或者 `requests.post(...)` 它们都能够正常工作, 但是每一次调用: 

Business Logic ➡ API Client ➡ requests.get() ➡ HTTP Request

都是一次独立的 HTTP 请求, 对于偶尔发送一两个请求来说, 这没有问题, 但是企业自动化平台通常会连续发送: 

- 获取设备列表

- 获取接口信息

- 获取 VLAN

- 获取 ACL

- 获取 Routing Table

可能在几秒钟内发送几十甚至几百个请求. 因此我们需要考虑: 

>这些请求之间能否共享一些通信资源? 

## Engineering Discussion

### 什么是 Session? 

可以把 Session 理解为: 

>客户端与服务器之间的一次持续通信上下文(Communication Context). 

注意这里说的 Session 不是用户登录, 也不是 Authentication 这是两个不同概念, 目前我们只讨论 HTTP Client. 

例如没有 Session: 

```
GET /devices
↓
建立连接
↓
发送请求
↓
关闭连接

──────────────────

GET /interfaces
↓
建立连接
↓
发送请求
↓
关闭连接
```

每一次都是独立流程. 

如果使用 Session: 

```
Session
      │
      ▼
GET /devices
      │
      ▼
GET /interfaces
      │
      ▼
GET /vlans
      │
      ▼
关闭 Session
```

整个过程中一些底层资源可以复用. 

## 为什么企业项目喜欢 Session? 

主要原因有三个. 

第一, 统一管理请求. 

例如: 所有请求都来自同一个 Session, 而不是到处调用: 

```python
requests.get()

requests.post()
```

第二, 共享通信配置. 

例如: 以后如果 Session 已经配置: 

- Header

- Timeout

- Cookie

那么每一次请求都无需重新设置. 

第三, 减少重复建立连接. 虽然底层实现细节超出了本章范围, 但是可以理解为 Session 能够减少重复初始化通信资源. 对于自动化平台尤其重要. 

## Layered Architecture

引入 Session 后通信层变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
HTTP Session
        │
        ▼
HTTP Request
```

注意 Business Logic 仍然不知道 Session. 所有管理全部属于 Connection Layer. 

## Hands-on Lab

首先创建统一 Session. 

```python
import requests

session = requests.Session()
```

随后修改 GET. 

```python
response = session.get(
    url,
    timeout=DEFAULT_TIMEOUT
)
```

POST 修改: 

```python
response = session.post(
    url,
    json=payload,
    timeout=DEFAULT_TIMEOUT
)
```

其他代码完全不用修改. 

## 为什么放在模块顶部? 

很多人会写: 

```python
def get(url):

    session = requests.Session()

    response = session.get(...)
```

这样实际上失去了 Session 存在的意义. 因为每一次调用都会创建新的 Session, 应该整个 API Client 共享一个 Session. 

例如 `session = requests.Session()`

位于模块顶部, 这样所有 GET, POST, PUT, PATCH, DELETE 都使用同一个 Session. 

## Workflow 的变化

现在一次请求变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
Shared Session
        │
        ▼
HTTP Request
```

Business Logic 仍然只有一句 `response = api_client.get(url)` 整个 Session 生命周期已经隐藏. 

## Engineering Analysis

目前 API Client 已经开始拥有自己的状态(State), 以前它只是一些函数. 现在它拥有 Shared Session 虽然目前 Session 里面几乎没有任何配置, 但是后面 Authentication, Cookie, Header 都会放入 Session. 因此这一节实际上是在为后续内容搭建基础设施. 

## 为什么现在不介绍 Cookie? 

很多 HTTP 教程, 介绍 Session 马上开始讲 Cookie, Login, Authentication 本 Workbook暂时不这样安排. 

原因是目前 Session 首先是通信管理工具. 

Authentication 只是后续利用 Session 实现的一项能力. 

按照课程路线先理解 Session. 再理解 Authentication, 学习节奏更加清晰. 

## Engineering Best Practice

企业项目中, 一个 API Client 通常遵循以下原则: 

- 在模块初始化时创建一个共享 Session. 

- 所有 HTTP 请求都通过该 Session 发起. 

- 不在每次请求时重复创建 Session. 

- 将 Session 作为 Connection Layer 的一部分, 而不是暴露给 Business Logic. 

这样做既提高了代码一致性, 也为后续统一管理认证信息, 公共 Header 和连接策略提供了基础. 

## Engineering Insight

这一节最大的变化并不是 `requests.get(...)` 变成了 `session.get(...)` 真正重要的是 API Client 从"一组工具函数"演变成了"一个拥有通信上下文的模块". 

这意味着 HTTP 通信已经开始具有生命周期: 

Create Session ➡ Multiple Requests ➡ Close Session

这种生命周期管理思想, 与我们在 SSH 自动化中管理连接对象的思路是一致的. 

虽然底层协议不同, 但在 Enterprise Automation Platform 中, 它们都属于 Connection Layer, 都需要统一管理连接资源, 而不是在每次调用时重新创建. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- requests.Session() 与 requests.get() 有什么区别? 

- 为什么 Session 应创建一次并重复使用? 

- 为什么不应在每个函数内部创建新的 Session? 

- Session 属于 Business Layer 还是 Connection Layer? 

- 为什么本节没有讨论 Cookie 和 Authentication? 

- 引入 Session 后, API Client 在架构上发生了什么变化? 

## Summary

本节引入了 HTTP Session, 进一步完善了 api_client.py: 

- 使用 requests.Session() 统一管理 HTTP 通信上下文. 

- 所有请求共享同一个 Session, 而不是重复创建. 

- 保持 Session 完全封装在 API Client 内部, 不暴露给 Business Logic. 

- 为后续加入认证, 公共 Header, Cookie 管理等能力奠定了基础. 

至此, api_client.py 已经具备了企业级 HTTP Client 的核心框架: 共享 Session, 统一请求发送, 统一超时控制, 统一异常处理, 统一状态码验证以及统一日志记录. 后续章节将在这一框架上逐步增加认证和更高级的通信能力, 而无需改变上层业务模块. 

# Lab 11 Internal Request Engine

很好, 现在 Session 已经建立. 下一步不应该立即讲 Authentication, 因为目前还有一个更基础的问题没有解决. 

我们的代码仍然是 `response = session.get(url)` 或者 `response = session.post(url, json=payload)` 虽然已经比前面好了很多, 但是还有一个明显的问题 GET 和 POST 出现了大量重复代码. 

例如: 

- Logging

- Timeout

- Exception Handling

- Status Validation

这些代码几乎完全一样. 企业工程下一步应该做的, 就是消除重复代码(Code Duplication), 这也是前面几章一直坚持的 DRY Principle. 

## Theory

目前 `api_client.py` 大致结构如下: 

```python
def get(url):

    logger.info(...)

    try:

        response = session.get(...)

        ...

        return response

    except ...

        ...
```

POST: 

```python
def post(url, payload):

    logger.info(...)

    try:

        response = session.post(...)

        ...

        return response

    except ...

        ...
```

可以发现除了 `session.get(...)` 和 `session.post(...)` 其它代码几乎一样. 

这意味着我们已经出现重复逻辑. 

## Engineering Discussion

### 为什么重复代码不好? 

假设以后需要记录 Request Duration. 

现在需要修改 GET, POST, 未来 PUT, PATCH, DELETE 全部都要修改. 

如果以后增加 Retry 仍然修改五六个函数. 

很明显这些能力属于所有 HTTP Request 的共性能力. 

因此应该集中, 而不是复制. 

## 提炼共同流程

仔细观察 GET, POST 真正不同的. 

只有这一行 `session.get(...)` 或者 `session.post(...)` 其它步骤完全一致. 

整个流程实际上都是: 

Write Request Log ➡ Send Request ➡ Handle Exception ➡ Validate Status ➡ Write Response Log ➡ Return Response

因此我们可以把整个流程抽象出来. 

## Layered Architecture

新的结构: 

```
Business Logic
        │
        ▼
api_client.get()
        │
        ▼
_request()
        │
        ▼
Session
        │
        ▼
HTTP
```

注意现在 GET, POST 已经不是真正发送请求. 而是调用统一 Request Engine. 

## Hands-on Lab

新增内部函数: 

```python
def _request(method, url, **kwargs):
    """
    Send an HTTP request.

    Args:
        method (str): HTTP method.
        url (str): API endpoint.

    Returns:
        requests.Response | None
    """

    logger.info(f"{method} {url}")

    try:

        response = session.request(
            method=method,
            url=url,
            timeout=DEFAULT_TIMEOUT,
            **kwargs
        )

        logger.info(
            f"HTTP Response {response.status_code}"
        )

        if not _check_status(response):
            logger.error(
                f"HTTP Error {response.status_code}"
            )
            return None

        return response

    except requests.RequestException as error:

        logger.error(
            f"HTTP Request Failed: {error}"
        )

        return None
```

这里第一次使用 `session.request(...)` 需要说明. 它不是新的协议, 也不是新的库. 而是 Session 提供的**通用请求接口**. 

## 简化 GET

现在 GET 变成: 

```python
def get(url):

    return _request(
        "GET",
        url
    )
```

整个函数只剩下一行. 

## 简化 POST

POST 也变成: 

```python
def post(url, payload):

    return _request(
        "POST",
        url,
        json=payload
    )
```

可以发现 POST 真正特殊的只有 `json=payload` 其它工作全部交给 `_request(). `

## 为什么使用 `_request()`? 

有人可能会问为什么不继续: 

```python
session.get()

session.post()
```

原因是企业工程真正关心的是请求生命周期. 而不是 HTTP Method. 现在所有 Method 都共享同一个生命周期. 

Request ➡ Logging ➡ Timeout ➡ Exception ➡ Status Validation ➡ Return

这就是 Request Engine 存在的意义. 

## Workflow 的变化

现在一次 GET 实际上变成: 

Business Logic ➡ get() ➡ _request() ➡ session.request() ➡ HTTP

POST 也是同样流程, 未来 PUT, PATCH, DELETE 无需重新实现. 只需要调用 `_request(...)` 即可. 

## Engineering Analysis

这一节最大的变化不是代码减少了, 真正重要的是我们完成了流程抽象(Workflow Abstraction). 

以前 GET 拥有自己的流程. POST 拥有自己的流程. 

现在整个 HTTP Client 只有一套流程. 

以后如果增加 Retry. 

例如: 

Logging ➡ Retry ➡ Timeout ➡ Exception ➡ Status Validation

只需要修改 `_request()` 整个项目全部生效. 

## 为什么 `_request()` 是内部函数? 

注意函数名 `_request()` 前面的 `_` 表示内部实现. 

Business Logic 永远不会调用 `_request(...)`

Business Logic 应该使用: 

```python
api_client.get()

api_client.post()
```

这样 API Client 仍然保持简单, 稳定, 易读. 

## Engineering Best Practice

成熟的 HTTP Client 通常都会有一个统一的请求入口: 

- 所有 HTTP Method 共用同一个请求流程. 

- 将日志, 超时, 异常处理, 状态码验证等共性能力集中管理. 

- 让各个 Method 只负责表达自己的业务语义(GET, POST, PUT 等), 而不是重复实现通信细节. 

这种设计既符合 DRY Principle, 也使得后续扩展功能几乎只需要修改一个地方. 

## Engineering Insight

这一节实际上完成了 `api_client.py` 的最后一次重要重构. 

到目前为止: 

```
API Client

├── Shared Session
├── Request Engine (_request)
├── Logging
├── Timeout
├── Exception Handling
├── Status Validation
├── GET
└── POST
```

请注意 `GET()` 和 `POST()` 已经不再是真正的"实现者". 

它们只是: 

>公开接口(Public Interface). 

真正完成工作的, 是 `_request()` 这种设计在企业软件中非常常见: 

- 对外提供简单, 稳定的接口. 

- 对内使用统一的执行引擎. 

前面 Chapters 中: 

- Renderer 隐藏了 Jinja2 的细节. 

- Connection Module 隐藏了 Netmiko 的细节. 

现在: 

API Client 隐藏了整个 HTTP 请求生命周期. 

整个 Workbook 的工程风格至此保持了高度一致. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么 GET 和 POST 会出现重复代码? 

- `_request()` 解决了什么问题? 

- 为什么使用 `session.request()` 而不是分别调用 `session.get()` 和 `session.post()`? 

- 为什么 `_request()` 应设计为内部函数? 

- 未来新增 PUT, PATCH, DELETE 时, 为什么几乎不用复制代码?

- 这一重构体现了哪些工程原则(如 DRY, Layered Architecture)? 

## Summary

本节完成了 `api_client.py` 的一次关键重构: 

- 提炼出统一的 `_request()` 请求引擎. 

- 将 Logging, Timeout, Exception Handling 和 Status Validation 等共性能力集中到一个位置. 

- 让 `get()`, `post()` 等公开接口只负责表达 HTTP Method, 而不再承担请求流程的实现. 

至此, 我们已经拥有了一个结构清晰, 职责明确的企业级 HTTP Client 骨架. 后续加入认证(Authentication), 默认请求头, 重试(Retry)或其他通信策略时, 都可以直接扩展 `_request()` 或共享 Session, 而无需修改上层业务代码或各个 HTTP Method 的接口. 

# Lab 12 API Client Configuration 

到这里, `api_client.py` 的整体架构已经基本稳定. 接下来, 不应该立刻介绍 Bearer Token、Basic Authentication 或 Cisco DNA Center API. 

因为还有一个企业工程中必须解决的问题: 

>Configuration(配置管理)

目前我们的代码仍然存在大量"硬编码(Hard Coding)". 

例如: `DEFAULT_TIMEOUT = 10`

或者: `url = "https://jsonplaceholder.typicode.com/posts/1"`

这些配置写在代码里面, 对于实验没有问题, 但是对于企业项目来说, 这是一个明显的设计缺陷. 

因此, 本节开始讨论 API Client Configuration

## Theory(理论)

回顾前面的章节, Chapter 5 我们学习了 Data-Driven Automation 核心思想就是数据与程序分离. 

Chapter 6 我们又学习了 YAML, JSON

目的也是: 

>将可变化的数据放到外部. 

因此 Chapter 10 的 API Client, 应该继续遵循相同原则. 

## Engineering Discussion

### 什么属于配置? 

观察目前的代码. 

例如: `DEFAULT_TIMEOUT = 10` 它是不是业务逻辑? 

不是. 

是不是 HTTP 协议? 

也不是. 

它只是运行参数(Runtime Configuration)

同样: https://jsonplaceholder.typicode.com 也不是程序逻辑. 而是服务器地址. 因此它也属于 Configuration. 

### 什么不属于配置? 

例如: `response = session.request(...)` 这是程序行为. 属于 Business Logic. 不应该放入 YAML, 否则配置文件开始决定程序执行流程, 整个系统就会越来越难维护. 

因此我们需要区分: 

| 类型                | 是否属于 Configuration |
| ------------------ | ------------------ |
| Timeout            | Yes                |
| Base URL           | Yes                |
| Verify SSL         | Yes                |
| Default Headers    | Yes                |
| HTTP Method        | No                 |
| Request Workflow   | No                 |
| Exception Handling | No                 |

这也是企业项目中非常重要的边界. 

## Layered Architecture

现在配置开始加入系统. 

架构变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
Configuration
        │
        ▼
Session
        │
        ▼
HTTP
```

注意 Configuration 影响 API Client, 但是 Business Logic 不知道 Timeout 是多少. 

## Hands-on Lab

建立: 

```
automation_project/

config/

    api.yaml
```

例如: 

```yaml
timeout: 10

verify_ssl: true

base_url: https://jsonplaceholder.typicode.com
```

注意目前只有三个配置不要一次增加几十项, 保持简单. 

## 读取配置

回顾 Chapter 6 可以继续使用: `from modules import loader`

假设: Chapter 6 已经拥有统一 YAML Loader. 

那么 API Client 只需要: 

```python
config = loader.load_yaml(
    "config/api.yaml"
)
```

随后: 

```python
DEFAULT_TIMEOUT = config["timeout"]
VERIFY_SSL = config["verify_ssl"]
BASE_URL = config["base_url"]
```

可以发现 HTTP Client 已经不再依赖硬编码. 

## 为什么不是 Environment Variable? 

很多教程会说应该全部使用 Environment Variable. 

例如: 

```
API_TIMEOUT

API_SERVER

VERIFY_SSL
```

对于大型生产系统这是常见方案, 但是对于当前 Workbook 我们已经建立 YAML Configuration Framework. 

因此继续保持一致. 不要为了介绍一种新技术, 破坏整个课程的统一架构. 后续如果涉及部署环境, 再讨论 Environment Variable 的作用. 

## Workflow 的变化

现在请求流程变成: 

```
Configuration
        │
        ▼
API Client
        │
        ▼
_request()
        │
        ▼
Session
        │
        ▼
HTTP
```

Business Logic 仍然只有 

```python
response = api_client.get("/posts/1")
```

甚至 URL 都可以进一步简化. 

## Base URL

目前代码: 

```python
url = "https://jsonplaceholder.typicode.com/posts/1"
```

实际上每一次都重复: `https://jsonplaceholder.typicode.com`

因此 API Client 完全可以负责拼接. 

例如: 

```python
Business Logic: 

response = api_client.get(
    "/posts/1"
)
```

API Client 内部: 

```python
url = BASE_URL + endpoint
```

最终发送 `https://jsonplaceholder.typicode.com/posts/1`

Business Logic 开始真正脱离 HTTP 地址. 以后服务器迁移. 

例如: 

api.company.com ➡ api2.company.com

只需要修改配置文件. 

整个项目无需修改代码. 

## Engineering Analysis

这里实际上体现了前几章一直强调的一句话: 

>变化的东西放到配置, 不变化的东西放到代码. 

观察目前所有内容变化的: 

- Timeout

- Base URL

- SSL Verification

固定的: 

- Request Engine

- Status Validation

- Exception Handling

- Logging Workflow

这种划分让整个 API Client 既灵活, 又稳定. 

## Engineering Best Practice

一个成熟的 API Client 通常会把以下内容作为配置项: 

- Base URL

- Timeout

- SSL Verification

- 默认请求头(后续章节)

- 默认认证方式(后续章节)

而请求生命周期、异常处理、日志记录等通信流程, 应保持在代码中实现, 而不是交给配置文件控制. 

## Engineering Insight

到这里, api_client.py 已经完成了从"代码示例"到"可配置通信模块"的演进. 

整个模块已经具备了三个明显的企业特征: 

```
API Client

├── Stable Public Interface
├── Centralized Communication Logic
└── Externalized Configuration
```

这三者共同决定了模块的可维护性. 

未来如果企业需要: 

- 更换 API Server. 

- 调整 Timeout. 

- 修改 SSL 策略. 

都可以通过配置完成, 而无需修改业务代码或请求流程. 

这正是前面 Chapter 5 与 Chapter 6 所建立的数据驱动思想, 在 API Automation 中的自然延续. 

## Engineering Checklist

完成本节后, 应能够回答以下问题? 

- 为什么 Timeout 应属于配置, 而不是业务逻辑? 

- 哪些内容适合放入配置文件? 哪些不适合? 

- 为什么 Base URL 应集中管理? 

- 为什么本 Workbook 当前阶段继续采用 YAML, 而不是 Environment Variable? 

- "变化的东西放到配置, 不变化的东西放到代码" 在 API Client 中是如何体现的? 

- 引入配置后, Business Logic 获得了哪些好处? 

## Summary

本节为 `api_client.py` 引入了统一配置管理: 

- 将 Timeout、Base URL、SSL Verification 等运行参数从代码中剥离. 

- 复用前面章节建立的 YAML 配置框架, 保持整个 Workbook 的一致性. 

- 让 API Client 成为一个可配置、可扩展的通信模块, 而不是依赖硬编码的示例程序. 

至此, `api_client.py` 已经具备了企业级 HTTP Client 的核心组成部分: **统一接口、共享 Session、统一请求引擎、集中通信策略以及外部配置管理**. 下一节将在这一基础上引入Authentication(认证), 说明如何在不破坏现有架构的前提下, 为所有请求统一添加认证信息. 

# Lab 13 HTTP Authentication

## Theory

HTTP 本身是一种通信协议. 

协议负责: Client ➡ Server 之间的数据传输. 

至于客户端是否有权限访问服务器这并不是 HTTP Protocol 自己决定的. 

因此各种 API 平台都会建立自己的 Authentication Mechanism(认证机制). 

例如: 

HTTP ➡ Authentication ➡ Business API

也就是说 HTTP 提供通信能力, Authentication 提供身份验证能力. 两者虽然一起工作, 但职责不同. 

## Engineering Discussion

### Authentication 属于 Business Logic 吗? 

假设 Business Logic: `devices = api_client.get("/devices")`

如果业务代码需要写: 

```python
headers = {
    "Authorization": "Bearer xxxxxxxxx"
}
```

然后: 

```python
requests.get(
    url,
    headers=headers
)
```

那么 Authentication 就开始散落到整个项目. 

例如: 

```
Inventory
↓
Authorization

────────────────

Compliance
↓
Authorization

────────────────

Monitoring
↓
Authorization
```

以后 Token 更新, Header 修改所有模块都要修改. 

这显然违反了  Single Responsibility Principle. 

## Authentication 属于哪一层? 

回顾目前架构: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
Session
        │
        ▼
HTTP
```

Authentication 本质上属于 Communication Strategy. 

因为它影响每一次 HTTP Request. 

因此应该放入 API Client, 而不是 Business Logic. 

## Layered Architecture

加入认证以后: 

```
Business Logic
        │
        ▼
API Client
        │
        ├── Session
        ├── Authentication
        ├── Timeout
        ├── Logging
        └── Request Engine
```

Business Logic 永远不知道 Header 如何构造, 也不知道 Token 放在哪里. 

## Authentication 与 Header 的关系

前面章节已经学习过 HTTP Header 保存的是通信元数据(Metadata).  Authentication 也是 Header 的一部分. 

例如: `Authorization: Bearer xxxxxxxxx`

或者: `Authorization: Basic xxxxxxxxx`

因此认证实际上只是 API Client 构造 Header 时增加的一项内容. 它并不会改变 Business Logic. 

## Hands-on Lab

首先修改配置文件. 

```yaml
timeout: 10

verify_ssl: true

base_url: https://jsonplaceholder.typicode.com

authentication:
  enabled: false
  type: bearer
  token: ""
```

注意目前即使测试 API 并不需要认证, 我们仍然建立配置结构. 这是为了工程一致性. 

## API Client 初始化

读取配置: 

```python
AUTH_ENABLED = config["authentication"]["enabled"]
AUTH_TYPE = config["authentication"]["type"]
AUTH_TOKEN = config["authentication"]["token"]
```

目前不要立即实现各种认证方式. 先建立配置入口. 

## Header Construction

新增内部函数: 

```python
def _build_headers():
    """
    Build default HTTP headers.
    """

    headers = {}

    if AUTH_ENABLED:

        if AUTH_TYPE == "bearer":

            headers["Authorization"] = (
                f"Bearer {AUTH_TOKEN}"
            )

    return headers
```

这里要注意 Business Logic 完全不知道 Header. 所有 Header 全部由 API Client 负责生成. 

## 修改 Request Engine

现在: 

```python
response = session.request(
    method=method,
    url=url,
    timeout=DEFAULT_TIMEOUT,
    verify=VERIFY_SSL,
    headers=_build_headers(),
    **kwargs
)
```

整个 Authentication 已经加入 Request Engine. 

GET, POST 无需任何修改. 

## Workflow 的变化

整个请求生命周期进一步完善. 

```
Business Logic
        │
        ▼
_request()
        │
        ├── Build Headers
        ├── Authentication
        ├── Logging
        ├── Timeout
        ├── Send Request
        ├── Exception Handling
        ├── Status Validation
        └── Return Response
```

可以看到 Authentication 只是 Request Engine 中的一个步骤. 而不是新的 Workflow. 

## 为什么先支持一种认证方式? 

目前我们只保留 Bearer 配置. 原因不是 Bearer 最重要, 而是我们要先建立 Authentication Framework. 

以后如果增加:

```
Basic

API Key

Custom Header
```

甚至 Vendor Authentication, 都只是扩展 `_build_headers()` 而不是修改整个 API Client. 

## Engineering Analysis

这里体现了一个重要的工程原则: 

>新增能力，应尽量扩展已有模块，而不是改变已有接口. 

注意 Business Logic 仍然调用 `api_client.get("/devices")` 

接口完全没有变化. 

Authentication 是在 API Client 内部增加的能力. 因此整个项目没有任何业务代码需要修改. 

这正是稳定接口(Stable Interface)带来的价值. 

## Engineering Best Practice

企业项目中，建议遵循以下原则: 

- 所有认证信息集中在配置中管理. 

- 所有认证 Header 由 API Client 统一生成. 

- Business Logic 永远不要直接拼接 Authorization Header. 

- 新增认证方式时，只扩展 Header 构建逻辑，不修改公共接口. 

这样既保证了安全性，也降低了后续维护成本. 

## Engineering Insight

请注意这一节真正建立的并不是 Bearer Token, 而是 Authentication Pipeline(认证流程). 

以后无论接入哪个厂商平台. 

例如: 

```
Cisco

Juniper

Arista

Palo Alto
```

Business Logic 都不会知道认证如何完成. 

它只负责调用: `api_client.get(...)` 认证机制. 

作为 Connection Layer 的一部分统一管理. 这与 SSH Automation 中 Connection Module 负责建立 SSH 登录, Business Logic 只负责发送命令本质上完全一致. 

## Engineering Checklist

完成本节后，应能够回答以下问题: 

- 为什么 Authentication 应属于 API Client，而不是 Business Logic? 

- Authentication 与 HTTP Header 有什么关系? 

- 为什么 Header 应由 _build_headers() 统一生成? 

- 为什么认证信息应放入配置文件? 

- 为什么新增认证方式不应修改 get()、post() 的接口? 

- 本节建立的是一种认证方式，还是整个认证框架? 

## Summary

本节为 `api_client.py` 引入了统一的认证框架: 

- 将认证配置纳入 YAML 配置管理. 

- 使用 _build_headers() 统一构造认证 Header. 

- 将认证流程集成到 _request() 中，而不改变公开接口. 

- 保持 Business Logic 与认证机制完全解耦. 

至此，`api_client.py` 已经形成了一个完整的企业级通信模块: 配置管理、共享 Session、统一请求引擎、日志、超时、异常处理、状态码验证以及认证管理. 后续学习具体 API 平台时，我们将直接复用这一框架，而无需重新设计通信层. 

# Lab 14 Business Logic and Api Client

## Theory

目前 Business Logic 调用 `response = api_client.get("/posts/1")` 然后 `data = response.json()` 虽然已经能够工作, 但是这里仍然存在一个问题. 

Business Logic 仍然知道 `response.json()`

也就是说 Business Logic 开始接触 HTTP Response. 

而不是业务对象. 

随着项目越来越复杂, 这会产生新的耦合. 

## Engineering Discussion

### 我们真正想获取的是什么? 

例如业务代码: `devices = get_devices()` 真正关心的是设备列表而不是 HTTP Response

Business Logic 不应该思考: 

```
Status Code

Response Header

HTTP Body
```

这些都属于 Communication Layer. 

Business Logic 真正关心的是 Python Object

例如: 

```python
[
    {
        "hostname": "R1"
    },
    {
        "hostname": "R2"
    }
]
```

### 为什么现在还不能修改 API Client? 

很多人看到这里, 会想到: 

```python
def get(...):
    ...
    return response.json()
```

前面我们已经讨论过, 目前不要这样设计. 原因是 API Client 负责 HTTP 而不是业务. 因此真正负责把 HTTP 转换成业务对象, 应该是 Service Layer. 

## 引入新的模块

现在平台开始增加新的一层. 

```
Business Logic
        │
        ▼
Service Layer
        │
        ▼
API Client
        │
        ▼
HTTP
```

注意这里 Service 不是 HTTP, 也不是 Business. 它负责把 API 转换成业务接口. 

## 为什么需要 Service Layer? 

例如以后业务需要设备列表. 

Business Logic 希望: 

```python
devices = inventory_service.get_devices()
```

而不是: 

```python
response = api_client.get("/devices")

devices = response.json()
```

因为 HTTP 已经泄漏到 Business Logic. 

## Hands-on Lab

建立: 

```
modules/

    inventory_service.py
```

第一版: 

```python
from modules import api_client


def get_posts():
    """
    Retrieve posts from the API.
    """

    response = api_client.get("/posts")

    if response is None:
        return None

    return response.json()
```

注意这里只有一句: `return response.json()` 这不是 API Client 负责, 而是 Service Layer 负责. 

## Workflow

脚本: 

```
scripts/

    get_posts.py
```

变成: 

```python
from modules import inventory_service

posts = inventory_service.get_posts()

if posts is None:
    print("Failed.")

else:

    print(posts)
```

Business Logic 现在完全不知道 HTTP, 甚至不知道 Response. 

## Layered Architecture

整个系统第一次真正形成完整分层. 

```
Workflow Script
        │
        ▼
Business Service
        │
        ▼
API Client
        │
        ▼
HTTP
        │
        ▼
API Server
```

这里每一层都有独立职责. 

## 职责划分

现在各层职责已经非常清晰. 

### Script

负责: 

- Workflow

- 调度模块

- 输出结果

不知道 HTTP. 

### Service

负责: 

- 调用 API

- 转换业务对象

- 返回 Python 数据

不知道 Session. 

### API Client

负责: 

- Session

- Authentication

- Logging

- Timeout

- Exception

- HTTP

不知道设备. 

### API Server

负责真正的数据. 

## Engineering Analysis

很多企业项目最大的错误就是业务模块直接调用 `requests.get(...)` 然后 `response.json()` 最后开始处理业务数据. 

结果 HTTP 彻底进入业务层. 以后如果通信方式发生变化. 

例如: REST API

变成: GraphQL. 

或者: SDK. 

整个项目都会受到影响. 

增加: Service Layer

以后 Business Logic 始终面对业务对象, 而不是通信对象. 

## 与前面章节的一致性

回顾 Chapter 8: 

```
Workflow
↓
Renderer
↓
Deployment
```

Chapter 9: 

```
Workflow
↓
Compliance
↓
Connection
```

Chapter 10 保持相同风格: 

```
Workflow
↓
Service
↓
API Client
```

可以发现整个 Workbook 的工程思想完全一致: 

>Workflow 不直接接触底层通信, 而是通过具有明确职责的中间模块完成业务. 

## Engineering Best Practice

在企业项目中, 建议保持以下原则: 

- Script 只负责流程控制. 

- Service 负责业务语义和数据转换. 

- API Client 负责 HTTP 通信. 

- 不要在 Script 中直接调用 response.json(). 

- 不要在 Service 中处理 Session、Header 或 Authentication. 

每一层都应只关注自己的职责. 

## Engineering Insight

这一节最大的意义, 不是新增了 inventory_service.py. 

而是完成了 HTTP 与业务之间的最后一次解耦. 

到目前为止: 

Business Object ➡ Service ➡ HTTP Response ➡ API Client ➡ HTTP

HTTP 已经不再向上传播. 

Business Logic 面对的始终是 Python Business Object. 

这意味着, 未来无论底层通信方式如何变化, 只要 Service 的接口保持稳定, 上层业务代码都无需修改. 

这正是企业软件中"稳定接口、隔离变化"的核心设计思想. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么 Business Logic 不应直接调用 response.json()? 

- 为什么需要新增 Service Layer? 

- Service Layer 与 API Client 的职责有什么区别? 

- 为什么 API Client 不应返回业务对象? 

- Script、Service、API Client 三层分别负责什么? 

- 这一设计与 Chapter 8、Chapter 9 的模块划分有哪些一致性? 

## Summary

本节为 Chapter 10 引入了 Service Layer: 

- 将 HTTP Response 到业务对象(Python Object)的转换放入 Service, 而不是 API Client. 

- 保持 API Client 专注于通信职责, Service 专注于业务语义. 

- 让 Workflow Script 只调用业务接口, 而无需了解 HTTP 细节. 

至此, Chapter 10 的整体架构已经形成: 

```
Workflow Script
        │
        ▼
Business Service
        │
        ▼
API Client
        │
        ▼
HTTP Session
        │
        ▼
API Server
```

这一架构与前面章节建立的分层思想完全一致, 也为后续接入真实的网络控制器 API(如 Cisco Catalyst Center、Cisco Meraki、Cisco SD-WAN 等)提供了稳定、可扩展的基础. 

# Lab 15 API Interface Design

Theory

目前我们的 Service Layer: 

```python
posts = inventory_service.get_posts()
```

看起来已经很好, 但是如果整个项目继续发展. 

很快就会出现: 

```python
get_posts()

get_users()

get_comments()

get_devices()

get_interfaces()

get_routes()

get_vlans()
```

随着 API 越来越多 Service Layer 会越来越庞大, 因此我们需要建立统一的接口设计原则. 

## Engineering Discussion

### 面向 HTTP 设计? 

很多初学者喜欢这样设计: 

```python
api_client.get(...)

api_client.post(...)

api_client.put(...)

api_client.delete(...)
```

然后 Business Logic 自己决定什么时候 GET, 什么时候 POST. 

这种设计实际上是面向 HTTP, 而不是面向业务. 

例如 Workflow: `api_client.post("/devices", payload)`

Workflow 开始知道 HTTP Method, Endpoint, URL

实际上 HTTP 已经泄漏到了业务层. 

### 面向业务设计

真正希望看到的是: 

```python
device_service.create_device(device)

device_service.get_devices()

device_service.delete_device(device_id)
```

注意 Business Logic 已经不知道 HTTP. 它看到的是业务动作. 

例如: 

```
Create Device

Delete Device

Update Device
```

而不是: 

```
GET

POST

PUT

DELETE
```

## Interface Mapping

实际上 Service Layer 负责完成: 业务动作 ➡ HTTP Method 的映射. 

例如: 

```
create_device()
↓
POST

────────────────

get_devices()
↓
GET

────────────────

update_device()
↓
PUT

────────────────

delete_device()
↓
DELETE
```

Business Logic 完全不需要知道 HTTP. 

## Layered Architecture

现在真正形成业务接口. 

```
Workflow
      │
      ▼
create_device()
      │
      ▼
Service
      │
      ▼
POST /devices
      │
      ▼
API Client
      │
      ▼
HTTP
```

可以发现 HTTP Method 已经停留在 Service 以下不会继续传播. 

## Hands-on Lab

假设未来我们需要设备管理可以建立: 

```
modules/

    device_service.py
```

例如: 

```python
from modules import api_client


def get_devices():

    response = api_client.get("/devices")

    if response is None:
        return None

    return response.json()


def create_device(device):

    response = api_client.post(
        "/devices",
        device
    )

    if response is None:
        return None

    return response.json()
```

这里要注意 Service 没有 Authentication, 没有 Timeout, 没有 Session, 也没有 Status Code, 它只负责业务动作. 

## Workflow

Script 进一步简化. 

例如: 

```python
from modules import device_service

devices = device_service.get_devices()

for device in devices:
    print(device)
```

Workflow 甚至不知道这是 REST API. 它只知道获取设备. 

## 为什么 Service 不叫 API? 

很多项目会出现 `device_api.py` 或者 `rest_api.py`

本 Workbook 推荐 `device_service.py` 原因是它提供的是业务服务(Business Service) 而不是 HTTP API. 

对于 Workflow 来说这里就是一个业务模块, 底层到底是 REST, NETCONF, SDK, GraphQL, Workflow 都不需要知道. 

## Engineering Analysis

现在整个项目已经形成两种不同层次的 API. 

第一种: HTTP API. 

例如: 

```
GET /devices

POST /devices
```

这是服务器提供的接口. 

第二种: Python API. 

例如: 

```python
device_service.get_devices()

device_service.create_device()
```

这是我们自己的平台提供的接口. 

Business Logic 真正依赖的是第二种, 而不是第一种, 这一点非常重要. 

因为: 

>企业自动化平台本质上就是在各种外部 API 之上, 建立一套稳定、统一、符合业务语义的内部接口. 

## Engineering Best Practice

一个成熟的 Service Layer 通常遵循以下原则: 

- 使用业务动作命名函数, 而不是 HTTP Method. 

- 每个函数表达一个明确的业务能力. 

- 将 Endpoint、HTTP Method 和请求细节封装在 Service 内部. 

- 返回 Python 业务对象, 而不是 HTTP Response. 

这样可以让上层 Workflow 始终围绕业务流程编写, 而不是围绕通信协议编写. 

## Engineering Insight

这一节实际上完成了整个 Workbook 一个非常重要的目标: 

>从"调用别人提供的 API", 提升到"设计自己的 API". 

从这一刻开始, 我们的平台本身也拥有了一套 API: 

```python
device_service.get_devices()

device_service.create_device()

device_service.delete_device()
```

这些接口不属于 requests, 也不属于任何厂商, 而是属于我们的自动化框架. 

未来如果底层平台从一个 REST API 更换到另一个 REST API, 甚至更换为 SDK, 只要保持这些 Service 接口不变, 所有 Workflow 都可以继续工作. 

这就是企业软件中常说的: 

>面向稳定接口编程, 而不是面向具体实现编程. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么 Business Logic 不应直接使用 HTTP Method? 

- Service Layer 为什么应使用业务动作命名? 

- HTTP API 与我们自己设计的 Python API 有什么区别? 

- 为什么推荐使用 `device_service.py`, 而不是 `device_api.py`? 

- Service Layer 如何完成业务动作到 HTTP Method 的映射? 

- 这一设计如何降低未来更换底层 API 的成本? 

## Summary

本节完成了 Chapter 10 从"使用 API"到"设计 API"的重要转变: 

- 将 Service Layer 定义为业务接口层, 而不是 HTTP 接口层. 

- 使用业务语义(如 `get_devices()`、`create_device()`)作为公开接口. 

- 将 Endpoint、HTTP Method 和请求细节完全封装在 Service 内部. 

- 建立了属于 Enterprise Automation Platform 自己的 Python API. 

# Lab 16 Error Handling Strategy

## Theory

目前我们的调用流程是: 

```
Workflow
    │
    ▼
Service
    │
    ▼
API Client
    │
    ▼
HTTP Server
```

在前面的章节中, `api_client.py` 已经负责: 

- Communication Exception

- Timeout

- HTTP Status Validation

- Logging

例如: 

```python
response = api_client.get("/devices")

if response is None:
    ...
```

这里已经说明 API Client 能够发现通信失败, 但是它不知道业务应该怎么办. 

## Engineering Discussion

假设 Workflow: `devices = device_service.get_devices()`

如果服务器返回: `404 Not Found`

API Client 能知道 HTTP 请求失败, 但是它不知道设备不存在, 还是 URL 写错, 还是服务器升级了.

这些都属于: **业务语义(Business Semantics)**. 

因此不能由 API Client 决定. 

### API Client 的职责

API Client 应该负责: 

HTTP ➡ Connection ➡ Status Code ➡ Response

例如: 

```python
logger.error(
    "HTTP Error 404"
)
```

到这里它的职责已经结束. 

### Service 的职责

Service 才知道当前请求是什么. 

例如: `def get_devices():` 如果失败 Service 可以决定: 

```
返回 None

或者

返回空列表

或者

重新组织错误信息
```

因为 Service 知道这是获取设备. 而不是获取用户. 

### Workflow 的职责

Workflow 最后决定程序应该继续, 还是结束. 

例如: 

```python
devices = device_service.get_devices()

if devices is None:

    print("Unable to retrieve inventory.")

    return
```

Workflow 决定整个流程. 

API Client 永远不要退出程序. 

例如不要 `exit()` 或者 `raise SystemExit` 因为通信模块, 没有资格决定整个程序生命周期. 

## Layered Error Handling

整个错误处理流程: 

```
HTTP Error

↓

API Client
(Detect)

↓

Service
(Interpret)

↓

Workflow
(Decide)
```

三个层次职责完全不同. 

## Hands-on Lab

例如: 

```python
device_service.py

from modules import api_client


def get_devices():

    response = api_client.get("/devices")

    if response is None:

        return None

    return response.json()
```

Workflow: 

```python
from modules import device_service


devices = device_service.get_devices()

if devices is None:

    print("Device inventory unavailable.")

else:

    for device in devices:

        print(device)
```

可以看到 Service 没有打印, 没有退出. Workflow 负责最终行为. 

## 为什么不要在 API Client 打印错误? 

很多示例喜欢: `print("Connection failed.")` 甚至: `print("404")` 企业项目一般避免这样设计. 

原因是 API Client 属于 Library. 

Library 应该提供能力, 而不是决定输出方式. 

例如: 有些 Workflow 希望 Console 有些希望 Log File 还有些希望 GUI 或者 Web Dashboard. 因此 API Client 记录日志即可, 最终如何展示由 Workflow 或者 上层应用决定. 

## Error Responsibility Matrix

| 层          | 负责什么             | 不负责什么        |
| ---------- | ---------------- | ------------ |
| API Client | 通信异常、HTTP 状态码、日志 | 业务含义、程序退出    |
| Service    | 将通信结果转换为业务结果     | 控制整个程序流程     |
| Workflow   | 决定重试、退出、提示用户     | 处理 HTTP 通信细节 |

这张职责表, 与前几章建立的分层思想保持一致. 

## Engineering Analysis

这一设计体现了一个重要原则: 

>每一层只处理自己能够理解的信息. 

例如: API Client 理解 404 但不知道 404 意味着设备不存在, 还是用户不存在. 

Service 理解设备 

Workflow 理解整个业务流程. 

因此错误处理也必须分层. 

## Engineering Best Practice

企业自动化项目通常遵循以下规则: 

- API Client 负责检测通信错误并记录日志. 

- Service 将通信错误转换为业务层能够理解的结果. 

- Workflow 决定是否重试、终止流程或通知用户. 

- 不要在底层模块直接调用 print() 或 exit(). 

- 保持错误处理与模块职责一致. 

## Engineering Insight

很多自动化项目的问题, 并不是 HTTP 请求失败. 而是错误处理放错了位置. 

例如: 通信模块直接 `exit()` 导致整个程序结束. 或者业务模块开始解析 Status Code. 导致 HTTP 泄漏到业务层. 

本 Workbook 一直坚持: 

>通信错误留在通信层, 业务决策留在业务层. 

只有这样, 整个自动化框架才能保持清晰、可维护, 也方便后续扩展统一的重试、告警和监控机制. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么 API Client 不应决定程序是否退出? 

- API Client、Service、Workflow 在错误处理上的职责分别是什么? 

- 为什么底层模块不建议使用 print()? 

- 为什么 Workflow 才是决定程序流程的地方? 

- 什么叫"每一层只处理自己能够理解的信息"? 

## Summary

本节建立了企业级 API Automation 的错误处理策略: 

- API Client 检测并记录通信错误. 

- Service 将通信结果转换为业务结果. 

- Workflow 根据业务场景决定后续处理方式. 

至此，Chapter 10 已经建立了完整的通信层设计, 包括: 

```
Workflow
    │
    ▼
Business Service
    │
    ▼
API Client
    ├── Configuration
    ├── Authentication
    ├── Shared Session
    ├── Request Engine
    ├── Logging
    ├── Timeout
    ├── Status Validation
    └── Error Detection
    │
    ▼
HTTP Server
```

这一架构为后续学习真实网络平台的 REST API 提供了统一, 稳定且符合企业工程实践的基础.

# Lab 17 Endpopint Management

到这里, Chapter 10 已经建立了完整的 API Automation 架构, 但是还有一个企业项目中一定会遇到的问题没有讨论：

如何组织 API Endpoint? 

目前我们的代码仍然存在这种写法：

`response = api_client.get("/devices")`

或者：

`response = api_client.get("/interfaces")`

实验没有问题, 但是企业项目里, 一个平台往往有几百个 API Endpoint. 

如果整个项目到处都是：

```
"/devices"

"/interfaces"

"/vlans"

"/routes"

"/users"

"/sites"
```

维护会越来越困难. 

因此, 这一节讨论：Endpoint Management(Endpoint 管理)

## Theory

Endpoint 本质上也是一种数据. 

例如：

```
/devices

/interfaces

/vlans
```

这些都不是程序逻辑, 而是服务器提供的资源路径. 因此Endpoint 不应该散落在整个项目. 

## Engineering Discussion

假设：服务器升级. 

原来：`/devices`

改成：`/network/devices`

如果整个项目有30个地方写着 `"/devices"` 那么需要修改30次. 很明显这违反了 DRY Principle. 

## 集中管理 Endpoint

企业项目通常会建立统一Endpoint 定义. 

例如：

```
modules/

    endpoints.py
```

里面：

```
DEVICES = "/devices"

INTERFACES = "/interfaces"

VLANS = "/vlans"
```

以后 Service 不再写 `api_client.get("/devices")` 

而是 

```
from modules import endpoints

response = api_client.get(
    endpoints.DEVICES
)
```

## 为什么不是写在 api_client.py? 

很多初学者会写：

```python
class APIClient:

    DEVICES = "/devices"
```

这样设计的问题是 API Client 负责 HTTP. 

Endpoint 属于业务资源, 它们不是同一层. 

因此 Endpoint 应该属于 Service Domain, 而不是 Communication Layer. 

## Layered Architecture

现在架构进一步清晰：

```
Workflow
      │
      ▼
Device Service
      │
      ├── Endpoints
      ▼
API Client
      ▼
HTTP
```

API Client 甚至不知道什么叫 Devices. 它只知道收到一个字符串. 

## Hands-on Lab

建立：

```
modules/

    endpoints.py
```

内容：

```python
"""
REST API endpoints.
"""

POSTS = "/posts"

COMMENTS = "/comments"

USERS = "/users"
```

修改 Service：

```python
from modules import api_client
from modules import endpoints


def get_posts():

    response = api_client.get(
        endpoints.POSTS
    )

    if response is None:
        return None

    return response.json()
```

Business Logic 没有任何变化. 

## 为什么使用常量? 

不要 `posts = "/posts"` 

建议全部使用大写. 

```
POSTS

DEVICES

USERS
```

因为它们表示不会在运行过程中改变. 属于模块常量(Module Constants), 这样阅读代码时, 也更容易识别哪些值是固定定义. 

## Endpoint 与 Base URL

还记得前面配置中的：

```yaml
base_url: https://jsonplaceholder.typicode.com
```

现在 API Client 负责：

Base URL + Endpoint

例如：

```
https://jsonplaceholder.typicode.com

+

/posts
```

最终得到：`https://jsonplaceholder.typicode.com/posts`

因此 Service 永远不要自己拼接 `BASE_URL + "/posts"` URL 的组合属于 API Client 的职责. 

## Engineering Analysis

这里再次体现了**变化集中管理**. 

如果：API Server 升级：

/posts ➡ /api/v2/posts

只需要修改：`POSTS = "/api/v2/posts"`

所有 Service 自动完成升级. 这比文搜索 `"/posts"` 更加安全. 

## Engineering Best Practice

成熟的自动化项目通常会：

- 将所有 Endpoint 集中定义. 

- 使用有意义的常量名称. 

- 避免在业务代码中直接书写资源路径. 

- 由 API Client 负责拼接 Base URL 与 Endpoint. 

- Service 只引用 Endpoint 常量, 不处理 URL 细节. 

## Engineering Insight

这一节看起来只是把字符串移动到了另一个文件. 

实际上, 它进一步强化了整个系统的分层：

- Configuration 管理运行参数(Timeout, Base URL, SSL 等). 

- Endpoints 管理资源路径. 

- API Client 管理 HTTP 通信. 

- Service 管理业务语义. 

- Workflow 管理业务流程. 

每一种信息都有唯一的归属位置. 

随着项目规模扩大, 这种"每类信息集中管理"的方式, 会极大降低维护成本和修改风险. 

## Engineering Checklist

完成本节后, 应能够回答以下问题：

- 为什么 Endpoint 不应散落在各个 Service 中? 

- 为什么 Endpoint 应集中定义? 

- 为什么 Endpoint 不属于 API Client? 

- 为什么推荐使用模块常量表示 Endpoint? 

- Base URL 与 Endpoint 分别由哪一层负责? 

- Endpoint 集中管理体现了哪些工程原则? 

## Summary

本节建立了统一的 Endpoint 管理机制：

- 将所有资源路径集中到 endpoints.py. 

- 使用模块常量统一维护 Endpoint. 

- 保持 API Client 专注于 HTTP 通信, Service 专注于业务逻辑. 

- 由 API Client 统一拼接 Base URL 与 Endpoint, 避免 URL 拼接逻辑分散在业务代码中. 

# Lab 18 API Response Processing

到这里，我认为 Chapter 10 已经完成了 Framework(框架)的设计. 

接下来应该开始真正讨论: 

>API Response Processing(API 响应处理)

很多初学者认为: `response.json()` 已经结束了. 实际上，这才是真正业务处理的开始. 

企业自动化项目中，大部分代码不是发送 HTTP Request，而是解析 API 返回的数据. 

因此，本节开始讨论: API Response Processing

## Theory

HTTP Response 可以分成两个部分: 

```
HTTP Response

├── Metadata
└── Payload
```

其中 Metadata 包括: 

- Status Code

- Headers

- Cookies

而真正的业务数据通常位于 Payload(响应内容). 

例如: 

```json
[
    {
        "id": 1,
        "title": "..."
    }
]
```

对于自动化工程来说真正有价值的是 Payload. 

## Engineering Discussion

目前 Service 写成: 

```python
response = api_client.get(endpoints.POSTS)

if response is None:
    return None

return response.json()
```

这里其实隐藏了两个步骤: 

HTTP Response ➡ JSON ➡ Python Object

注意 `response.json(): ` 并不是返回 JSON, 它返回的是 Python 数据结构. 

例如服务器返回: 

```json
{
    "hostname": "R1",
    "ip": "10.0.0.1"
}
```

经过 `response.json()` 以后得到的是: 

```python
{
    "hostname": "R1",
    "ip": "10.0.0.1"
}
```

这是 Python Dictionary, 而不是 JSON 字符串, 这一点要与 Chapter 6 保持一致. 

## API Payload ≠ Business Object

很多教程直接 `devices = response.json()`

然后认为已经得到业务对象, 严格来说还没有.

例如服务器返回: 

```python
{
    "hostname": "R1",
    "managementIp": "10.0.0.1",
    "serialNumber": "ABC123",
    "createdTime": "...",
    "lastUpdated": "...",
    "internalId": "..."
}
```

但是我们的 Workflow 可能真正需要: 

```python
{
    "hostname": "R1",
    "ip": "10.0.0.1"
}
```

很多字段只是平台内部字段, 并不是业务需要. 

## Service 的职责

因此 Service 除了调用 API, 还负责**数据整理(Data Transformation)**. 

例如: 

```python
def get_devices():

    response = api_client.get(endpoints.DEVICES)

    if response is None:
        return None

    devices = []

    for item in response.json():

        devices.append(
            {
                "hostname": item["hostname"],
                "ip": item["managementIp"]
            }
        )

    return devices
```

现在 Workflow 获得的是真正需要的数据, 而不是 API Server 的原始格式. 

## 为什么不要把原始 Payload 传到 Workflow? 

假设 Workflow 需要 `device["managementIp"]` 如果未来厂商升级 API: 

managementIp ➡ ipAddress

整个项目都会失效, 但是如果 Service 统一转换: 

```python
{
    "ip": item["managementIp"]
}
```

那么未来只需要修改Service, Workflow 完全不用改变. 

## Layered Architecture

现在数据流变成: 

HTTP Response ➡ SON Payload ➡ Service Transformation ➡ Business Object ➡ Workflow

注意 Workflow 永远不要依赖 Vendor API 的字段名称. 

## Engineering Analysis

这里体现了另一个重要原则: 

>隔离外部数据模型(External Data Model). 

API Server 返回的数据结构属于外部模型. 

Workflow 使用的数据结构属于内部模型. 

两者之间应该有 Service 作为转换层, 否则整个项目都会依赖外部平台的数据格式, 维护成本非常高. 

## Engineering Best Practice

企业项目通常建议: 

- API Client 返回 Response. 

- Service 完成 JSON 解析. 

- Service 将外部 Payload 转换为内部业务对象. 

- Workflow 只使用内部业务对象. 

- 不要让 Workflow 依赖厂商 API 的字段命名. 

这样可以有效降低厂商 API 变更带来的影响. 

## Engineering Insight

这一节完成了 API Automation 中最后一层解耦.

前面我们已经隔离了: 

- HTTP 通信. 

- Authentication. 

- Endpoint. 

- Configuration. 

现在我们进一步隔离了: **数据模型**, 也就是说即使未来: 

- API Endpoint 改变. 

- 字段名称改变. 

- 返回结构调整. 

只要 Service 保持输出一致, 整个 Workflow 都无需修改. 

这就是企业自动化平台中非常重要的一种能力: 

>屏蔽外部平台的变化，为上层提供稳定的数据模型. 

## Engineering Checklist

完成本节后，应能够回答以下问题: 

- response.json() 返回的是 JSON，还是 Python 对象? 

- 为什么 API Payload 不等于业务对象? 

- 为什么数据转换应由 Service 完成? 

- 为什么 Workflow 不应依赖厂商 API 的字段名称? 

- 什么是外部数据模型? 什么是内部数据模型? 

- Service 如何降低 API 升级带来的影响? 

## Summary

本节建立了 API Response Processing 的工程原则: 

- 将 API 返回的 JSON Payload 与业务对象明确区分. 

- 由 Service 完成 JSON 解析和数据转换. 

- 为 Workflow 提供稳定、统一的内部数据模型. 

- 将外部 API 的数据结构变化限制在 Service 层内部. 

# Lab 19 API Pagination

到这里, 我们已经完成了: 

- HTTP 通信

- API Client

- Service Layer

- Endpoint Management

- Response Processing

但是还有一个在企业 API 自动化中几乎每天都会遇到的问题没有讨论, 如何处理分页(Pagination)? 

很多初学者认为 `devices = device_service.get_devices()` 就能拿到所有设备. 实际上, 大多数企业 API 并不会一次返回全部数据. 

## Theory

为了避免一次返回过大的数据量, REST API 通常会限制单次响应的记录数量. 

例如数据库中有10,000 Devices 服务器可能只返回100 Devices 剩余数据需要继续请求. 

因此一次业务请求可能对应多次 HTTP Request, 这是 Pagination 的本质. 

## Engineering Discussion

假设服务器规定: `GET /devices?page=1&page_size=100`

返回: 第一页. 

继续请求: `GET /devices?page=2&page_size=100`

返回: 第二页. 

直到没有更多数据. 

Workflow 希望得到: `devices = device_service.get_devices()`

而不是: 

```python
page = 1

while True:

    response = api_client.get(...)

    ...
```

为什么? 因为分页属于 API 的通信规则, 不是业务流程. 

## Pagination 应该放在哪一层? 

回顾整个架构: 

```
Workflow
        │
        ▼
Service
        │
        ▼
API Client
        │
        ▼
HTTP
```

API Client 负责发送一次 HTTP Request. 它不知道 "设备列表", 也不知道什么时候停止. 

Service 知道当前业务就是获取所有设备. 

因此分页逻辑应该放在: Service Layer. 

## Hands-on Lab

例如: 

```python
from modules import api_client
from modules import endpoints


def get_devices():

    devices = []

    page = 1

    while True:

        response = api_client.get(
            f"{endpoints.DEVICES}?page={page}"
        )

        if response is None:
            return None

        data = response.json()

        if not data:
            break

        devices.extend(data)

        page += 1

    return devices
```

这里只是演示分页思想. 实 API 分页方式可能不同, 但是 Workflow 始终只有 `devices = device_service.get_devices()`

## 为什么不要让 API Client 自动翻页? 

有人可能会想到为什么不在 `api_client.get()` 里面自动完成所有分页? 

原因是 API Client 不知道什么时候应该翻页. 

例如: 下面两种业务 `get_devices()` 需要全部数据, 但是 `search_devices()` 可能只需要第一页. 

因此 API Client 不能替业务做决定.

## 数据流

现在 Workflow 看到的是 All Devices 而实际发生的是: 

Workflow ➡ Service ➡ GET Page 1 ➡ GET Page 2 ➡ GET Page 3 ➡ Merge Result ➡ Return Devices

整个分页过程被 Service 完全隐藏. 

## Engineering Analysis

分页体现了我们一直坚持的一个原则: 

>一个业务操作, 可以由多个通信操作组成. 

对于 Workflow 来说 "获取设备列表" 只是一个动作, 但是 Service 可以根据平台要求执行一次, 两次, 二十次. HTTP Request, Workflow 完全不需要知道. 这也是为什么通信细节不能泄漏到业务层. 

## Engineering Best Practice

企业自动化项目通常遵循以下原则: 

- API Client 一次只负责一个 HTTP Request. 

- Service 根据业务需要决定是否进行多次请求. 

- Workflow 永远只调用一个业务接口. 

- 将分页、结果合并和数据整理都封装在 Service 中. 

- 不要让 Workflow 处理页码、偏移量或分页 Token. 

## Engineering Insight

分页其实再次证明了 HTTP Request 并不等于业务操作. 前面章节中我们建立了: 

Business Action ➡ Service ➡ HTTP Request

现在进一步发展为: 

```
Business Action

↓

Service

↓

HTTP Request 1

HTTP Request 2

HTTP Request 3

↓

Business Result
```

也就是说一个业务动作. 可以对应多个 HTTP 请求, 而这一复杂性, 应始终由 Service Layer 吸收. 这也是 Service 存在的重要价值之一. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么企业 API 经常使用分页?

- 为什么分页逻辑不应放在 Workflow?

- 为什么 API Client 不应自动获取所有页面?

- 为什么分页属于 Service Layer 的职责?

- 一个业务操作为什么可能对应多个 HTTP Request?

- Workflow 为什么不应感知页码和分页参数? 

## Summary

本节建立了 API 分页处理的工程原则: 

- 将分页视为 API 通信规则, 而不是业务流程. 

- 保持 API Client 一次只发送一个 HTTP 请求. 

- 由 Service 负责循环获取分页数据、合并结果并返回统一的业务对象.
 
- 保持 Workflow 接口简单稳定, 不暴露任何分页细节. 

至此, Chapter 10 不仅覆盖了单次 API 调用, 还覆盖了企业环境中最常见的多请求业务场景, 使整个 Workflow → Service → API Client → HTTP 架构能够自然支持大规模数据获取, 而无需改变上层业务代码. 

# Lab 20 Query Parameters 

到这里, 我们已经能够处理: 

- 单次请求

- 多次请求(Pagination)

- 数据转换

- 错误处理

接下来还有一个企业 API 自动化中非常重要的话题: 

>Filtering(过滤)与 Query Parameters(查询参数)

这是 REST API 中使用频率最高的能力之一. 

## Theory

目前我们的请求都是: `GET /devices` 或者 `GET /posts` 但是实际企业 API 很少这样使用. 

更多情况是: `GET /devices?hostname=R1`

或者: `GET /devices?site=Frankfurt`

又或者: `GET /devices?status=online`

这里 `?hostname=R1` 就是 Query Parameter(查询参数). 

它用于描述如何查询资源, 而不是资源本身. 

## Engineering Discussion

很多初学者喜欢这样写: 

```python
endpoint = (
    "/devices?hostname=R1"
)
```

或者: 

```python
endpoint = (
    f"/devices?hostname={hostname}"
)
```

虽然能够运行, 但是很快就会变成: 

```python
f"/devices?hostname={hostname}&site={site}&status={status}"
```

代码越来越长也越来越难维护. 

### requests 已经提供了解决方案

实际上 `requests` 提供了 `params=`

例如: 

```python
response = session.request(
    method="GET",
    url=url,
    params={
        "hostname": "R1"
    }
)
```

最终 `requests` 自动生成 `GET /devices?hostname=R1`

如果多个参数: 

```python
params={
    "hostname": "R1",
    "status": "online"
}
```

最终生成: `GET /devices?hostname=R1&status=online` 因此不要自己拼接 URL. 

## API Client 是否负责 Query Parameters? 

答案是负责发送, 但是不负责决定参数内容. 

例如: 

```python
API Client: 

def get(endpoint, params=None):

    return _request(
        "GET",
        endpoint,
        params=params
    )
```

这里只是转交: `params=params` API Client 不知道 hostname 是什么意思. 

## Service 的职责

真正决定查询条件的应该是 Service. 

例如: 

```python
def get_devices(hostname=None):

    params = {}

    if hostname is not None:
        params["hostname"] = hostname

    response = api_client.get(
        endpoints.DEVICES,
        params=params
    )

    if response is None:
        return None

    return response.json()
```

现在业务接口变成: 

```python
devices = device_service.get_devices(
    hostname="R1"
)
```

Workflow 不知道 HTTP Query String. 

## Layered Architecture

数据流

```
Workflow

↓

get_devices(hostname="R1")

↓

Service

↓

params={
    "hostname":"R1"
}

↓

API Client

↓

GET /devices?hostname=R1
```

可以看到 Query String 仍然没有进入 Workflow. 

## 为什么不要把 Query String 写进 Workflow? 

例如不要: 

```python
api_client.get(
    "/devices?hostname=R1"
)
```

因为 Workflow 开始理解 HTTP. 

真正希望看到的是: 

```python
device_service.get_devices(
    hostname="R1"
)
```

甚至以后可以继续扩展: 

```python
device_service.get_devices(
    hostname="R1",
    status="online",
    site="Frankfurt"
)
```

Workflow 仍然保持业务语义. 

## Engineering Analysis

这里再次体现了: 

>参数属于业务, 编码属于通信. 

例如: hostname="R1"

这是业务条件, 但是 `?hostname=R1` 这是HTTP 表达方式. 

Service 负责: 业务条件. 

API Client 负责: HTTP 表达. 

两层职责不能混淆. 

## Engineering Best Practice

企业项目建议遵循以下原则: 

- 使用 params 参数传递查询条件, 而不是手工拼接 URL. 

- API Client 负责发送查询参数, 不负责决定查询内容. 

- Service 将业务条件转换为查询参数. 

- Workflow 使用业务接口, 而不是 HTTP Query String. 

- 保持 Query Parameters 与 Endpoint 的职责分离: Endpoint 表示资源, Query Parameters 表示查询方式. 

- Engineering Insight

这一节进一步强化了整个框架的职责划分: 

```
Workflow
    │
    ▼
Business Condition
    │
    ▼
Service
    │
    ▼
Query Parameters
    │
    ▼
API Client
    │
    ▼
HTTP Request
```

从 Workflow 到 HTTP 的过程中, 每一层都完成了一次语义转换: 

- Workflow 表达业务需求. 

- Service 将业务需求转换为查询条件. 

- API Client 将查询条件编码为 HTTP 请求. 

这种分层设计意味着, 即使未来 API 平台将查询方式从 Query Parameters 改为其他机制(例如请求体或特定 SDK 方法), 变化也只会发生在 Service 或 API Client 内部, 而不会影响 Workflow. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- Query Parameters 与 Endpoint 有什么区别? 

- 为什么不建议手工拼接 Query String? 

- requests 中 params 参数的作用是什么? 

- 为什么 API Client 不应决定查询条件? 

- 为什么 Service 应负责构建查询参数? 

- Workflow 为什么不应直接操作 HTTP Query String? 

## Summary

本节建立了 Query Parameters 的工程实践: 

- 将资源路径(Endpoint)与查询条件(Query Parameters)明确区分. 

- 使用 requests 的 params 参数完成 URL 编码, 而不是字符串拼接. 

- 保持 API Client, Service 和 Workflow 的职责边界清晰. 

- 让 Workflow 始终围绕业务条件编写, 而不是围绕 HTTP 请求格式编写. 

至此, Chapter 10 已经覆盖了企业 REST API 自动化中最常见的请求模式: 基础请求, 分页请求以及带查询条件的请求, 为后续接入真实网络平台 API 提供了完整的设计基础. 

# Lab 21 Request Payload Design

到这里, 我们已经讨论了: 

- Endpoint

- Query Parameters

- Pagination

- Response Processing

还有最后一种 REST API 中最常见的数据输入方式没有介绍: 

>Request Payload(请求体)

这是创建(Create)和修改(Update)资源时的核心内容. 

需要注意的是, 本节讨论的重点不是 JSON 语法, 而是请求数据在企业架构中的流转方式. 

## Theory

目前 GET 请求: 

```python
response = api_client.get(
    endpoints.DEVICES
)
```

通常没有 Request Body. 

而 POST `POST /devices` 通常需要: 

```python
{
    "hostname": "R1",
    "managementIp": "10.0.0.1"
}
```

也就是说除了 URL, 客户端还需要把数据发送给服务器. 这部分数据就是 Request Payload. 

## Engineering Discussion

很多初学者会直接这样写: 

```python
payload = {
    "hostname": "R1",
    "managementIp": "10.0.0.1"
}

api_client.post(
    endpoints.DEVICES,
    payload
)
```

虽然能够运行, 但是随着项目越来越大 Workflow 很快会充满: 

```python
{
    ...
}
```

大量 Dictionary, Workflow 开始知道 Vendor API 到底需要哪些字段. 

例如: 

```python
{
    "hostname": "...",
    "managementIp": "...",
    "serialNumber": "...",
    "siteId": "...",
    "locationId": "...",
    ...
}
```

这意味着 Workflow 已经依赖外部 API, 这不是我们希望看到的设计. 

## Payload 应该由谁构造? 

继续按照我们的分层原则, Workflow 负责业务意图. 

例如: 

```python
device = {
    "hostname": "R1",
    "ip": "10.0.0.1"
}
```

这里使用的是内部业务模型. 

Service 负责转换成 API Payload. 

例如: 

```python
payload = {
    "hostname": device["hostname"],
    "managementIp": device["ip"]
}
```

然后: 

```python
response = api_client.post(
    endpoints.DEVICES,
    payload
)
```

API Client 只是发送 Payload, 并不知道这些字段代表什么. 

## Layered Architecture

现在数据流: 

Workflow ➡ Business Object ➡ Service ➡ API Payload ➡ API Client ➡ HTTP Request

注意 Payload 已经属于 HTTP, 不是 Business. 

## Hands-on Lab

例如: 

```python
from modules import api_client
from modules import endpoints


def create_device(device):

    payload = {
        "hostname": device["hostname"],
        "managementIp": device["ip"]
    }

    response = api_client.post(
        endpoints.DEVICES,
        payload
    )

    if response is None:
        return None

    return response.json()
```

Workflow 保持非常简单: 

```python
device = {
    "hostname": "R1",
    "ip": "10.0.0.1"
}

result = device_service.create_device(device)
```

Workflow 完全不知道 Vendor API 真正需要 `managementIp` 这个字段. 

## 为什么不要在 Workflow 构造 Payload? 

假设 Vendor 升级: 

managementIp ➡ managementAddress

如果 Workflow 自己构造 Payload. 整个项目都会修改, 但是如果只有 Service 构造 Payload. 那么修改这一处即可, Workflow 无需任何变化. 

## Payload 与 Business Object 的区别

请注意下面两个对象可能长得很像. 

例如 Workflow: 

```python
{
    "hostname": "R1",
    "ip": "10.0.0.1"
}
```

Service: 

```python
{
    "hostname": "R1",
    "managementIp": "10.0.0.1"
}
```

虽然都是 Dictionary, 但是它们代表完全不同的模型. 

第一个: 属于 Business Object. 

第二个: 属于 Transport Payload. 

不要因为数据结构相同, 就认为它们是同一个对象. 

## Engineering Analysis

这里实际上形成了数据生命周期: 

Business Object ➡ Service Mapping ➡ Request Payload ➡ HTTP ➡ Response Payload ➡ Service Mapping ➡ Business Object

可以发现 Service 既负责向下转换, 也负责向上转换. 因此它成为 Business 和 HTTP 之间唯一的数据转换层. 

## Engineering Best Practice

企业项目通常建议: 

- Workflow 使用业务对象. 

- Service 构造 Request Payload. 

- API Client 负责发送 Payload. 

- 不要在 Workflow 中直接组织厂商 API 所要求的字段. 

- 保持内部数据模型与外部传输模型分离. 

## Engineering Insight

到目前为止, 我们已经建立了两个方向的数据转换, 向服务器发送数据: 

Business Object ➡ API Payload

服务器返回数据: 

API Payload ➡ Business Object

两次转换都发生在 Service Layer. 这意味着 Service 不只是"调用 API". 

更准确地说它是: 

>业务模型(Business Model)与外部 API 模型(External API Model)之间的适配层(Adapter). 

这是很多成熟自动化平台都会采用的设计思想. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- Request Payload 与 Business Object 有什么区别? 

- 为什么 Payload 不应由 Workflow 构造? 

- 为什么 API Client 不应理解 Payload 的业务含义? 

- 为什么 Service 同时负责请求数据和响应数据的转换? 

- 如果厂商修改了 Payload 字段名称, 应该修改哪一层? 

- Service 为什么可以看作 Business Model 与 External API Model 的适配层? 

## Summary

本节建立了 Request Payload 的工程设计原则: 

- 将业务对象与 API 请求体明确区分. 

- 由 Service 完成业务对象到 Request Payload 的映射. 

- 保持 API Client 只负责发送数据, 而不理解业务字段. 

- 形成了完整的数据双向转换机制, 使 Workflow 始终面向稳定的内部业务模型, 而不依赖外部 API 的具体实现. 

至此, Chapter 10 已经完整建立了 REST API 自动化的核心工程体系: 请求发送、响应处理、分页、查询参数、错误处理以及请求/响应数据模型转换. 这套架构将直接作为后续章节接入真实网络控制器 API 的基础. 

# Lab 22 HTTP Method Semantics

到这里, 我们已经建立了完整的数据流: 

```
Business Object
↓
Service Mapping
↓
Request Payload
↓
API Client
↓
HTTP
↓
Response Payload
↓
Service Mapping
↓
Business Object
```

但是还有一个企业 REST API 中经常被忽略, 却非常重要的话题: 

>HTTP Method Semantics(HTTP 方法语义)

这一节不是介绍 GET, POST, PUT, DELETE 的基本用途——这些我们前面已经学习过. 

真正要讨论的是: 

>为什么不同的 HTTP Method 会影响自动化程序的设计? 

## Theory

很多教程都会简单介绍: 

```
GET    Read

POST   Create

PUT    Update

DELETE Delete
```

但是企业自动化真正关心的是**这些操作是否会改变系统状态(System State)**. 

例如: GET /devices 只是读取数据, 服务器的数据不会发生变化. 而 POST /devices 可能创建一台新的设备, 服务器状态发生改变. 

因此 REST API 可以简单分成两类: 

```
Read Operation

Write Operation
```

## Engineering Discussion

### Read Operation

例如 `devices = device_service.get_devices()` 

或者 `interfaces = device_service.get_interfaces()`

这些操作只是读取数据, 不会修改服务器. 

因此即使连续执行: 

```python
device_service.get_devices()

device_service.get_devices()

device_service.get_devices()
```

服务器状态保持一致. 

### Write Operation

例如: `device_service.create_device(device)` 每执行一次服务器可能都会发生变化. 

例如: 第一次 

```
Device Count

100
↓
101
```

第二次: 

```
101
↓
102
```

因此写操作必须更加谨慎. 

## 为什么要区分 Read 与 Write? 

假设下面代码: 

```python
device_service.get_devices()
```

失败. Workflow 完全可以再次执行: 

```python
device_service.get_devices()
```

一般不会造成副作用, 但是如果: 

```python
device_service.create_device(device)
```

第一次实际上已经成功, 只是客户端因为网络超时没有收到响应. 

Workflow 再次执行: 

```python
device_service.create_device(device)
```

服务器可能创建两台设备, 因此读取操作和写入操作在自动化设计中处理策略通常不同. 

## Layered Architecture

Service 开始表达业务动作. 

```
Read Service

GET

────────────────

Write Service
↓
POST

PUT

DELETE
```

Workflow 不用知道 HTTP Method, 但是 Service 应该知道这是读取, 还是修改. 

## Hands-on Lab

例如: 

```python
def get_devices():

    response = api_client.get(
        endpoints.DEVICES
    )

    ...
```

属于 Read Service 而: 

```python
def create_device(device):

    payload = ...

    response = api_client.post(
        endpoints.DEVICES,
        payload
    )

    ...
```

属于 Write Service, 两者接口设计可以类似, 但是工程意义不同. 

## Retry Strategy

很多企业项目都会建立不同的 Retry Policy. 

例如: 

```
Read Request
↓
允许自动 Retry

────────────────

Write Request
↓
谨慎 Retry
```

原因很简单 GET 重新执行通常不会修改服务器. POST 重新执行可能产生重复资源. 

因此不要把所有 HTTP Method 都当成完全一样. 

## Engineering Analysis

这里体现了: 

>业务语义比 HTTP 语法更重要. 

对于 API Client 来说只是: 

```python
_request(
    method,
    endpoint
)
```

但是对于 Service 来说. 这是 Read 还是 Write 这种区别. 

会影响: 

- Retry Strategy

- Error Handling

- Workflow Decision

因此真正理解 HTTP Method 的语义, 比记住 Method 的名称更重要. 

## Engineering Best Practice

企业自动化项目通常遵循以下原则: 

- 将读取操作与写入操作在设计上明确区分. 

- 对读取操作可以采用更积极的重试策略. 

- 对写入操作应避免未经确认的重复执行. 

- 在 Service 层表达业务动作, 而不是直接暴露 HTTP Method. 

- Workflow 关注"我要读取什么"或"我要修改什么", 而不是"我要发送 GET 还是 POST". 

## Engineering Insight

这一节实际上为后续章节埋下了一个重要基础. 

目前我们已经知道: 

Business Action ➡ Service ➡ HTTP Method

但随着自动化平台越来越复杂, 我们会发现: 

并不是所有"修改"操作都可以安全地重复执行, 也不是所有"读取"操作都完全没有副作用. 

因此, 在设计 Service 接口时, 不仅要考虑功能, 还要考虑操作语义. 

成熟的自动化框架通常都会把"读取"和"修改"视为两类不同的业务能力, 并围绕它们制定不同的错误处理, 日志记录和执行策略. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么要区分 Read Operation 与 Write Operation? 

- 为什么 GET 通常比 POST 更适合自动重试? 

- 为什么 Workflow 不应直接关注 HTTP Method? 

- Service 为什么需要理解操作的业务语义? 

- HTTP Method 的语义如何影响错误处理和重试策略? 

- 为什么"业务动作"比"HTTP 方法"更适合作为接口设计基础? 

## Summary

本节从工程设计角度重新理解了 HTTP Method: 

- 将 API 操作划分为读取(Read)和写入(Write)两类业务行为. 

- 强调 HTTP Method 的语义会影响自动化框架的重试策略和错误处理. 

- 保持 Workflow 面向业务动作, Service 面向业务语义, API Client 面向 HTTP 通信. 

# Lab 23 API Workflow Design

这一节不是新增知识, 而是把前面所有零散的内容整合成一套完整的企业工作流。这也是一本工程教材中非常重要的一节。

## Theory

到目前为止, 我们已经分别学习了: 

- Workflow

- Service

- API Client

- HTTP

- Request Payload

- Response Processing

- Business Object

这些内容都是独立介绍的, 但是, 一个真正的企业自动化程序, 并不是这些模块的简单堆叠, 而是它们按照固定的数据流协同工作。

因此, 本节的目标是: 

>建立完整的 API Automation Workflow。

## Engineering Discussion

假设 Workflow 希望获取所有设备 Workflow 并不会直接发送 HTTP Request。

整个执行流程实际上是: 

Workflow ➡ device_service.get_devices() ➡ api_client.get() ➡ _request() ➡ Session ➡ HTTP Server

服务器返回: `HTTP Response`

然后又会沿着相反方向返回。

## 完整数据流

整个流程如下: 

```
Workflow
        │
        ▼
Business Service
        │
        ▼
Endpoint Selection
        │
        ▼
API Client
        │
        ▼
Build Headers
        │
        ▼
Authentication
        │
        ▼
Shared Session
        │
        ▼
HTTP Request
        │
        ▼
REST API Server
        │
        ▼
HTTP Response
        │
        ▼
Status Validation
        │
        ▼
Response Object
        │
        ▼
JSON Parsing
        │
        ▼
Business Mapping
        │
        ▼
Business Object
        │
        ▼
Workflow
```

请注意 Workflow 最终拿到的是 Business Object。

它永远不会直接接触: 

- HTTP Header

- Status Code

- Authentication

- Endpoint

- Payload Format

## 数据生命周期

如果只关注数据整个生命周期是: 

Business Object ➡ Service ➡ Request Payload ➡ HTTP ➡ Response Payload ➡ Service ➡ Business Object

这里可以发现 Service 负责两次转换。

第一次: Business ➡ Transport

第二次: Transport ➡ Business

因此 Service 实际上就是: **数据适配层(Data Adapter)**。

## 通信生命周期

如果只关注通信, 生命周期则是: 

Workflow ➡ Service ➡ API Client ➡ Request Engine ➡ HTTP ➡ API Server ➡ HTTP ➡ Request Engine ➡ Service ➡ Workflow

这里 API Client 始终负责整个通信生命周期。

包括: 

- Session

- Authentication

- Timeout

- Logging

- Status Validation

- Exception Handling

Service 完全不需要了解这些内容。

## Layer Responsibility Review

到目前为止整个系统已经形成稳定的职责划分。

### Workflow

负责: 

- 调度业务流程

- 控制执行顺序

- 输出最终结果

不负责: 

- HTTP

- JSON

- Authentication

- Payload

### Service

负责: 

- 业务接口

- Endpoint 选择

- Query Parameters

- Pagination

- Payload Mapping

- Response Mapping

不负责: 

- Session

- Logging

- Timeout

- HTTP

### API Client

负责: 

- HTTP Communication

- Authentication

- Headers

- Timeout

- Session

- Logging

- Exception

- Status Validation

不负责: 

- Devices

- Users

- Inventory

- Compliance

### HTTP Server

负责: 

- 提供资源

- 返回数据

- 执行业务

属于外部系统。

## Engineering Analysis

请回顾 Chapter 8 和 Chapter 9 我们一直坚持一个设计原则, 每一层都应该隐藏自己的实现细节, 只向上一层暴露稳定接口。

在 Chapter 10 中, 这一原则同样成立: 

- Workflow 不知道 HTTP。

- Service 不知道 Session。

- API Client 不知道业务对象。

- HTTP Server 不知道我们的内部实现。

这种层层封装, 使每个模块都可以独立修改, 而不会影响整个系统。

## Engineering Best Practice

成熟的 API Automation Framework 通常具有以下特征: 

- Workflow 只调用业务接口。

- Service 层隔离业务模型与外部 API 模型。

- API Client 统一管理所有 HTTP 通信能力。

- Configuration、Endpoints 和 Authentication 集中管理。

- 每一层都通过稳定接口与下一层交互, 而不是依赖实现细节。

## Engineering Insight

到这里, 我们已经完成了整个 Workbook 中第二套完整的工程框架。

回顾前面的章节 Chapter 8 建立了: 

```
Workflow
    │
    ▼
Renderer
    │
    ▼
Deployment
    │
    ▼
Netmiko
```

Chapter 9 建立了: 

```
Workflow
    │
    ▼
Compliance
    │
    ▼
Connection
```

Chapter 10 则建立了: 

```
Workflow
    │
    ▼
Business Service
    │
    ▼
API Client
    │
    ▼
HTTP
```

虽然底层通信方式不同, 但三章遵循的是同一种工程思想 Workflow 面向业务, 通信模块面向协议, 中间层负责隔离两者。

这也是整个 Workbook 希望建立的统一架构理念。

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 一个完整的 API Automation Workflow 包含哪些阶段? 

- Service 在数据流中承担了哪两次转换? 

- API Client 在通信生命周期中承担哪些职责? 

- 为什么 Workflow 不应接触 HTTP Response? 

- Chapter 10 的分层设计与 Chapter 8、Chapter 9 有哪些共同点? 

- 什么叫"每一层隐藏自己的实现细节"? 

## Summary

本节将 Chapter 10 的各个知识点整合为一套完整的 API Automation Workflow: 

从业务请求到 HTTP 通信, 再到响应处理, 建立了完整的数据流和通信流。
明确了 Workflow、Service、API Client 和 HTTP Server 的职责边界。
强调了分层架构、稳定接口和数据模型隔离等核心工程原则。

至此, Chapter 10 的核心框架已经完整建立。后续的收尾部分将对模块依赖、项目目录结构和整体架构进行最终回顾, 为进入下一章的真实 REST API 自动化实践做好准备。

# Lab 24 Module Dependency Review

本节不再增加新的 REST API 知识，而是对整个项目进行一次架构审查(Architecture Review). 

这是企业开发中非常重要但很多教材都会忽略的一部分. 

## Theory

随着 Chapter 10 的完成，我们已经创建了多个模块: 

```
scripts/

modules/
    api_client.py
    device_service.py
    endpoints.py
    loader.py
    logger.py
```

这些模块已经可以工作, 但是还有一个问题: 

>它们之间是否形成了合理的依赖关系(Dependency)? 

对于一个小项目来说，错误的依赖关系可能暂时没有影响, 但随着项目规模扩大，不合理的依赖会导致模块耦合、循环引用和维护困难. 

因此，企业项目通常会对模块依赖方向进行明确约束. 

## Engineering Discussion

### 当前依赖关系

按照目前的设计: 

```
scripts
    │
    ▼
device_service
    │
    ├─────────────┐
    ▼             ▼
api_client    endpoints
    │
    ├─────────────┐
    ▼             ▼
loader       logger
    │
    ▼
requests
```

请注意依赖方向始终向下, 没有任何模块回头依赖上层. 

### 为什么不能反向依赖? 

例如下面这种代码: 

```python
# api_client.py

from modules import device_service
```

就是错误设计, 为什么? 

因为: device_service ➡ api_client 已经存在. 

现在又出现: api_client ➡ device_service

于是形成: device_service ↔ api_client

也就是 Circular Dependency(循环依赖)

## 循环依赖的问题

循环依赖不仅容易导致 `ImportError` 更严重的是职责开始混乱. 

例如: API Client 开始知道 Devices 那么以后 API Client 是不是还要知道 

```
Users

Interfaces

Routes

Compliance
```

最终 API Client 就变成一个巨大模块, 违反 **Single Responsibility Principle**. 

## Layer Dependency Rule

整个项目遵循下面的依赖规则: 

Workflow ➡ Service ➡ API Client ➡ Utility Modules ➡ Third-party Libraries

依赖只能向下, 不能向上. 

## Utility Modules

例如: 

```
loader.py

logger.py
```

属于 Utility 它们可以被 Service, API Client 共同使用, 但是 Utility 绝不能反向导入: 

```python
from modules import api_client
```

否则 Utility 开始依赖 Business 职责立即混乱. 

## Hands-on Lab

下面属于正确依赖: 

```python
# device_service.py

from modules import api_client
from modules import endpoints
```

API Client: 

```python
from modules import loader
from modules import logger
```

Logger: 

```python
import logging
```

这里 Logger 不知道 Device 也不知道 HTTP. 

错误示例: 

```python
# logger.py

from modules import device_service
```

或者: 

```python
# loader.py

from modules import api_client
```

这种设计都应避免. 

## Dependency Pyramid

整个项目形成依赖金字塔: 

```
               Workflow
                  │
                  ▼
            Business Service
             ┌──────────┐
             ▼          ▼
       API Client   Endpoints
             │
      ┌──────┴──────┐
      ▼             ▼
   Loader        Logger
      │
      ▼
 Third-party Libraries
```

越靠近底层模块越通用, 越靠近上层模块越接近业务. 

## Engineering Analysis

请注意这里讨论的是依赖方向. 不是调用方向. 

例如: Workflow 调用 Service, 但是 Logger 也可能记录 Workflow. 

这并不意味着 Logger 应该 Import Workflow 调用关系和模块依赖, 是两件不同的事情, 很多初学者容易混淆. 

## Engineering Best Practice

成熟的自动化项目通常遵循以下依赖原则: 

- 上层模块可以依赖下层模块. 

- 下层模块不要依赖上层模块. 

- Utility Module 保持通用，不依赖业务模块. 

- 避免循环依赖(Circular Dependency). 

- 模块依赖方向应长期保持稳定. 

这样可以保证模块可测试、可复用，并降低后续重构成本. 

## Engineering Insight

回顾整个 Workbook. 

Chapter 8: 

Workflow ➡ Renderer ➡ Deployment

Chapter 9: 

Workflow ➡ Compliance ➡ Connection

Chapter 10: 

Workflow ➡ Service ➡ API Client ➡ Utility

虽然模块名称不同, 但依赖规则完全一致业务能力依赖基础能力，基础能力绝不依赖业务能力. 这也是整个 Workbook 一直坚持的架构原则. 

未来无论增加新的 Service、API Client 或 Utility，都应遵循这一依赖方向，而不是因为功能方便而打破分层. 

## Engineering Checklist

完成本节后，应能够回答以下问题: 

- 什么是模块依赖关系? 

- 为什么依赖方向只能向下? 

- 什么是循环依赖? 为什么要避免? 

- Utility Module 为什么不能依赖业务模块? 

- 调用关系与依赖关系有什么区别? 

- Chapter 8、9、10 在模块依赖设计上有哪些共同原则? 

## Summary

本节对 Chapter 10 的模块结构进行了工程审查: 

- 建立了自上而下的模块依赖规则. 

- 明确了 Workflow、Service、API Client 与 Utility 的职责边界. 

- 强调避免循环依赖和反向依赖，保持基础模块的通用性. 

至此，Chapter 10 不仅建立了 API Automation 的功能架构，也建立了项目的依赖架构(Dependency Architecture). 这使整个自动化框架在继续扩展时仍然能够保持清晰、稳定和易于维护. 

# Lab 25 Project Structure Review

现在可以进入 Chapter 10 的最后一个工程性章节. 

前面我们已经审查了: 

- 数据流

- 通信流

- 模块职责

- 模块依赖

最后还需要回答一个问题: 

>整个项目最终应该长什么样? 

很多教程讲完 API 就结束了. 

但是企业项目真正重要的是: 

>代码应该如何组织(Project Organization). 

## Theory

随着 Chapter 10 完成, 我们的自动化框架已经包含多个模块. 

如果没有统一的目录结构, 项目很快就会出现: 

```
api.py

api2.py

new_api.py

device.py

device_new.py

test.py

test2.py
```

这样的文件命名虽然能够工作, 但是随着项目扩大维护成本会迅速增加, 因此企业项目通常会先设计目录, 再增加功能. 

## Engineering Discussion

结合前面 Chapters. 

目前整个项目可以整理为: 

```
automation_project/

├── config/
│   ├── api.yaml
│   └── variables.yaml
│
├── inventory/
│   ├── devices.yaml
│   ├── R1.yaml
│   ├── R2.yaml
│   └── R3.yaml
│
├── templates/
│   ├── base.j2
│   └── main.j2
│
├── output/
│
├── logs/
│
├── modules/
│   ├── api_client.py
│   ├── device_service.py
│   ├── endpoints.py
│   ├── connection.py
│   ├── deployment.py
│   ├── renderer.py
│   ├── validator.py
│   ├── inventory.py
│   ├── loader.py
│   └── logger.py
│
└── scripts/
    ├── deploy.py
    ├── compliance.py
    └── get_devices.py
```

请注意整个目录并不是按照协议分类, 而是按照职责(Responsibility)进行分类. 

## 为什么不建立 api 文件夹? 

很多初学者喜欢: 

```
modules/

    api/

        client.py

        service.py

        endpoints.py
```

这种设计在大型项目当然可以, 但是目前我们的 Workbook 规模仍然较小再增加一级目录收益并不明显. 

因此保持: 

```
modules/

    api_client.py

    device_service.py

    endpoints.py
```

更加简单, 如果未来 Service 增加到二三十个再拆分目录也不迟. 

## Script 的定位

请注意 `scripts/` 始终都是入口. 

例如: 

```
deploy.py

compliance.py

get_devices.py
```

它们负责启动一个完整 Workflow, 而不是保存公共逻辑. 

因此不要在 `scripts/` 

下面建立: 

```
utils.py

helper.py
```

公共能力应该放入 `modules/` 保持 Scripts 很薄, Modules 很稳定.

## Config 的定位

前面章节我们已经建立 `config/` 

现在里面可以包含: 

```
api.yaml

variables.yaml
```

以后如果继续扩展, 例如: 

```
logging.yaml

credentials.yaml
```

仍然属于 Configuration, 不要把配置分散到多个模块里面. 

## Modules 的定位

整个项目真正的核心就是 `modules/` 这里保存所有可以复用的能力. 

例如: 

```
Renderer

Validator

Connection

API Client

Service
```

Workflow 永远调用 Modules. Modules 彼此按照依赖规则协作. 

## Layer Review

现在整个工程已经形成完整分层. 

Scripts ➡ Business Modules ➡ Communication Modules ➡ Utility Modules ➡ Third-party Libraries

其中 Business Modules

例如 `device_service.py`

Communication Modules

例如: 

```
api_client.py

connection.py
```

Utility: 

例如: 

```
loader.py

logger.py
```

可以发现 Chapter 8 SSH, Chapter 10 HTTP 虽然协议不同, 最终组织方式完全一致. 

## Engineering Analysis

这一节没有新增任何 Python 语法. 

真正完成的是: 

>工程标准化(Engineering Standardization). 

以后每新增一个模块我们首先要问: 它属于哪一层? 而不是应该放哪个文件夹. 

当职责确定之后目录位置自然就确定了, 这比根据功能名称随意建立文件夹更加稳定. 

## Engineering Best Practice

企业项目通常建议: 

- 按职责组织目录，而不是按协议或临时需求组织. 

- Scripts 保持精简，只负责启动 Workflow. 

- Modules 保存所有可复用逻辑. 

- Config 集中保存配置. 

- Output、Logs、Templates、Inventory 等目录保持单一职责，不混合存放其他内容. 

这样可以让项目随着规模增长仍保持清晰的结构. 

## Engineering Insight

回顾整个 Workbook, Chapter 3 学习了: 如何连接设备. 

Chapter 8 学习了: 如何组织自动化项目. 

Chapter 10 学习了: 如何组织 API 自动化项目. 

虽然通信协议已经从 SSH 转换为 HTTP, 但是项目结构几乎没有变化. 这正说明好的工程架构应该独立于底层技术. 协议可以变化, 平台可以变化甚至厂商也可以变化, 但目录结构、模块职责和依赖方向依然保持稳定, 这正是企业软件长期可维护的重要原因. 

## Engineering Checklist

完成本节后，应能够回答以下问题: 

- 为什么项目应按职责组织，而不是按协议组织? 

- scripts/ 与 modules/ 的职责有什么区别? 

- 为什么配置应集中在 config/? 

- 为什么 modules/ 是整个项目的核心? 

- 当新增模块时，应先考虑什么问题? 

- 为什么 Chapter 8 和 Chapter 10 的项目结构几乎一致? 

## Summary

本节对整个 API Automation 项目进行了结构整理: 

- 明确了各目录的职责和边界. 

- 建立了统一的项目组织规范. 

- 将 SSH 自动化与 API 自动化统一到同一套工程结构中. 

至此，Chapter 10 已经完成了从 HTTP 基础 到 企业级 API Automation Framework 的全部架构设计. 下一节将作为本章的最终总结，对整个 Chapter 10 的设计理念、工程原则和核心知识进行全面回顾，为进入 Chapter 11 做准备.