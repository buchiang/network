Theory(理论)

上一节我们使用：

```python
response.text
```

查看了服务器返回的数据. 

虽然看到的是 JSON 格式：

```json
{
    "userId": 1,
    "id": 1,
    "title": "...",
    "body": "..."
}
```

但是需要注意 response.text 返回的是字符串(String). 而不是 Python Dictionary, 这一点非常重要. 

## Engineering Discussion

### 为什么不能直接处理 response.text? 

假设服务器返回：

```json
{
    "hostname": "R1",
    "ip": "10.1.1.1"
}
```

如果：`print(response.text)`

Python 得到的是：`'{"hostname":"R1","ip":"10.1.1.1"}'`

注意两边的：`'`

说明这是一个字符串, 字符串虽然可以打印, 但是不能直接：`response.text["hostname"]`

因为字符串没有 hostname 这个字段. 因此自动化程序真正需要的是 Python Object. 而不是 JSON String. 

### requests 如何处理 JSON? 

requests 已经帮我们准备好了一个非常方便的方法：

```python
response.json()
```

它的作用不是获取 JSON. 而是将 Response Body 中的 JSON 转换成 Python 对象, 这一点要特别注意. 

很多初学者容易认为：`response.json()` 返回 JSON. 实际上 JSON 是一种文本格式. Python 并不存在 JSON 类型. 真正返回的是 Python Object. 

通常是：

- dict

- list

取决于服务器返回的数据. 

## Hands-on Lab

修改程序：

```python
import requests

url = "https://jsonplaceholder.typicode.com/posts/1"

response = requests.get(url)

data = response.json()

print(data)
print(type(data))
```

运行：`python3 scripts/http_get.py`

输出: `<class 'dict'>`

可以看到 requests 已经把 JSON 自动转换为了 Python Dictionary. 

## 访问数据

现在 data 已经不是字符串, 因此可以直接访问字段. 

例如：

```python
print(data["id"])
print(data["title"])
print(data["body"])
```

输出类似：

```
1

sunt aut facere...

quia et suscipit...
```

这里已经完全没有 JSON Parser. 因为 requests 已经完成了转换. 

## 与 Chapter 6 的联系

现在回顾 Chapter 6

当时：

JSON File ➡ json.load() ➡ Python Dictionary

例如：

```python
with open("inventory.json") as file:
    inventory = json.load(file)
```

整个过程是：磁盘 ➡ JSON ➡ Python

现在 HTTP 通信也是一样, 只是 JSON 来源发生了变化. 

API Server ➡ JSON ➡ `response.json()` ➡ Python

可以发现 JSON 始终只是一种数据交换格式. 无论来自文件, 还是来自网络. 最终都会变成 Python Object, 这正是 Chapter 6 提前学习 JSON 的意义. 

## Response 生命周期

现在可以完整描述一次 API 返回的数据流. 

```
HTTP Response
        │
        ▼
Response Body
        │
        ▼
JSON
        │
        ▼
response.json()
        │
        ▼
Python Dictionary
        │
        ▼
Business Logic
```

Business Logic 永远处理 Python Object, 而不是 JSON 字符串. 这符合我们一直坚持的分层思想. 

## 与 CLI Automation 的比较

回顾 Chapter 9 CLI 返回 `show ip interface brief`

得到文本

然后：

Parser ➡ Python Object ➡ Compliance

而 API 返回：

HTTP Response ➡ JSON ➡ response.json() ➡ Python Object ➡ Business Logic

两种方式最终都会得到 Python Object. 区别在于 CLI 需要我们自己编写 Parser. HTTP API 因为采用了结构化数据, 大部分情况下可以直接转换. 这也是 API 自动化相比 CLI 自动化的重要优势. 

## Engineering Best Practice

在企业项目中, 建议形成固定的处理流程：

发送 Request ➡ 检查 Status Code ➡ 确认请求成功 ➡ response.json() ➡ Business Logic

而不是：

发送 Request ➡ response.json() ➡ 开始处理

原因很简单, 如果服务器返回：`500 Internal Server Error` 或者 `404 Not Found` Body 中的数据可能并不是业务数据. 

因此检查状态码仍然应该放在 JSON 解析之前, 这也是企业项目中最常见的处理顺序. 

## Engineering Insight

这里有一个容易混淆的地方. 很多人说 "API 返回的是 JSON. " 更准确地说应该是 HTTP Response Body 中包含 JSON 文本. 

而 `response.json()`

返回的是：Python Object. 

自动化程序真正处理的, 

始终都是 Python 的数据结构. 

这一点解释了为什么前面章节一直强调：

>Business Logic 应尽量使用 Python Object, 而不是直接处理原始通信数据. 

## Engineering Checklist

完成本实验后, 应能够回答以下问题：

- response.text 与 response.json() 有什么区别? 

- response.json() 返回的是 JSON, 还是 Python Object? 

- 为什么 response.text 不适合直接进行业务处理? 

- 本实验与 Chapter 6 的 json.load() 有什么共同点? 

- API 自动化相比 CLI 自动化, 为什么通常不需要编写复杂的 Parser? 

- 企业项目中, 为什么应先检查 status_code, 再调用 response.json()? 

## Summary

本实验完成了从 HTTP Response 到 Python Object 的转换过程：

- `response.text`：返回响应内容的字符串表示. 

- `response.json()`：将 JSON 响应解析为 Python 对象. 

- Business Logic：应处理 Python Object, 而不是 JSON 字符串. 

至此, 我们已经具备了读取 API 数据的基本能力. 下一节将开始学习如何向服务器发送业务数据, 即使用 POST Request 与 HTTP Body, 将 Python 数据转换为 JSON Payload 并发送给 API 服务, 这将与本节形成完整的双向数据流. 