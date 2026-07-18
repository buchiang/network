实际上，Logging 不应该只是"打印信息", 它应该与 Chapter 8 建立的日志体系保持一致. 这样，整个 Enterprise Automation Platform 才只有一套 Logging Architecture. 

## Theory

目前，我们的 `api_client.py` 已经具备: 

- Send Request

- Communication Exception

- Status Code Validation

- Timeout

但是整个通信过程仍然是不可观察(Unobservable)的. 

例如程序失败以后,我们不知道: 

- 请求发送到了哪个 URL? 

- 使用了什么 Method? 

- 请求什么时候发生? 

- 返回了什么 Status Code? 

- 请求耗时多久? 

如果没有日志这些信息都会丢失. 

## Previous Chapter Review

回顾 Chapter 8, 当时我们建立了统一日志模块. 

例如: 

```
modules/

    logger.py
```

所有业务模块: 

```
Deployment

Compliance

Inventory
```

都通过 `logger.info(...)` 记录运行信息, Chapter 10 不应该重新设计日志. HTTP Communication 也应该使用同一套 Logging Framework. 

## Engineering Discussion

### 为什么不能使用 print()? 

目前 API Client 仍然有 `print(f"HTTP Error: {response.status_code}")` 虽然可以工作, 但是企业项目几乎不会这样做. 

原因有很多, 例如程序后台运行时 `stdout` 可能根本没人看. 

另外 `print` 没有:

- Timestamp

- Log Level

- Module Name

因此无法用于生产环境. 

### HTTP Log 应记录什么? 

很多初学者喜欢记录整个 Response. 

例如 `print(response.text)` 实际上真正有价值的是通信信息. 

例如: 

```
GET

https://server/api/devices

200
```

这些信息能够帮助工程师快速定位通信是否成功. 至于业务数据属于   Business Logic, 不应该全部写入 Communication Log. 

## Logging Scope

建议 API Client 只记录通信信息. 

例如: 

```
Timestamp

Method

URL

Status Code

Result
```

而不是: 

```
JSON Payload

Business Data

Configuration

Device Inventory
```

这样日志职责保持单一. 

## Hands-on Lab

首先导入 Chapter 8 的 Logger `from modules.logger import logger`

修改: 

```python
def get(url):
    try:

        logger.info(f"HTTP GET {url}")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT
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

POST保持一致 `logger.info(f"HTTP POST {url}")`

随后记录: 

```python
logger.info(
    f"HTTP Response {response.status_code}"
)
```

保持统一格式. 

## 为什么记录两次? 

有人可能觉得只记录 200 是不是够了? 实际上一次请求包含两个重要事件. 

第一, 请求发送 `GET /devices`

第二, 服务器响应 `200`

如果第二条日志没有出现, 说明请求可能超时. 或者程序异常退出. 

因此请求响应分别记录, 更容易排查问题. 

## Layered Architecture

现在完整的数据流变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ├── Write Request Log
        ├── Apply Timeout
        ├── Send Request
        ├── Handle Exception
        ├── Validate Status
        ├── Write Response Log
        └── Return Response
```

可以看到 Logging 属于 Communication Layer. 

Business Layer 无需重复记录 HTTP. 

## Engineering Analysis

目前 API Client 已经承担: 

Communication Strategy ➡ Logging ➡ Exception Handling ➡ Status Validation ➡ Timeout

Business Logic 越来越简单. 

例如: 

```python
response = api_client.get(url)

if response:
    devices = response.json()
```

整个 HTTP 生命周期已经完全封装. 

## 这正是 Layered Architecture 带来的价值. 

为什么暂时不记录 Response Body? 

很多教程喜欢 `logger.info(response.text)` 但是企业项目通常不会默认这样做. 

原因包括: 

第一, Response Body 可能非常大. 

例如: 几百 KB, 甚至几十 MB. 

第二, Body 可能包含敏感信息. 

例如: Token, Password, API Key. 

第三, 绝大多数通信故障只需要 Method, URL, Status Code 即可定位. 

因此默认 Communication Log 应保持精简. 真正需要分析业务数据时再由 Business Logic 根据需要记录. 

## Engineering Best Practice

通信日志建议保持统一格式. 

例如: 

```
INFO HTTP GET https://server/api/devices

INFO HTTP Response 200

ERROR HTTP Request Failed:
Connection timed out

ERROR HTTP Error 404
```

这种格式便于: 

- 阅读. 

- 搜索. 

- 后续导入日志分析平台. 

更重要的是整个项目都保持一致. 

## Engineering Insight

到目前为止，我们已经完成了一个典型企业 HTTP Client 的五项核心能力: 

```
API Client

├── Request
├── Timeout
├── Exception Handling
├── Status Validation
└── Logging
```

注意这里没有增加任何业务功能, 我们一直在完善通信能力. 这正体现了 Workbook 一直强调的思想: 

>优秀的基础模块，不是因为功能复杂，而是因为它把所有共性的能力都集中管理，并以稳定, 统一的接口提供给整个系统. 

未来加入认证(Authentication), Session, 重试(Retry)等能力时，仍然会沿着这一思路继续扩展，而不需要修改任何业务模块. 

## Engineering Checklist

完成本节后，应能够回答以下问题: 

- 为什么 API Client 应使用统一的 Logger，而不是 print()? 

- 为什么请求日志和响应日志应分别记录? 

- Communication Log 应记录哪些信息? 

- 为什么默认不记录完整的 Response Body? 

- Logging 属于 Communication Layer 还是 Business Layer? 

- 当前 API Client 已经集中管理了哪些通信能力? 

## Summary

本节将 Logging 纳入了 api_client.py 的统一职责: 

- 复用了 Chapter 8 建立的统一日志体系. 

- 在请求发送和响应返回两个关键节点记录日志.

- 将日志内容聚焦于通信信息，而非业务数据. 

- 保持 Logging, Timeout, Exception, Status Validation 等通信策略全部集中在 API Client 中. 

至此，api_client.py 已经具备了一个企业级 HTTP 通信模块的基础框架. 接下来，我们将进一步引入Session(会话管理)，解决每次请求重复建立连接的问题，为后续学习认证机制和企业 API 平台打下基础. 