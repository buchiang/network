这里不继续堆功能(例如 raise_for_status(), 认证, Session 等). 

按照我们 Workbook 前面几章的风格, 这里应该先统一设计 API Client 的返回契约(Return Contract). 

这是企业开发里比 requests 本身更重要的一件事情. 

很多教程都会直接继续讲: `response.raise_for_status()` 但是企业项目真正首先讨论的是 API Client 应该向上层返回什么? 

因为一旦接口设计好了, 后面加入认证, Session, 日志, Retry 都不会影响 Business Logic. 

所以这一节应该放在这里. 

## Theory

目前我们的 `api_client.py`: 

```python
def get(url):
    try:
        return requests.get(url)

    except requests.RequestException:
        return None
```

Business Logic: 

```python
response = api_client.get(url)

if response is None:
    ...
```

虽然已经能够工作. 但是这里仍然存在一个设计问题. 

>API Client 到底应该返回什么? 

这是所有通信模块都会遇到的问题. 不仅仅是 HTTP, SSH, NETCONF, RESTCONF, gRPC 都会面对同一个问题. 

## Engineering Discussion

### API Client 是谁的接口? 

很多人容易误认为 API Client 是 requests 的封装, 实际上不是. 它真正的消费者(Consumer)是 Business Logic. 

因此设计时首先应该考虑 Business Logic 最希望得到什么, 而不是 requests 返回什么. 

例如 requests 返回: `<Response [200]>`

这是 requests 的设计, 并不是我们的设计. 

### 为什么不能完全暴露 requests? 

假设以后 requests 升级, 或者整个项目改成其他 HTTP Library. 

例如: (这里只讨论概念, 不引入新的库. )

如果 Business Logic 到处都是: 

```python
response.status_code

response.headers

response.cookies
```

那么整个项目都会受到影响. Business Logic 实际上已经依赖 requests, 而不是 API Client. 因此 API Client 应该成为整个平台唯一知道 requests 存在的地方. 

## 什么是 Return Contract? 

Return Contract 就是 API Client 向外承诺我一定返回什么. 

例如下面三种设计. 

方案一: 始终返回 Response Object. 

```python
response = api_client.get(...)
```

优点: 最简单

缺点: Business Logic

知道: requests. 

方案二: 始终返回 Python Object. 

例如: `device = api_client.get(...)`

Business Logic 直接得到: Dictionary. 

完全不知道: HTTP. 

方案三: 返回统一结果对象. 

例如: 

```
Request Result

├── success
├── status
├── data
└── message
```

这是很多大型项目采用的方法, 但是目前对于 Workbook 来说复杂度过高. 

因此暂不采用. 

## 为什么目前继续返回 Response? 

本 Workbook 当前阶段. 

推荐继续返回 `requests.Response` 原因有三个. 

第一, 学习成本最低. 

目前读者正在学习 HTTP, 如果再引入自己的 Response Class 反而会增加理解难度. 

第二, 后面可以逐步演进.

例如未来:

Response ➡ Enterprise Response ➡ Business Object

架构可以自然升级, 不用推倒重来. 

第三, 保持 Connection Layer. 

只负责通信. Business Layer 负责业务. 

这种边界目前最清晰. 

## Layered Architecture

目前的数据流保持: 

```
Business Logic
        │
        ▼
Response Object
        │
        ▼
API Client
        │
        ▼
requests
        │
        ▼
HTTP
```

注意 Business Logic 依赖的是 API Client. 不是 requests, 这一点非常重要. 虽然目前 Response 来自 requests, 但是所有创建, 异常处理, 发送, 接收. 全部隐藏在: API Client. 

## Engineering Analysis

很多初学者会认为 

```ptyhon
return requests.get(...)
```

和 

```python
response = requests.get(...)
return response
```

没有区别. 实际上真正重要的是返回行为由 API Client 定义. 

例如以后如果需要统一 `response.raise_for_status()` 或者统一记录: 

```
Request Time

Response Time
```

Business Logic 完全不用修改. 因为 Contract 没有变化. 这就是 API Interface稳定的重要性. 

## 为什么现在不直接返回 `response.json()`? 

很多教程喜欢这样写: 

```python
def get(url):
    response = requests.get(url)
    return response.json()
```

看起来很方便, 但是这样做会丢失很多重要信息. 

例如: Business Logic

无法获得: `response.status_code`

也无法获得: `response.headers`

更无法知道服务器到底返回了什么, 因此目前阶段. 仍然保留完整 Response Object. 让 Business Logic 根据需要读取: 

```python
response.json()

response.status_code
```

这样接口保持最大灵活性. 

## Engineering Best Practice

企业项目中, 一个通信模块应首先保证: 

- 返回行为稳定. 

- 接口尽可能简单. 

- 不要让上层依赖底层通信库的实现细节. 

- 未来能够平滑扩展, 而不是频繁修改接口. 

目前的 `api_client.py` 已经满足这些目标: 

- 统一发送请求. 

- 统一处理通信异常. 

- 统一返回 `Response` 对象. 

后续新增认证, 超时, 日志, 重试等能力, 都可以在保持接口不变的前提下完成. 

## Engineering Insight

这一节虽然没有增加新的代码, 却完成了一个比代码更重要的设计决策: 

>API Client 的价值, 不在于包装了多少 requests 函数, 而在于它定义了整个 Enterprise Automation Platform 与 HTTP 通信之间的契约(Contract). 

前面的章节, 我们已经分别建立了: 

- Inventory Contract: Inventory Module 提供统一的设备数据. 

- Renderer Contract: Renderer Module 提供统一的配置渲染结果. 

- Connection Contract: SSH Connection Module 提供统一的设备连接能力. 

现在API Client 建立了 HTTP Communication Contract. 所有上层模块都通过这一契约访问 HTTP 服务, 而无需了解底层实现细节. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 什么是 API Client 的 Return Contract? 

- 为什么 API Client 的接口应面向 Business Logic, 而不是面向 requests? 

- 为什么目前保留 Response 对象, 而不是直接返回 response.json()? 

- 返回契约稳定对后续扩展有什么好处? 

- API Client 在整个 Enterprise Automation Platform 中承担什么角色? 

## Summary

本节没有增加新的 HTTP 功能, 而是确定了 api_client.py 的接口设计原则: 

- API Client 是 Business Logic 与 HTTP 通信之间的统一接口. 

- 当前阶段保持返回 Response 对象, 以兼顾学习目标和接口灵活性. 

- 通过稳定的返回契约, 为后续加入认证, 日志, 超时, 状态码检查, 重试等功能奠定基础, 而无需修改上层业务代码. 

- 这一步完成后, 我们再继续完善 api_client.py 的能力, 就能够始终保持整个平台的分层架构和接口稳定性. 