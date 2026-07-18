这里进入 Session(会话管理). 这是 Chapter 10 中第一个真正体现企业级 HTTP Client 与"教程代码"差异的主题. 

很多入门教程一直使用: 

```python
requests.get(...)
requests.post(...)
```

实际上, 这只是 `requests` 提供的便捷函数. 企业项目几乎都会进一步封装 `requests.Session()`

不过, 这一节我们仍然保持 Vendor Neutral, 不涉及任何具体网络控制器. 

## Theory

到目前为止, 我们一直使用 `requests.get(...)` 或者 `requests.post(...)` 它们都能够正常工作, 但是每一次调用: 

Business Logic ➡ API Client ➡ requests.get() ➡ HTTP Request

都是一次独立的 HTTP 请求, 对于偶尔发送一两个请求来说, 这没有问题, 但是企业自动化平台通常会连续发送: 

- 获取设备列表

- 获取接口信息

- 获取 VLAN

- 获取 ACL

- 获取 Routing Table

可能在几秒钟内发送几十甚至几百个请求. 因此我们需要考虑: 

>这些请求之间能否共享一些通信资源? 

## Engineering Discussion

### 什么是 Session? 

可以把 Session 理解为: 

>客户端与服务器之间的一次持续通信上下文(Communication Context). 

注意这里说的 Session 不是用户登录, 也不是 Authentication 这是两个不同概念, 目前我们只讨论 HTTP Client. 

例如没有 Session: 

```
GET /devices
↓
建立连接
↓
发送请求
↓
关闭连接

──────────────────

GET /interfaces
↓
建立连接
↓
发送请求
↓
关闭连接
```

每一次都是独立流程. 

如果使用 Session: 

```
Session
      │
      ▼
GET /devices
      │
      ▼
GET /interfaces
      │
      ▼
GET /vlans
      │
      ▼
关闭 Session
```

整个过程中一些底层资源可以复用. 

## 为什么企业项目喜欢 Session? 

主要原因有三个. 

第一, 统一管理请求. 

例如: 所有请求都来自同一个 Session, 而不是到处调用: 

```python
requests.get()

requests.post()
```

第二, 共享通信配置. 

例如: 以后如果 Session 已经配置: 

- Header

- Timeout

- Cookie

那么每一次请求都无需重新设置. 

第三, 减少重复建立连接. 虽然底层实现细节超出了本章范围, 但是可以理解为 Session 能够减少重复初始化通信资源. 对于自动化平台尤其重要. 

## Layered Architecture

引入 Session 后通信层变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
HTTP Session
        │
        ▼
HTTP Request
```

注意 Business Logic 仍然不知道 Session. 所有管理全部属于 Connection Layer. 

## Hands-on Lab

首先创建统一 Session. 

```python
import requests

session = requests.Session()
```

随后修改 GET. 

```python
response = session.get(
    url,
    timeout=DEFAULT_TIMEOUT
)
```

POST 修改: 

```python
response = session.post(
    url,
    json=payload,
    timeout=DEFAULT_TIMEOUT
)
```

其他代码完全不用修改. 

## 为什么放在模块顶部? 

很多人会写: 

```python
def get(url):

    session = requests.Session()

    response = session.get(...)
```

这样实际上失去了 Session 存在的意义. 因为每一次调用都会创建新的 Session, 应该整个 API Client 共享一个 Session. 

例如 `session = requests.Session()`

位于模块顶部, 这样所有 GET, POST, PUT, PATCH, DELETE 都使用同一个 Session. 

## Workflow 的变化

现在一次请求变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
Shared Session
        │
        ▼
HTTP Request
```

Business Logic 仍然只有一句 `response = api_client.get(url)` 整个 Session 生命周期已经隐藏. 

## Engineering Analysis

目前 API Client 已经开始拥有自己的状态(State), 以前它只是一些函数. 现在它拥有 Shared Session 虽然目前 Session 里面几乎没有任何配置, 但是后面 Authentication, Cookie, Header 都会放入 Session. 因此这一节实际上是在为后续内容搭建基础设施. 

## 为什么现在不介绍 Cookie? 

很多 HTTP 教程, 介绍 Session 马上开始讲 Cookie, Login, Authentication 本 Workbook暂时不这样安排. 

原因是目前 Session 首先是通信管理工具. 

Authentication 只是后续利用 Session 实现的一项能力. 

按照课程路线先理解 Session. 再理解 Authentication, 学习节奏更加清晰. 

## Engineering Best Practice

企业项目中, 一个 API Client 通常遵循以下原则: 

- 在模块初始化时创建一个共享 Session. 

- 所有 HTTP 请求都通过该 Session 发起. 

- 不在每次请求时重复创建 Session. 

- 将 Session 作为 Connection Layer 的一部分, 而不是暴露给 Business Logic. 

这样做既提高了代码一致性, 也为后续统一管理认证信息, 公共 Header 和连接策略提供了基础. 

## Engineering Insight

这一节最大的变化并不是 `requests.get(...)` 变成了 `session.get(...)` 真正重要的是 API Client 从"一组工具函数"演变成了"一个拥有通信上下文的模块". 

这意味着 HTTP 通信已经开始具有生命周期: 

Create Session ➡ Multiple Requests ➡ Close Session

这种生命周期管理思想, 与我们在 SSH 自动化中管理连接对象的思路是一致的. 

虽然底层协议不同, 但在 Enterprise Automation Platform 中, 它们都属于 Connection Layer, 都需要统一管理连接资源, 而不是在每次调用时重新创建. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- requests.Session() 与 requests.get() 有什么区别? 

- 为什么 Session 应创建一次并重复使用? 

- 为什么不应在每个函数内部创建新的 Session? 

- Session 属于 Business Layer 还是 Connection Layer? 

- 为什么本节没有讨论 Cookie 和 Authentication? 

- 引入 Session 后, API Client 在架构上发生了什么变化? 

## Summary

本节引入了 HTTP Session, 进一步完善了 api_client.py: 

- 使用 requests.Session() 统一管理 HTTP 通信上下文. 

- 所有请求共享同一个 Session, 而不是重复创建. 

- 保持 Session 完全封装在 API Client 内部, 不暴露给 Business Logic. 

- 为后续加入认证, 公共 Header, Cookie 管理等能力奠定了基础. 

至此, api_client.py 已经具备了企业级 HTTP Client 的核心框架: 共享 Session, 统一请求发送, 统一超时控制, 统一异常处理, 统一状态码验证以及统一日志记录. 后续章节将在这一框架上逐步增加认证和更高级的通信能力, 而无需改变上层业务模块. 