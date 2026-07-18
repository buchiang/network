很好, 到这里, 我们已经完成了 `api_client.py` 的整体框架设计. 接下来, 就应该真正完善这个模块. 

按照企业项目的请求生命周期, 现在缺少的一步是: 

Send Request ➡ Communication Exception ➡ HTTP Status Code Validation ➡ Return Response

前一节已经完成了: 

- 发送请求

- 通信异常处理

- 返回契约

现在应该加入: 

>统一的 HTTP Status Code Validation. 

这是一个企业 API Client 必须具备的能力. 

## Theory

在 Chapter 10 前半部分, 我们已经学习了 HTTP Status Code 分为: 

- 2xx —— Success

- 4xx —— Client Error

- 5xx —— Server Error

但是, 到目前为止, 我们的 API Client 并没有真正使用这些知识. 

例如: 

```python
response = api_client.get(url)

print(response.status_code)
```

Business Logic 仍然需要自己判断: 

```python
if response.status_code == 200:
    ...
```

或者: 

```python
if response.status_code == 404:
    ...
```

这样做虽然没有问题, 但是随着项目越来越大, 这种判断会不断重复. 

## Engineering Discussion

### 谁应该检查 Status Code? 

这里有两个方案. 

方案一, 每个业务模块自己检查. 

例如: 

```python
response = api_client.get(url)

if response.status_code != 200:
    ...
```

Compliance 检查一次. 

Inventory 检查一次. 

Deployment 检查一次. 

Monitoring 再检查一次. 

整个项目到处都是 `if response.status_code ...` 

这种设计违反了

>Don't Repeat Yourself(DRY)

方案二, 统一交给 API Client. 

流程变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ├── Send Request
        ├── Handle Exception
        ├── Validate Status Code
        └── Return Response
```

Business Logic 不用重复编写 HTTP 判断逻辑. 这更加符合 Layered Architecture. 

## 什么叫 Success? 

很多初学者容易认为 200 才代表成功. 

实际上, HTTP 定义的是整个 2xx 都属于 Success. 

例如: 

| Status Code | 含义       |
| ----------- | ---------- |
| 200         | OK         |
| 201         | Created    |
| 202         | Accepted   |
| 204         | No Content |


因此企业项目一般不会写: `if response.status_code == 200:`

而是判断是否属于 2xx. 

## Hands-on Lab

首先新增一个内部函数: 

```python
import requests


def _check_status(response):
    """
    Validate HTTP status code.

    Args:
        response (requests.Response): HTTP response.

    Returns:
        bool: True if request succeeded.
    """
    return 200 <= response.status_code < 300
```

这里使用 `_check_status()`

注意前面的: `_` 表示这是 API Client 内部使用的辅助函数. 

Business Logic 不应该直接调用. 

修改: 

```python
def get(url):
    try:
        response = requests.get(url)

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
        response = requests.post(url, json=payload)

        if not _check_status(response):
            print(f"HTTP Error: {response.status_code}")
            return None

        return response

    except requests.RequestException as error:
        print(f"HTTP request failed: {error}")
        return None
```

## 为什么使用内部函数? 

很多人可能会写 `if 200 <= response.status_code < 300:`

然后复制到GET, POST, PUT, PATCH, DELETE. 以后如果修改判断逻辑, 需要修改五个地方. 

因此封装成 `_check_status()` 以后整个项目只有一个地方负责 Status Code Validation. 这也是 DRY Principle 的体现. 

## Workflow 的变化

现在 Business Logic 进一步简化. 

例如: 

```python
response = api_client.get(url)

if response is None:
    print("Request failed.")
else:
    data = response.json()
    print(data)
```

Business Logic 已经不知道失败原因到底是: 

- Timeout

- DNS

- 404

- 500

它只知道请求成功, 或者失败. 这种抽象正是 Connection Layer 存在的意义. 

## Engineering Analysis

现在 API Client 已经形成完整流程. 

```
Business Logic
        │
        ▼
api_client.get()
        │
        ▼
requests.get()
        │
        ▼
Communication Exception?
        │
    Yes │ No
        ▼
     Return None
        │
        ▼
Status Code Validation
        │
    Fail │ Pass
        ▼
 Return None   Response
```

Business Logic 完全不用关心 HTTP 细节, 所有通信相关工作. 已经全部收敛到 API Client. 

## 为什么这里没有使用 `raise_for_status()`? 

requests 提供了 `response.raise_for_status()` 它可以把 4xx 和 5xx 转换成异常, 这是一个很方便的功能, 但是当前 Workbook 暂时不使用,原因有两个. 

第一, 目前我们希望明确区分: 

- 通信异常

- HTTP 响应错误

如果立即使用 `raise_for_status()`, 这两类情况都会表现为异常, 不利于初学者理解整个请求生命周期. 

第二, 自己实现 `_check_status()`, 能够更清楚地体现 API Client 拥有 Status Code Validation 的职责, 而不是完全依赖第三方库提供的默认行为. 在读者理解了这一设计之后, 再介绍 raise_for_status() 会更加自然. 

## Engineering Best Practice

企业项目中, 一个成熟的 API Client 通常负责: 

- 统一发送请求. 

- 统一处理通信异常. 

- 统一验证 HTTP Status Code. 

- 统一返回结果. 

Business Logic 只负责业务流程. 而不是通信流程. 

这种职责划分, 使得整个系统更容易维护, 也便于未来统一加入日志、认证、重试和监控. 

# Engineering Insight

到目前为止, 我们已经逐步把一个简单的 `requests.get(url)` 演化成了一个真正具有工程意义的通信组件. 

这个演化过程体现了一个重要思想:

>企业工程并不是不断增加新功能, 而是不断把重复的、共性的能力向下沉淀到基础模块. 

`api_client.py` 现在已经不仅是一个 `requests` 包装器, 它开始承担整个平台 HTTP 通信入口的职责. 未来无论增加认证、Session、日志还是重试, 都将在这个统一入口中完成, 而不会扩散到业务代码中. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么不建议每个业务模块自行检查 status_code? 

- 为什么 _check_status() 使用 2xx 范围, 而不是只判断 200? 

- 为什么 _check_status() 设计为 API Client 的内部函数? 

- 通信异常与 HTTP Status Code Validation 在请求生命周期中的顺序是什么? 

- 为什么本章暂时没有使用 response.raise_for_status()? 

- API Client 当前已经承担了哪些统一职责? 

## Summary

本节进一步完善了 api_client.py: 

- 新增统一的 HTTP Status Code Validation. 

- 使用内部辅助函数 _check_status() 避免重复代码. 

- 将 HTTP 成功定义为整个 2xx 状态码范围, 而不仅是 200. 

- 保持 Business Logic 与 HTTP 通信细节完全解耦. 

至此, api_client.py 已经具备了一个企业级通信模块的基本能力: 发送请求 → 处理通信异常 → 验证 HTTP 状态码 → 返回统一结果. 后续章节将在此基础上继续加入认证、超时配置、日志记录和会话管理, 而无需改变上层业务代码. 