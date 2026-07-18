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