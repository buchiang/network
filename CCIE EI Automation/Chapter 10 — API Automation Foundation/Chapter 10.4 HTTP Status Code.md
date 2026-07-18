很多教程都会把 HTTP Status Code 当成一张需要死记硬背的表格, 但从企业自动化的角度来看, 更重要的是理解: 

>Status Code 不是给人看的, 而是给程序做决策（Decision Making）的. 

Chapter 9 中, 我们通过 Parser 判断 CLI 输出是否符合预期；到了 API 自动化中, 我们首先会根据 Status Code 判断这次请求是否成功, 再决定是否继续后续流程. 

## Theory（理论）

当客户端发送一个 HTTP Request 后, 服务器不会只返回数据, 它还会返回一个 HTTP Status Code（HTTP 状态码）. 

Status Code 的作用是: 

>告诉客户端, 这次请求执行的结果. 

例如: 

- 请求是否成功? 

- 请求格式是否正确? 

- 是否需要身份认证? 

- 请求的资源是否存在? 

- 服务器是否发生异常? 

对于自动化程序来说, Status Code 是判断请求结果的第一依据. 

## Engineering Discussion

### 为什么需要 Status Code? 

假设没有 Status Code. 

客户端发送: GET /devices

服务器返回: {}

这时客户端无法判断这是因为: 

- 没有任何设备? 

- 查询失败? 

- 权限不足? 

- URL 写错? 

- 服务器内部异常? 

仅凭返回的数据, 很难判断真正发生了什么. 

因此, HTTP 协议规定: 

>服务器必须先返回一个状态码. 

例如: 200 OK

表示: 请求已经成功处理. 

或者: 404 Not Found, 表示: 请求的资源不存在. 

因此, 一个 HTTP Response 可以简化表示为: 

```
HTTP Response
│
├── Status Code
├── Headers
└── Body
```

其中, Status Code 永远是自动化程序首先关注的内容. 

## Status Code 的分类

HTTP 状态码采用三位数字, 真正重要的是第一位数字. 第一位数字决定了这一类状态码的含义. 

| 范围  | 含义                  |
| --- | ------------------- |
| 1xx | 信息（Informational）   |
| 2xx | 成功（Success）         |
| 3xx | 重定向（Redirection）    |
| 4xx | 客户端错误（Client Error） |
| 5xx | 服务器错误（Server Error） |

对于网络自动化来说真正需要重点掌握的是: 

- 2xx

- 4xx

- 5xx

1xx 和 3xx 在大多数 API 自动化场景中较少直接处理, 因此本章不深入展开. 

### 2xx —— Success（成功）

2xx 表示: 服务器已经成功处理请求. 

其中最常见的是: 200 OK

表示: 请求成功. 

例如: GET /devices

服务器: 200 OK

随后返回设备列表. 

这表示请求已经完成, 程序可以继续处理返回的数据. 

另一个常见状态码是: 201 Created

表示: 服务器成功创建了新的资源. 

例如: POST /interfaces

服务器: 201 Created

说明: Loopback Interface 已经成功创建. 

还有: 204 No Content

表示: 请求成功, 

但是没有返回任何数据. 

例如删除一个对象: DELETE /interfaces/Loopback100

服务器可能返回: 204 No Content

表示: 删除成功. 

只是没有内容需要返回. 

### 4xx —— Client Error（客户端错误）

4xx 并不是服务器坏了, 它表示客户端发送的请求存在问题. 也就是说服务器能够正常工作, 但是客户端请求不正确. 因此自动化程序首先应该检查自己. 

最常见的是: 400 Bad Request

表示: 请求格式错误. 

例如: JSON 格式不正确. 

或者: 缺少必须字段, 服务器无法解析请求. 

另一个非常重要的是: 401 Unauthorized

表示: 身份认证失败. 

例如: 用户名或 Token 错误. 

服务器不会执行请求. 这里需要注意401 表示尚未通过身份认证. 它通常意味着: 程序需要提供正确的认证信息. 

还有: 403 Forbidden

表示: 已经完成身份认证, 

但是: 没有权限执行当前操作. 

例如: 普通用户尝试删除系统配置. 服务器知道你是谁, 但拒绝执行, 这与 401 有本质区别. 

再来看: 404 Not Found

表示: 请求的资源不存在. 

例如: GET /devices/R100

而服务器只有: 

- R1

- R2

- R3

那么服务器可能返回: 404 Not Found

说明: URL 本身是正确的, 

但是目标资源不存在. 

## 5xx —— Server Error（服务器错误）

5xx 表示: 服务器在处理请求时发生了异常. 这里的问题通常不在客户端, 而是在服务器. 

例如: 500 Internal Server Error

表示: 服务器内部发生异常. 

可能是: 

- 软件 Bug

- 后端数据库异常

- 服务崩溃

- 未处理的程序错误

对于自动化程序来说, 通常应该: 

- 记录日志

- 重试（根据业务场景决定）

- 终止当前工作流或进入异常处理流程

而不是盲目继续执行. 

另一个常见状态码是: 503 Service Unavailable

表示: 服务暂时不可用. 

例如: 服务器正在维护. 

或者: 负载过高. 

这种情况往往是临时性的. 

与 500 不同, 503 在很多企业系统中适合结合有限次数的重试机制, 但具体的重试策略属于后续章节讨论的内容. 

## Status Code 与 Enterprise Workflow

回顾 Chapter 9. 我们当时是这样工作的: SSH ➡ CLI Output ➡ Parser ➡ Compliance

因为 CLI 没有统一的状态反馈, 所以必须先解析输出. 

而在 API 中第一步通常变成: 

HTTP Request ➡ Status Code ➡ Body ➡ Business Logic

也就是说只有当 Status Code 表明请求成功时, 程序才会继续处理 Body 中的数据. 这是一种更加稳定、更加标准化的工作流程. 

## Engineering Best Practice

在企业自动化开发中, 不建议: 发送请求 ➡ 直接解析返回数据

更推荐: 发送请求 ➡ 检查 Status Code ➡ 确认请求成功 ➡ 解析 Body ➡ 执行业务逻辑

原因很简单, 假设服务器返回 404 Not Found.

Body 中可能只有: 

```
{
    "error":"Device Not Found"
}
```

如果程序直接把它当作正常业务数据处理, 就可能产生错误的判断. 

因此先检查 Status Code, 再处理数据, 应当成为整个自动化平台的统一规范. 

## Engineering Insight

对于网络工程师来说, Status Code 可以理解为 CLI 世界中的命令是否执行成功, 但两者并不完全相同. 

CLI 通常依赖: 

- 输出内容

- 错误提示

- 关键字匹配

来判断执行结果. 

而 HTTP 提供了统一的状态反馈机制. 

这意味着自动化程序无需解析错误提示文本, 只需根据标准化的 Status Code, 就能快速决定下一步如何处理. 这也是 HTTP API 比 CLI 更适合程序自动化的重要原因之一. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- HTTP Status Code 的作用是什么? 

- 为什么程序应先检查 Status Code, 而不是直接解析返回数据? 

- 2xx、4xx、5xx 分别表示什么类型的结果? 

- 401 与 403 有什么区别? 

- 404 表示什么? 它一定意味着服务器不可用吗? 

- 为什么 5xx 错误通常意味着需要记录日志并进入异常处理流程? 

## Summary

本节建立了 HTTP Status Code 的工程模型: 

- 2xx: 请求成功, 可以继续处理返回数据. 

- 4xx: 客户端请求存在问题, 应检查请求内容、认证或资源路径. 

- 5xx: 服务器处理异常, 应进行日志记录和错误处理, 而不是继续执行业务逻辑. 

至此, 我们已经理解了 HTTP 通信中的两个核心元素: 

- Request: 客户端如何表达自己的请求. 

- Status Code: 服务器如何反馈请求结果. 