## Theory

HTTP 本身是一种通信协议. 

协议负责: Client ➡ Server 之间的数据传输. 

至于客户端是否有权限访问服务器这并不是 HTTP Protocol 自己决定的. 

因此各种 API 平台都会建立自己的 Authentication Mechanism(认证机制). 

例如: 

HTTP ➡ Authentication ➡ Business API

也就是说 HTTP 提供通信能力, Authentication 提供身份验证能力. 两者虽然一起工作, 但职责不同. 

## Engineering Discussion

### Authentication 属于 Business Logic 吗? 

假设 Business Logic: `devices = api_client.get("/devices")`

如果业务代码需要写: 

```python
headers = {
    "Authorization": "Bearer xxxxxxxxx"
}
```

然后: 

```python
requests.get(
    url,
    headers=headers
)
```

那么 Authentication 就开始散落到整个项目. 

例如: 

```
Inventory
↓
Authorization

────────────────

Compliance
↓
Authorization

────────────────

Monitoring
↓
Authorization
```

以后 Token 更新, Header 修改所有模块都要修改. 

这显然违反了  Single Responsibility Principle. 

## Authentication 属于哪一层? 

回顾目前架构: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
Session
        │
        ▼
HTTP
```

Authentication 本质上属于 Communication Strategy. 

因为它影响每一次 HTTP Request. 

因此应该放入 API Client, 而不是 Business Logic. 

## Layered Architecture

加入认证以后: 

```
Business Logic
        │
        ▼
API Client
        │
        ├── Session
        ├── Authentication
        ├── Timeout
        ├── Logging
        └── Request Engine
```

Business Logic 永远不知道 Header 如何构造, 也不知道 Token 放在哪里. 

## Authentication 与 Header 的关系

前面章节已经学习过 HTTP Header 保存的是通信元数据(Metadata).  Authentication 也是 Header 的一部分. 

例如: `Authorization: Bearer xxxxxxxxx`

或者: `Authorization: Basic xxxxxxxxx`

因此认证实际上只是 API Client 构造 Header 时增加的一项内容. 它并不会改变 Business Logic. 

## Hands-on Lab

首先修改配置文件. 

```yaml
timeout: 10

verify_ssl: true

base_url: https://jsonplaceholder.typicode.com

authentication:
  enabled: false
  type: bearer
  token: ""
```

注意目前即使测试 API 并不需要认证, 我们仍然建立配置结构. 这是为了工程一致性. 

## API Client 初始化

读取配置: 

```python
AUTH_ENABLED = config["authentication"]["enabled"]
AUTH_TYPE = config["authentication"]["type"]
AUTH_TOKEN = config["authentication"]["token"]
```

目前不要立即实现各种认证方式. 先建立配置入口. 

## Header Construction

新增内部函数: 

```python
def _build_headers():
    """
    Build default HTTP headers.
    """

    headers = {}

    if AUTH_ENABLED:

        if AUTH_TYPE == "bearer":

            headers["Authorization"] = (
                f"Bearer {AUTH_TOKEN}"
            )

    return headers
```

这里要注意 Business Logic 完全不知道 Header. 所有 Header 全部由 API Client 负责生成. 

## 修改 Request Engine

现在: 

```python
response = session.request(
    method=method,
    url=url,
    timeout=DEFAULT_TIMEOUT,
    verify=VERIFY_SSL,
    headers=_build_headers(),
    **kwargs
)
```

整个 Authentication 已经加入 Request Engine. 

GET, POST 无需任何修改. 

## Workflow 的变化

整个请求生命周期进一步完善. 

```
Business Logic
        │
        ▼
_request()
        │
        ├── Build Headers
        ├── Authentication
        ├── Logging
        ├── Timeout
        ├── Send Request
        ├── Exception Handling
        ├── Status Validation
        └── Return Response
```

可以看到 Authentication 只是 Request Engine 中的一个步骤. 而不是新的 Workflow. 

## 为什么先支持一种认证方式? 

目前我们只保留 Bearer 配置. 原因不是 Bearer 最重要, 而是我们要先建立 Authentication Framework. 

以后如果增加:

```
Basic

API Key

Custom Header
```

甚至 Vendor Authentication, 都只是扩展 `_build_headers()` 而不是修改整个 API Client. 

## Engineering Analysis

这里体现了一个重要的工程原则: 

>新增能力，应尽量扩展已有模块，而不是改变已有接口. 

注意 Business Logic 仍然调用 `api_client.get("/devices")` 

接口完全没有变化. 

Authentication 是在 API Client 内部增加的能力. 因此整个项目没有任何业务代码需要修改. 

这正是稳定接口(Stable Interface)带来的价值. 

## Engineering Best Practice

企业项目中，建议遵循以下原则: 

- 所有认证信息集中在配置中管理. 

- 所有认证 Header 由 API Client 统一生成. 

- Business Logic 永远不要直接拼接 Authorization Header. 

- 新增认证方式时，只扩展 Header 构建逻辑，不修改公共接口. 

这样既保证了安全性，也降低了后续维护成本. 

## Engineering Insight

请注意这一节真正建立的并不是 Bearer Token, 而是 Authentication Pipeline(认证流程). 

以后无论接入哪个厂商平台. 

例如: 

```
Cisco

Juniper

Arista

Palo Alto
```

Business Logic 都不会知道认证如何完成. 

它只负责调用: `api_client.get(...)` 认证机制. 

作为 Connection Layer 的一部分统一管理. 这与 SSH Automation 中 Connection Module 负责建立 SSH 登录, Business Logic 只负责发送命令本质上完全一致. 

## Engineering Checklist

完成本节后，应能够回答以下问题: 

- 为什么 Authentication 应属于 API Client，而不是 Business Logic? 

- Authentication 与 HTTP Header 有什么关系? 

- 为什么 Header 应由 _build_headers() 统一生成? 

- 为什么认证信息应放入配置文件? 

- 为什么新增认证方式不应修改 get()、post() 的接口? 

- 本节建立的是一种认证方式，还是整个认证框架? 

## Summary

本节为 `api_client.py` 引入了统一的认证框架: 

- 将认证配置纳入 YAML 配置管理. 

- 使用 _build_headers() 统一构造认证 Header. 

- 将认证流程集成到 _request() 中，而不改变公开接口. 

- 保持 Business Logic 与认证机制完全解耦. 

至此，`api_client.py` 已经形成了一个完整的企业级通信模块: 配置管理、共享 Session、统一请求引擎、日志、超时、异常处理、状态码验证以及认证管理. 后续学习具体 API 平台时，我们将直接复用这一框架，而无需重新设计通信层. 