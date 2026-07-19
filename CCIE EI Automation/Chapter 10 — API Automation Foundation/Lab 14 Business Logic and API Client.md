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