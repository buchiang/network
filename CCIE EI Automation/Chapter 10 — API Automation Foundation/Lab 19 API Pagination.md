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