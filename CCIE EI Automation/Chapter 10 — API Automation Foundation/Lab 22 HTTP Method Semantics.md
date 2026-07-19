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