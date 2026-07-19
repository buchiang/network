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