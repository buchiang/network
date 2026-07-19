到这里, Chapter 10 已经建立了完整的 API Automation 架构, 但是还有一个企业项目中一定会遇到的问题没有讨论：

如何组织 API Endpoint? 

目前我们的代码仍然存在这种写法：

`response = api_client.get("/devices")`

或者：

`response = api_client.get("/interfaces")`

实验没有问题, 但是企业项目里, 一个平台往往有几百个 API Endpoint. 

如果整个项目到处都是：

```
"/devices"

"/interfaces"

"/vlans"

"/routes"

"/users"

"/sites"
```

维护会越来越困难. 

因此, 这一节讨论：Endpoint Management(Endpoint 管理)

## Theory

Endpoint 本质上也是一种数据. 

例如：

```
/devices

/interfaces

/vlans
```

这些都不是程序逻辑, 而是服务器提供的资源路径. 因此Endpoint 不应该散落在整个项目. 

## Engineering Discussion

假设：服务器升级. 

原来：`/devices`

改成：`/network/devices`

如果整个项目有30个地方写着 `"/devices"` 那么需要修改30次. 很明显这违反了 DRY Principle. 

## 集中管理 Endpoint

企业项目通常会建立统一Endpoint 定义. 

例如：

```
modules/

    endpoints.py
```

里面：

```
DEVICES = "/devices"

INTERFACES = "/interfaces"

VLANS = "/vlans"
```

以后 Service 不再写 `api_client.get("/devices")` 

而是 

```
from modules import endpoints

response = api_client.get(
    endpoints.DEVICES
)
```

## 为什么不是写在 api_client.py? 

很多初学者会写：

```python
class APIClient:

    DEVICES = "/devices"
```

这样设计的问题是 API Client 负责 HTTP. 

Endpoint 属于业务资源, 它们不是同一层. 

因此 Endpoint 应该属于 Service Domain, 而不是 Communication Layer. 

## Layered Architecture

现在架构进一步清晰：

```
Workflow
      │
      ▼
Device Service
      │
      ├── Endpoints
      ▼
API Client
      ▼
HTTP
```

API Client 甚至不知道什么叫 Devices. 它只知道收到一个字符串. 

## Hands-on Lab

建立：

```
modules/

    endpoints.py
```

内容：

```python
"""
REST API endpoints.
"""

POSTS = "/posts"

COMMENTS = "/comments"

USERS = "/users"
```

修改 Service：

```python
from modules import api_client
from modules import endpoints


def get_posts():

    response = api_client.get(
        endpoints.POSTS
    )

    if response is None:
        return None

    return response.json()
```

Business Logic 没有任何变化. 

## 为什么使用常量? 

不要 `posts = "/posts"` 

建议全部使用大写. 

```
POSTS

DEVICES

USERS
```

因为它们表示不会在运行过程中改变. 属于模块常量(Module Constants), 这样阅读代码时, 也更容易识别哪些值是固定定义. 

## Endpoint 与 Base URL

还记得前面配置中的：

```yaml
base_url: https://jsonplaceholder.typicode.com
```

现在 API Client 负责：

Base URL + Endpoint

例如：

```
https://jsonplaceholder.typicode.com

+

/posts
```

最终得到：`https://jsonplaceholder.typicode.com/posts`

因此 Service 永远不要自己拼接 `BASE_URL + "/posts"` URL 的组合属于 API Client 的职责. 

## Engineering Analysis

这里再次体现了**变化集中管理**. 

如果：API Server 升级：

/posts ➡ /api/v2/posts

只需要修改：`POSTS = "/api/v2/posts"`

所有 Service 自动完成升级. 这比文搜索 `"/posts"` 更加安全. 

## Engineering Best Practice

成熟的自动化项目通常会：

- 将所有 Endpoint 集中定义. 

- 使用有意义的常量名称. 

- 避免在业务代码中直接书写资源路径. 

- 由 API Client 负责拼接 Base URL 与 Endpoint. 

- Service 只引用 Endpoint 常量, 不处理 URL 细节. 

## Engineering Insight

这一节看起来只是把字符串移动到了另一个文件. 

实际上, 它进一步强化了整个系统的分层：

- Configuration 管理运行参数(Timeout, Base URL, SSL 等). 

- Endpoints 管理资源路径. 

- API Client 管理 HTTP 通信. 

- Service 管理业务语义. 

- Workflow 管理业务流程. 

每一种信息都有唯一的归属位置. 

随着项目规模扩大, 这种"每类信息集中管理"的方式, 会极大降低维护成本和修改风险. 

## Engineering Checklist

完成本节后, 应能够回答以下问题：

- 为什么 Endpoint 不应散落在各个 Service 中? 

- 为什么 Endpoint 应集中定义? 

- 为什么 Endpoint 不属于 API Client? 

- 为什么推荐使用模块常量表示 Endpoint? 

- Base URL 与 Endpoint 分别由哪一层负责? 

- Endpoint 集中管理体现了哪些工程原则? 

## Summary

本节建立了统一的 Endpoint 管理机制：

- 将所有资源路径集中到 endpoints.py. 

- 使用模块常量统一维护 Endpoint. 

- 保持 API Client 专注于 HTTP 通信, Service 专注于业务逻辑. 

- 由 API Client 统一拼接 Base URL 与 Endpoint, 避免 URL 拼接逻辑分散在业务代码中. 