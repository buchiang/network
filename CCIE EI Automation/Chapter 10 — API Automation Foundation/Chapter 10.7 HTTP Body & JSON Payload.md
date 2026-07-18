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