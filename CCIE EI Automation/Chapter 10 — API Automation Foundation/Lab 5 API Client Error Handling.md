很好, 现在应该继续完善 `api_client.py`, 而不是立即进入认证(Authentication)或具体厂商 API. 

原因很简单, 目前我们的 `api_client.py` 只是一个"转发器": 

```python
def get(url):
    return requests.get(url)
```

虽然完成了解耦, 但是距离企业工程还有一步, 这一节, 我们开始加入统一错误处理(Error Handling). 注意, 这里说的是HTTP 通信层的错误处理, 不是业务错误处理, 这是 API Client 最重要的职责之一. 

## Theory

目前我们的 API Client: 

```python
def get(url):
    return requests.get(url)
```

能够正常工作, 但是它假设了一件事情 HTTP Request 一定能够成功发送, 现实情况并非如此. 

例如: 

- API Server 宕机

- DNS 无法解析

- 网络中断

- TCP Connection Timeout

- SSL 建立失败

这些情况都属于通信失败(Communication Failure). 

注意它们与上一节学习的: 

```
404

500
```

不是同一种错误. 

## Engineering Discussion

### 两类完全不同的错误

很多初学者容易把所有错误混在一起, 实际上HTTP 自动化至少存在两类错误. 

第一类: **通信错误(Communication Error)**

例如: 

Python ➡ 无法连接服务器

这种情况下 HTTP Request 根本没有成功发送, 服务器甚至没有收到请求. 

因此不会存在: 

```
200

404

500
```

这些 Status Code. 

第二类: **HTTP 错误(HTTP Error)**

例如: 

Python ➡ HTTP Request ➡ API Server ➡ 404 Not Found

这里说明通信已经成功, 服务器已经收到请求. 只是服务器返回了错误结果. 

因此通信成功, 业务失败. 

整个流程可以表示为: 

```
                API Request
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
Communication Failed      HTTP Response Received
         │                       │
         ▼                       ▼
Exception              Status Code
```

这是后续整个 API 自动化中最重要的错误分类. 

## 为什么 API Client 要处理通信错误? 

假设: 

Business Logic: `generate_report()`

里面直接: `requests.get(...)`

如果服务器断网, 程序可能直接抛出异常. 

Business Logic 突然开始处理: 

- Timeout

- DNS

- SSL

- Socket

这显然违反了 Single Responsibility Principle. 

Business Logic 应该只关心: 

>"设备信息是否获取成功? "

而不是 TCP 为什么建立失败. 

因此通信异常, 应该首先由 API Client 负责. 

## Hands-on Lab

修改: `modules/api_client.py`

第一版错误处理:

```python
import requests


def get(url):
    """
    Send an HTTP GET request.
    """
    try:
        return requests.get(url)

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None


def post(url, payload):
    """
    Send an HTTP POST request.
    """
    try:
        return requests.post(url, json=payload)

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

这里第一次出现 `requests.RequestException`

它是 requests 提供的通用异常类型, 能够覆盖绝大多数通信错误. 目前我们不展开各种具体异常, 保持本章的学习节奏.

## 修改 Workflow

由于 API Client

现在可能返回 `None`

Workflow 需要进行简单检查. 

例如: 

```python
from modules import api_client

url = "https://jsonplaceholder.typicode.com/posts/1"

response = api_client.get(url)

if response is None:
    print("Request failed.")
else:
    print(response.status_code)
```

这里要注意, Workflow 仍然没有处理 Timeout, DNS, SSL. 它只知道请求失败, 真正的通信细节仍然隐藏在 API Client. 

## Engineering Analysis

现在整个平台的数据流已经发生变化. 

以前: 

Business Logic ➡ requests ➡ HTTP

现在: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
Communication Error Handling
        │
        ▼
requests
        │
        ▼
HTTP
```

Business Logic 根本不知道 requests 抛出了什么异常. 它只知道请求成功, 或者失败.

这就是 Layered Architecture 最大的价值.

为什么这里只处理通信异常?

很多读者可能会问为什么 404 没有在 API Client 里面处理? 

答案是因为 404 并不是通信失败. 

例如: 

Python ➡ HTTP Request ➡ Server ➡ 404

整个通信完全成功. 

只是服务器告诉客户端资源不存在. 

因此 404 属于 HTTP Response, 而不是 Communication Exception. 

后面我们会讨论如何统一处理 Status Code. 目前 API Client 只负责确保请求能够正常发送. 

## Engineering Best Practice

在企业项目中, 可以遵循如下职责划分: 

| 类型               | 处理位置             |
| ---------------- | ---------------- |
| 网络中断             | API Client       |
| DNS 失败           | API Client       |
| Timeout          | API Client       |
| SSL 异常           | API Client       |
| HTTP Status Code | API Client(统一检查) |
| 业务逻辑判断           | Business Logic   |

这样做的好处是整个项目中所有通信问题, 都集中在一个模块. 而不是散落在几十个业务脚本里面. 

## Engineering Insight

这里需要注意一个容易混淆的地方. 很多教程会说 "404 是 Exception. " 实际上并不是. 对于 requests 来说服务器正常返回 404 默认不会抛出通信异常. 因为 HTTP 协议已经完成, TCP 已经建立, 服务器已经响应. 

404 只是服务器返回的一种结果. 因此在工程上通信异常(Exception)与 HTTP Status Code 应作为两类不同的问题进行处理. 

这种区分能够让 API Client 的职责更加清晰, 也符合我们一直坚持的分层设计. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 通信错误与 HTTP 错误有什么区别? 

- 为什么 API Client 应负责处理通信异常? 

- requests.RequestException 的作用是什么? 

- 为什么 Workflow 不需要知道 Timeout、DNS 等细节? 

- 为什么 404 不属于通信异常? 

- 为什么通信错误应集中在 API Client 中统一处理? 

## Summary

本节进一步完善了 `api_client.py`: 

- 引入了统一的通信异常处理. 

- 使用 requests.RequestException 捕获 HTTP 请求过程中的通信错误.

- 将网络异常与 HTTP Status Code 明确区分. 

- 保持 Business Logic 与底层通信实现解耦. 

至此, api_client.py 已经不仅仅是 requests 的简单封装, 而开始承担 Connection Layer 的职责. 下一节我们将在此基础上加入统一的 Status Code 检查, 形成完整的请求生命周期: 发送请求 → 处理通信异常 → 检查 HTTP Status Code → 返回响应对象. 这样, 一个企业级 API Client 的基本框架就初步建立起来了. 