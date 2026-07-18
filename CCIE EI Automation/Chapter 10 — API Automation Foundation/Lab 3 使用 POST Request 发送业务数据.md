## Theory

前两个实验中, 我们一直使用 GET

GET 的特点是读取资源. 

因此客户端几乎不用向服务器发送业务数据. 

真正需要发送业务数据的是: 

- POST

- PUT

- PATCH

它们都会涉及 HTTP Body. 

本实验首先学习最常见的 POST. 

## Previous Lab Review

上一节的数据流是: 

API Server ➡ JSON ➡ response.json() ➡ Python Object

这是: 服务器 ➡ 客户端 的数据流. 

现在我们要学习相反的方向: 

Python Object ➡ JSON ➡ HTTP Body ➡ API Server

可以发现整个过程正好相反. 

## Engineering Discussion

### POST 与 GET 的区别

回顾上一节. 

GET: `GET /devices`

客户端只是: 请求数据, 几乎没有业务数据需要发送. 

而 POST: `POST /devices`

服务器一定会问: "你准备创建什么设备? "

因此客户端必须把设备信息发送给服务器. 

这些数据就位于 HTTP Body. 

### Python 如何发送 Body? 

我们已经知道 HTTP Body 中通常保存的是 JSON Payload. 

而 Business Logic 一直使用 Python Dictionary. 

例如: 

```python
device = {
    "hostname": "R1",
    "management_ip": "10.1.1.1"
}
```

那么 Python Dictionary 如何变成 HTTP Body? 

这就是 requests 负责完成的工作. 

## Hands-on Lab

为了演示 POST, 我们继续使用公开测试 API. 

创建`scripts/http_post.py`

代码如下: 

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts"

payload = {
    "title": "Automation Workbook",
    "body": "Chapter 10",
    "userId": 1
}

response = requests.post(url, json=payload)

print(response.status_code)
print(response.json())
```

运行 `python3 scripts/http_post.py`

输出类似 `201`

随后: 

```
{
    "title": "...",
    "body": "...",
    "userId": 1,
    "id": 101
}
```

## Engineering Analysis

注意这一行: 

```python
response = requests.post(url, json=payload)
```

这里出现了新的参数 `json=payload`

它并不是 HTTP Method, 也不是 JSON 文件. 

它表示把 Python Dictionary 作为 JSON Payload 发送. 

requests 会自动完成以下工作: 


Python Dictionary ➡ JSON Serialization ➡ HTTP Body ➡ 发送 HTTP Request

整个过程无需我们手工转换. 

## 为什么使用 json=? 

很多初学者会问为什么不是 

```python
data=payload
```

或者: 

```python
body=payload
```

对于当前阶段, 只需要理解当使用 `json=payload` requests 会自动: 

- 将 Python Object 序列化为 JSON. 

- 将 JSON 放入 HTTP Body. 

- 设置正确的 `Content-Type`. 

因此对于发送 JSON 数据的 API, 这是最常见、也是最推荐的写法. 

至于 `data=` 与 `json=` 的区别, 我们将在后续介绍不同数据格式时再深入讨论, 避免一次引入过多概念. 

## 数据流分析

现在可以完整描述一次 POST 请求. 

```
Business Logic
        │
        ▼
Python Dictionary
        │
        ▼
requests.post(json=...)
        │
        ▼
JSON Payload
        │
        ▼
HTTP Body
        │
        ▼
API Server
```

服务器收到请求以后, 再返回: 

```
HTTP Response

↓

Status Code

↓

Response Body

↓

response.json()

↓

Python Dictionary
```

整个流程形成了一个完整的数据闭环. 

## 与前面章节的联系

回顾 Workbook 前面的内容. 

Chapter 6: 

JSON File ➡ Python Dictionary

Chapter 10(GET): 

HTTP Response ➡ JSON ➡ Python Dictionary

Chapter 10(POST): 

Python Dictionary ➡ JSON ➡ HTTP Request

可以发现, 无论数据来自: 

- 文件

- 网络响应

- 网络请求

Business Logic 始终使用 Python Dictionary. JSON 只是交换格式. 

这一设计保持了整个 Enterprise Automation Platform 的一致性. 

## Engineering Best Practice

在企业项目中, 建议遵循以下职责划分: 

Business Logic ➡ 构造 Python Object ➡ API Client ➡ 转换为 JSON ➡ 发送 HTTP Request

Business Logic 不应关心: 

- JSON 如何序列化. 

- Header 如何设置. 

- HTTP Body 如何构造. 

这些工作都属于 API Client(Connection Layer). 这样可以保证当通信细节发生变化时, 业务逻辑无需修改. 

## Engineering Insight

请注意一个容易混淆的概念很多人会说: "我发送了 JSON."

更准确的描述应该是: 

>Business Logic 构造了 Python Object；HTTP Client 将它序列化为 JSON, 并作为 HTTP Body 发送给服务器. 

这种描述明确区分了: 

- 业务数据(Python Object)

- 交换格式(JSON)

- 传输载体(HTTP Body)

这种分层思维, 将贯穿整个 Workbook. 

## Engineering Checklist

完成本实验后, 应能够回答以下问题: 

- 为什么 POST 通常需要 HTTP Body?

- json=payload 中的 payload 是什么类型?

- requests 在发送请求时自动完成了哪些工作?

- 为什么 Business Logic 应构造 Python Object, 而不是直接拼接 JSON 字符串?

- 本实验的数据流与上一节(GET)有什么区别?

- 为什么 JSON 应被视为数据交换格式, 而不是业务对象?

## Summary

本实验完成了客户端向服务器发送业务数据的全过程: 

- 使用 POST 创建资源. 

- 使用 Python Dictionary 描述业务数据. 

- 使用 json=payload 将业务数据发送给服务器.

- 理解了 requests 自动完成 JSON 序列化与 HTTP Body 构造的过程. 

至此, 我们已经掌握了 HTTP API 最核心的两种数据流: 

- GET: 服务器 → JSON → Python Object. 

- POST: Python Object → JSON → 服务器. 