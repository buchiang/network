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