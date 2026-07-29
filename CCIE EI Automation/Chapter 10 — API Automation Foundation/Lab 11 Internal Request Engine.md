很好, 现在 Session 已经建立. 下一步不应该立即讲 Authentication, 因为目前还有一个更基础的问题没有解决. 

我们的代码仍然是 `response = session.get(url)` 或者 `response = session.post(url, json=payload)` 虽然已经比前面好了很多, 但是还有一个明显的问题 GET 和 POST 出现了大量重复代码. 

例如: 

- Logging

- Timeout

- Exception Handling

- Status Validation

这些代码几乎完全一样. 企业工程下一步应该做的, 就是消除重复代码(Code Duplication), 这也是前面几章一直坚持的 DRY Principle. 

## Theory

目前 `api_client.py` 大致结构如下: 

GET:

```python
def get(url):

    logger.info(...)

    try:

        response = session.get(...)

        ...

        return response

    except ...

        ...
```

POST: 

```python
def post(url, payload):

    logger.info(...)

    try:

        response = session.post(...)

        ...

        return response

    except ...

        ...
```

可以发现除了 `session.get(...)` 和 `session.post(...)` 其它代码几乎一样. 

这意味着我们已经出现重复逻辑. 

## Engineering Discussion

### 为什么重复代码不好? 

假设以后需要记录 Request Duration. 

现在需要修改 GET, POST, 未来 PUT, PATCH, DELETE 全部都要修改. 

如果以后增加 Retry 仍然修改五六个函数. 

很明显这些能力属于所有 HTTP Request 的共性能力. 

因此应该集中, 而不是复制. 

## 提炼共同流程

仔细观察 GET, POST 真正不同的. 

只有这一行 `session.get(...)` 或者 `session.post(...)` 其它步骤完全一致. 

整个流程实际上都是: 

Write Request Log ➡ Send Request ➡ Handle Exception ➡ Validate Status ➡ Write Response Log ➡ Return Response

因此我们可以把整个流程抽象出来. 

## Layered Architecture

新的结构: 

```
Business Logic
        │
        ▼
api_client.get()
        │
        ▼
_request()
        │
        ▼
Session
        │
        ▼
HTTP
```

注意现在 GET, POST 已经不是真正发送请求. 而是调用统一 Request Engine. 

## Hands-on Lab

新增内部函数: 

```python
def _request(method, url, **kwargs):
    """
    Send an HTTP request.

    Args:
        method (str): HTTP method.
        url (str): API endpoint.

    Returns:
        requests.Response | None
    """

    logger.info(f"{method} {url}")

    try:

        response = session.request(
            method=method,
            url=url,
            timeout=DEFAULT_TIMEOUT,
            **kwargs
        )

        logger.info(
            f"HTTP Response {response.status_code}"
        )

        if not _check_status(response):
            logger.error(
                f"HTTP Error {response.status_code}"
            )
            return None

        return response

    except requests.RequestException as error:

        logger.error(
            f"HTTP Request Failed: {error}"
        )

        return None
```

这里第一次使用 `session.request(...)` 需要说明. 它不是新的协议, 也不是新的库. 而是 Session 提供的**通用请求接口**. 

这里的 `**kwargs` 表示接受任意数量的关键字参数(keyword arguments), 并把他们打包成一个字典(dict).

例如

```
response = _request(
    "GET",
    "https://example.com",
    headers={"Accept": "application/json"},
    timeout=10
)
```

python 会把这些参数变为:

```
kwargs = {
    "headers": {"Accept": "application/json"},
    "timeout": 10
}
```

为什么前面要加两个 `*` 

这里有两个概念需要区分：

`*args` 收集位置参数(Positional Arguments)

```python
def test(*args):
    print(args)

test(1, 2, 3)
```

输出:

```python
(1, 2, 3)
```
它是一个 tuple.

`**kwargs` 收集关键字参数(Keyword Arguments).

```python
def test(**kwargs):
    print(kwargs)

test(a=1, b=2)
```

输出:

```python
{
    "a": 1,
    "b": 2
}
```

它是一个 dict.

### 为什么 API Client 要这样写？

如果不用 `**kwargs`, 你可能需要这样定义:

```python
def _request(
    method,
    url,
    headers=None,
    params=None,
    json=None,
    timeout=10,
    verify=True,
    auth=None,
    cookies=None,
    proxies=None,
):
    ...
```

随着 `requests.request()` 支持的参数越来越多, 你就必须不断修改 `_request()` 的参数列表.

而使用:

```python
def _request(method, url, **kwargs):
```

无论调用者传入什么参数, 都可以直接转交给 `requests.request()：`

`return requests.request(method, url, **kwargs)`

例如:

```python
_request(
    "GET",
    url,
    headers=headers,
    timeout=10,
    verify=False,
    params=params
)
```

等价于:

```python
requests.request(
    "GET",
    url,
    headers=headers,
    timeout=10,
    verify=False,
    params=params
)
```

这样 `_request()` 就成了一个通用的中间层(Internal Request Engine).

## 简化 GET

现在 GET 变成: 

```python
def get(url):

    return _request(
        "GET",
        url
    )
```

整个函数只剩下一行. 

## 简化 POST

POST 也变成: 

```python
def post(url, payload):

    return _request(
        "POST",
        url,
        json=payload
    )
```

可以发现 POST 真正特殊的只有 `json=payload` 其它工作全部交给 `_request(). `

## 为什么使用 `_request()`? 

有人可能会问为什么不继续: 

```python
session.get()

session.post()
```

原因是企业工程真正关心的是请求生命周期. 而不是 HTTP Method. 现在所有 Method 都共享同一个生命周期. 

Request ➡ Logging ➡ Timeout ➡ Exception ➡ Status Validation ➡ Return

这就是 Request Engine 存在的意义. 

## Workflow 的变化

现在一次 GET 实际上变成: 

Business Logic ➡ get() ➡ _request() ➡ session.request() ➡ HTTP

POST 也是同样流程, 未来 PUT, PATCH, DELETE 无需重新实现. 只需要调用 `_request(...)` 即可. 

## Engineering Analysis

这一节最大的变化不是代码减少了, 真正重要的是我们完成了流程抽象(Workflow Abstraction). 

以前 GET 拥有自己的流程. POST 拥有自己的流程. 

现在整个 HTTP Client 只有一套流程. 

以后如果增加 Retry. 

例如: 

Logging ➡ Retry ➡ Timeout ➡ Exception ➡ Status Validation

只需要修改 `_request()` 整个项目全部生效. 

## 为什么 `_request()` 是内部函数? 

注意函数名 `_request()` 前面的 `_` 表示内部实现. 

Business Logic 永远不会调用 `_request(...)`

Business Logic 应该使用: 

```python
api_client.get()

api_client.post()
```

这样 API Client 仍然保持简单, 稳定, 易读. 

## Engineering Best Practice

成熟的 HTTP Client 通常都会有一个统一的请求入口: 

- 所有 HTTP Method 共用同一个请求流程. 

- 将日志, 超时, 异常处理, 状态码验证等共性能力集中管理. 

- 让各个 Method 只负责表达自己的业务语义(GET, POST, PUT 等), 而不是重复实现通信细节. 

这种设计既符合 DRY Principle, 也使得后续扩展功能几乎只需要修改一个地方. 

## Engineering Insight

这一节实际上完成了 `api_client.py` 的最后一次重要重构. 

到目前为止: 

```
API Client

├── Shared Session
├── Request Engine (_request)
├── Logging
├── Timeout
├── Exception Handling
├── Status Validation
├── GET
└── POST
```

请注意 `GET()` 和 `POST()` 已经不再是真正的"实现者". 

它们只是: 

>公开接口(Public Interface). 

真正完成工作的, 是 `_request()` 这种设计在企业软件中非常常见: 

- 对外提供简单, 稳定的接口. 

- 对内使用统一的执行引擎. 

前面 Chapters 中: 

- Renderer 隐藏了 Jinja2 的细节. 

- Connection Module 隐藏了 Netmiko 的细节. 

现在: 

API Client 隐藏了整个 HTTP 请求生命周期. 

整个 Workbook 的工程风格至此保持了高度一致. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么 GET 和 POST 会出现重复代码? 

- `_request()` 解决了什么问题? 

- 为什么使用 `session.request()` 而不是分别调用 `session.get()` 和 `session.post()`? 

- 为什么 `_request()` 应设计为内部函数? 

- 未来新增 PUT, PATCH, DELETE 时, 为什么几乎不用复制代码?

- 这一重构体现了哪些工程原则(如 DRY, Layered Architecture)? 

## Summary

本节完成了 `api_client.py` 的一次关键重构: 

- 提炼出统一的 `_request()` 请求引擎. 

- 将 Logging, Timeout, Exception Handling 和 Status Validation 等共性能力集中到一个位置. 

- 让 `get()`, `post()` 等公开接口只负责表达 HTTP Method, 而不再承担请求流程的实现. 

至此, 我们已经拥有了一个结构清晰, 职责明确的企业级 HTTP Client 骨架. 后续加入认证(Authentication), 默认请求头, 重试(Retry)或其他通信策略时, 都可以直接扩展 `_request()` 或共享 Session, 而无需修改上层业务代码或各个 HTTP Method 的接口. 