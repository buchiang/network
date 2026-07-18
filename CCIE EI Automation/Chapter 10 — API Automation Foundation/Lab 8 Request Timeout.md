到这里, 我们已经完成了一个能够工作的 `api_client.py`. 但是, 如果直接把它放到企业项目中, 还存在一个明显的问题 `response = requests.get(url)` 这里没有任何限制. 

如果服务器一直没有响应, 会发生什么? 

答案是程序可能一直等待对于自动化平台而言, 这是不可接受的. 

因此, 下一步应该加入: Timeout(超时控制)这是企业 HTTP Client 的基本能力之一. 

## Theory

目前 `response = requests.get(url)` requests 会等待服务器返回结果. 

如果: 

- 网络非常慢

- API Server 无响应

- TCP 已建立但服务器没有返回数据

程序可能等待很长时间. 

在自动化平台中, 这意味着 Inventory ➡ API Request ➡ 一直等待…… ➡ 整个 Workflow 被阻塞

因此企业项目通常都会设置 Timeout. 

## Engineering Discussion

### Timeout 的意义

很多人认为 Timeout 是为了提高速度, 实际上不是. Timeout 的真正目的只有一个防止程序无限等待. 它保护的是整个 Workflow. 

例如: 

Generate Report ➡ Get Device Inventory ➡ Get Interface Information ➡ Generate Report

如果第二步一直等待, 那么整个流程都会停止. Timeout 可以让程序在合理时间内结束等待, 并决定下一步如何处理. 

Timeout 属于哪一层? 

根据前面建立的架构: 

Business Logic ➡ API Client ➡ requests ➡ HTTP

Timeout 属于 HTTP Communication. 

因此它应该由 API Client 统一设置. 

Business Logic 不应该写 `requests.get(url, timeout=10)` 否则 Timeout 又会散落到整个项目. 

## Hands-on Lab

修改: 

```python
import requests

DEFAULT_TIMEOUT = 10


def get(url):
    try:
        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT
        )

        if not _check_status(response):
            print(f"HTTP Error: {response.status_code}")
            return None

        return response

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

POST 同样: 

```python
def post(url, payload):
    try:
        response = requests.post(
            url,
            json=payload,
            timeout=DEFAULT_TIMEOUT
        )

        if not _check_status(response):
            print(f"HTTP Error: {response.status_code}")
            return None

        return response

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

## 为什么使用常量? 

这里没有直接写 `timeout=10` 而是 `DEFAULT_TIMEOUT = 10` 原因是 Timeout 属于整个 API Client 的配置. 

以后如果需要调整例如 10秒 ➡ 30秒. 只需要修改一个地方. 

而不是搜索整个项目. 

## Timeout 应该由 Business Logic 决定吗? 

很多项目容易出现: 

```python
api_client.get(url, timeout=5)

api_client.get(url, timeout=20)

api_client.get(url, timeout=60)
```

虽然这种设计很灵活, 但是对于当前 Workbook 的平台来说统一策略更加重要. 

Business Logic 应该表达获取设备信息, 而不是获取设备信息, 并等待 17 秒. 

等待多久-属于通信策略. 因此应该由 API Client 统一决定. 如果未来确实出现特殊需求, 再扩展接口, 而不是一开始就增加复杂度. 

## Workflow 的变化

现在一次请求的完整生命周期变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ├── Build Request
        ├── Apply Timeout
        ├── Send Request
        ├── Handle Communication Exception
        ├── Validate Status Code
        └── Return Response
```

Business Logic 仍然只有一句 `response = api_client.get(url)` 通信策略已经进一步下沉. 

## Engineering Analysis

注意 Timeout 与: 

```
404

500
```

完全不同. 

Timeout 发生在服务器返回 Response 之前. 因此属于 Communication Exception. 而 404 说明服务器已经成功收到请求. 

因此属于 HTTP Response 整个流程可以表示为: 

```
Send Request
      │
      ▼
Timeout ?
 │        │
Yes      No
 │        ▼
Exception  Receive Response
              │
              ▼
       Status Code Validation
```

这再次验证了前面建立的错误分类模型. 

## Engineering Best Practice

企业项目通常遵循以下原则: 

- 每个 HTTP 请求都应设置 Timeout. 

- Timeout 应由通信层统一管理. 

- 不要依赖第三方库的默认等待行为. 

- 避免在 Business Logic 中重复指定 Timeout. 

这样既保证了代码一致性, 也方便后续根据生产环境统一调整通信策略. 

## Engineering Insight

Timeout 看似只是增加了一个参数 `timeout=10` 实际上, 它体现的是一种设计原则通信策略应集中管理, 而不是由业务代码决定. 

前面我们已经统一了: 

- 请求发送

- 通信异常

- 状态码验证

现在Timeout 也加入了统一管理. 

可以看到, api_client.py 正在逐步成为整个平台唯一负责 HTTP 通信策略的模块, 而不是简单地包装几个 requests 函数. 

Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么企业项目应始终设置 Timeout?

- Timeout 与 HTTP 404 有什么本质区别?

- 为什么 Timeout 应由 API Client 统一管理?

- 为什么使用 DEFAULT_TIMEOUT 常量, 而不是直接写数字?

- Timeout 属于通信策略还是业务逻辑?

- 当前 API Client 已经统一管理了哪些通信策略? 

## Summary

本节为 api_client.py 增加了统一的超时控制: 

- 引入 DEFAULT_TIMEOUT 作为统一配置. 

- 为所有 HTTP 请求设置 Timeout, 避免无限等待. 

- 将 Timeout 明确归类为通信策略, 由 API Client 集中管理. 

- 保持 Business Logic 与通信实现进一步解耦. 

至此, 我们的 API Client 已经具备了发送请求、异常处理、状态码验证和超时控制等基础能力. 下一步, 将继续完善这一模块, 引入统一日志记录(Logging), 使每一次 HTTP 请求都能够被自动记录, 为后续故障排查和审计提供支持. 这也将与前面章节建立的日志体系保持一致. 