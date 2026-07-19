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