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