## Theory

在 [Chapter 10.8](<Chapter 10.8 Python HTTP Client.md>) 已经介绍了: 

- HTTP 是通信协议

- requests 是 Python 的 HTTP Client Library

这一节开始, 我们第一次使用 requests. 

目标只有一个**完成一次 HTTP GET 请求**. 

暂时不考虑: 

- 身份认证

- JSON Payload

- POST

- PUT

- DELETE

- 企业 API

我们只关注 **Python 如何发送 HTTP Request, 并接收 HTTP Response.**

## Engineering Discussion

### 为什么选择 GET? 

HTTP Method 有很多: 

- GET

- POST

- PUT

- PATCH

- DELETE

其中 GET 最容易理解, 因为 GET 不会修改服务器的数据, 它只是读取资源. 

这与我们在 CLI 中执行: 

```
show version

show interface

show inventory
```

非常类似. 

因此第一段代码选择 GET, 是最自然的学习路径. 

### 为什么暂时使用公共测试 API? 

目前我们的 Enterprise Automation Platform 还没有接入任何真实的网络控制器. 

如果直接使用某个厂商的 API: 

- 需要账号

- 需要认证

- 需要实验环境

- 需要提前介绍厂商平台

这违反了 Workbook 的 Roadmap. 

因此我们先使用一个公开提供的测试 API. 

它的唯一作用就是**帮助我们理解 HTTP 通信.**

后面学习具体网络平台时, 再替换为真实的 API Endpoint. 

## Hands-on Lab

### 安装 requests

首先确认已经安装 requests. 

```bash
pip install requests
```

安装完成后, 可以验证版本: 

```bash
pip show requests
```

### 第一个程序

创建: `scripts/http_get.py`

代码如下: 

```
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

print(response)
```

运行: `python3 scripts/http_get.py`

输出类似: `<Response [200]>`

## Engineering Analysis

虽然只有一行输出: `<Response [200]>`

但实际上已经完成了一次完整的 HTTP 通信. 

整个过程如下: 

```
Python Program
        │
        ▼
requests.get()
        │
        ▼
HTTP Request
        │
        ▼
Internet
        │
        ▼
API Server
        │
        ▼
HTTP Response
        │
        ▼
Response Object
```

需要注意返回的并不是 JSON

而是 Response Object

也就是说服务器返回的数据, 已经被 requests 封装成了一个 Python 对象. 这一点与 Netmiko 十分相似. 

例如: `output = connection.send_command(...)`

返回的是: CLI 输出. 

而: `response = requests.get(...)`

返回的是: Response Object. 

后续所有信息例如: 

- Status Code

- Headers

- JSON Body

都是从这个对象中获取. 

## 查看 Status Code

上一节学习过 Status Code 是程序首先应该检查的内容. 

因此修改程序: 

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

print(response.status_code)
```

运行: `python3 scripts/http_get.py`

输出: 200

说明服务器已经成功处理请求.

这里再次验证了上一节建立的工程原则:

HTTP Request → Status Code → Business Logic

程序首先获得: Status Code.

然后才决定是否继续处理数据.

## 查看 Response Body

服务器真正返回的数据位于 Response Body. 

可以使用 `print(response.text)`

输出类似: 

```
{
  "userId": 1,
  "id": 1,
  "title": "...",
  "body": "..."
}
```

可以发现 Body 中保存的是 JSON 数据. 

这正好对应上一节学习的: 

HTTP Response → Body → JSON Payload

## Response Object 提供了什么? 

目前我们已经接触到三个最重要的属性. 

| 属性                   | 作用          |
| -------------------- | ----------- |
| response.status_code | 获取 HTTP 状态码 |
| response.text        | 获取响应内容（字符串） |
| response.headers     | 获取响应头       |

后续章节还会介绍: 

- `response.json()`

- `response.content`

- `response.raise_for_status()`

目前无需提前学习, 保持知识递进. 

## 与 Enterprise Automation Platform 的关系

目前代码直接写成: 

```python
response = requests.get(url)
```

只是为了帮助理解 requests 的基本使用. 这不是最终的工程实现. 

按照前面建立的架构: 

Business Logic → API Client → requests → HTTP

未来: `requests.get()`

不会散落在业务代码中, 而是统一封装到 `modules/` 中的 API Client 模块. 

本节只是验证 Python 已经具备发送 HTTP Request 的能力. 

## Engineering Best Practice

虽然目前代码非常简单: 

```python
response = requests.get(url)
```

但在企业项目中, 应逐步养成以下习惯: 

- 始终检查 status_code, 不要假设请求一定成功. 

- 不要立即解析返回内容, 先确认请求是否成功. 

- 避免在业务代码中大量直接调用 requests.get(), 后续将统一封装到 API Client 中. 

- 保持通信逻辑与业务逻辑分离, 继续遵循 Workbook 的 Layered Architecture. 

这些原则将在后续实验中不断强化. 

## Engineering Checklist

完成本实验后, 应能够回答以下问题: 

- `requests.get()` 的作用是什么? 

- `requests.get()` 返回的是 JSON, 还是 Response Object? 

- 如何获取 HTTP Status Code? 

- 如何获取 Response Body? 

- 为什么程序应先检查 `status_code`, 再处理响应内容? 

- 为什么当前示例代码不是最终的企业工程实现? 

## Summary

本实验完成了 Chapter 10 的第一次 HTTP 通信: 

- 使用 `requests` 发送了一个 GET Request. 

- 获得了 Response Object. 

- 读取了 Status Code. 

- 查看了 Response Body. 

- 验证了 HTTP Request → HTTP Response 的完整流程. 