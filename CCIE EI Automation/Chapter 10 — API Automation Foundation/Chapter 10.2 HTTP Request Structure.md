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