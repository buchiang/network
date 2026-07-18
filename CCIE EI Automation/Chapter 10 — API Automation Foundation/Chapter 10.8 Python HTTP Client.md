Theory

到目前为止, 我们已经完整学习了 HTTP 通信模型. 

一个 HTTP Request 包括 Method ➡ URL ➡ Headers ➡ Body 但是还有一个问题没有回答. 

Python 如何发送一个 HTTP Request? 仅仅理解 HTTP 协议还不够, 我们还需要一个能够代表客户端(Client)与服务器通信的工具. 

这就是 HTTP Client. 

## Engineering Discussion

### Client 与 Server

HTTP 是一种典型的 Client-Server Architecture(客户端-服务器架构). 

例如: 

Python ➡ HTTP Client ➡ Internet / Network ➡ HTTP Server

其中 Python 程序属于 Client. 

API 所在的软件属于 Server. 

整个通信都是由 Client 发起, Server 响应. 这一点与 SSH Automation 非常类似. 

例如 Chapter 3: 

Python ➡ Netmiko ➡ SSH ➡ Network Device

这里 Netmiko 就充当了 SSH Client. 

同样 HTTP Automation 也需要 HTTP Client. 

## 什么是 HTTP Client? 

HTTP Client 可以理解为: 

>负责发送 HTTP Request, 并接收 HTTP Response 的软件组件. 

它负责完成: 

- 建立 TCP 连接

- 发送 HTTP Request

- 接收 HTTP Response

- 解析 HTTP 协议细节

- 将结果返回给 Python

因此我们的 Python 代码并不会直接操作 TCP, 也不会自己拼接 HTTP 报文. 这些工作全部由 HTTP Client 完成. 

## 为什么需要 HTTP Client? 

理论上 Python 完全可以自己构造: 

```
GET /devices HTTP/1.1
Host: server.example.com
...
```

然后通过 Socket 发送, 但是这样开发效率极低, 而且需要自己处理: 

- TCP

- HTTP

- Header

- 超时

- 重定向

- SSL

- 编码

因此几乎所有 Python 项目, 都会使用成熟的 HTTP Client Library. 

这与 Chapter 3 中几乎没有人自己实现 SSH 协议, 而是使用 Netmiko 的原因完全一致. 

## Python 的 HTTP Client

Python 标准库已经提供了 HTTP Client, 但是标准库更偏向底层, 代码通常比较繁琐. 因此企业开发中, 几乎都会使用 requests 作为 HTTP Client Library. 

需要强调的是 requests 不是 HTTP 协议, 它只是 HTTP 的一个 Python 实现. 就像 Netmiko 不是 SSH, 只是 SSH Client Library. 因此不要把 HTTP 和 requests 混为一谈. 

二者关系可以表示为: 

HTTP ➡ 通信协议 ➡ requests ➡ Python Library

## requests 在平台中的定位

回顾之前的章节. 

Chapter 3: 

Business Logic ➡ Connection Module ➡ Netmiko ➡ SSH

可以发现 Business Logic 不知道 Netmiko. 真正知道 Netmiko 的, 是 Connection Module. 

API Automation 也是一样, 未来的平台: 

Business Logic ➡ Connection Module ➡ requests ➡ HTTP

Business Logic 仍然不知道 requests, 它只知道获取设备, 或者创建接口. 真正负责 HTTP 通信的, 应该仍然是 Connection Layer. 

## 为什么不能到处调用 requests? 

很多初学者会写: 

```python
requests.get(...)

requests.post(...)

requests.put(...)
```

散落在整个项目里面. 这种方式虽然可以运行, 但是工程上存在很多问题. 

例如: 认证方式发生变化. 

需要修改几十个文件. 

或者统一增加 Timeout. 

又需要修改所有 requests. 

随着项目越来越大, 维护成本会快速增加. 因此企业工程更推荐: 

Business Logic ➡ API Client ➡ requests ➡ HTTP

Business Logic 只调用: 

```python
get_device()

create_vlan()

delete_acl()
```

至于里面到底调用了 requests, 还是其他 HTTP Client 业务层完全不需要知道. 

## API Client 的职责

因此, 在 Enterprise Automation Platform 中, API Client 更适合承担以下职责: 

- 构造 HTTP Request

- 添加统一的 Headers

- 处理认证信息

- 设置 Timeout

- 发送请求

- 接收 Response

- 检查 Status Code

- 返回处理结果

而 Business Logic 继续保持只关注业务. 这与前面章节建立的 Layered Architecture 保持完全一致. 

与 SSH Automation 的对比现在可以发现, SSH 与 HTTP 的整体架构非常相似. 

| SSH Automation    | API Automation |
| ----------------- | -------------- |
| SSH Protocol      | HTTP Protocol  |
| Netmiko           | requests       |
| Connection Module | API Client     |
| Business Logic    | Business Logic |

虽然通信协议不同, 但是整个工程设计没有发生变化. 这正是我们一直强调的平台稳定, 通信方式可替换. 

## Engineering Insight

这里需要特别强调一个容易混淆的概念. 很多教程会说 "requests 就是 API. " 这种说法并不准确. 

实际上: 

HTTP API ➡ 通信规范 ➡ requests ➡ Python 工具

requests 并不会定义 API. 真正定义 API 的是服务器. requests 只是帮助客户端按照 HTTP 协议去访问这些 API. 

理解这一点, 有助于后续阅读不同厂商的 API 文档, 也能避免把某个 Python 库与协议本身混为一谈. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 什么是 HTTP Client? 

- 为什么 Python 不直接操作 TCP 来发送 HTTP 请求? 

- HTTP 与 requests 的关系是什么? 

- requests 与 Netmiko 在整个 Workbook 中分别承担什么角色? 

- 为什么 Business Logic 不应该直接调用 requests? 

- API Client 在 Enterprise Automation Platform 中应承担哪些职责? 

## Summary

本节建立了 Python HTTP Client 的工程定位: 

- HTTP: 通信协议. 

- requests: HTTP 的 Python 客户端库. 

- API Client: 平台中的通信组件, 统一管理 HTTP 请求. 

- Business Logic: 不直接依赖 requests, 而是通过 API Client 完成通信. 

至此, 我们已经完成了从 HTTP 协议 → HTTP 请求 → HTTP 响应 → JSON Payload → HTTP Client 的理论基础. 