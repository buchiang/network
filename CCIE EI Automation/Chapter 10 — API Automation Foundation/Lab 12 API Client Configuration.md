到这里, `api_client.py` 的整体架构已经基本稳定. 接下来, 不应该立刻介绍 Bearer Token、Basic Authentication 或 Cisco DNA Center API. 

因为还有一个企业工程中必须解决的问题: 

>Configuration(配置管理)

目前我们的代码仍然存在大量"硬编码(Hard Coding)". 

例如: `DEFAULT_TIMEOUT = 10`

或者: `url = "https://jsonplaceholder.typicode.com/posts/1"`

这些配置写在代码里面, 对于实验没有问题, 但是对于企业项目来说, 这是一个明显的设计缺陷. 

因此, 本节开始讨论 API Client Configuration

## Theory(理论)

回顾前面的章节, Chapter 5 我们学习了 Data-Driven Automation 核心思想就是数据与程序分离. 

Chapter 6 我们又学习了 YAML, JSON

目的也是: 

>将可变化的数据放到外部. 

因此 Chapter 10 的 API Client, 应该继续遵循相同原则. 

## Engineering Discussion

### 什么属于配置? 

观察目前的代码. 

例如: `DEFAULT_TIMEOUT = 10` 它是不是业务逻辑? 

不是. 

是不是 HTTP 协议? 

也不是. 

它只是运行参数(Runtime Configuration)

同样: https://jsonplaceholder.typicode.com 也不是程序逻辑. 而是服务器地址. 因此它也属于 Configuration. 

### 什么不属于配置? 

例如: `response = session.request(...)` 这是程序行为. 属于 Business Logic. 不应该放入 YAML, 否则配置文件开始决定程序执行流程, 整个系统就会越来越难维护. 

因此我们需要区分: 

| 类型                | 是否属于 Configuration |
| ------------------ | ------------------ |
| Timeout            | Yes                |
| Base URL           | Yes                |
| Verify SSL         | Yes                |
| Default Headers    | Yes                |
| HTTP Method        | No                 |
| Request Workflow   | No                 |
| Exception Handling | No                 |

这也是企业项目中非常重要的边界. 

## Layered Architecture

现在配置开始加入系统. 

架构变成: 

```
Business Logic
        │
        ▼
API Client
        │
        ▼
Configuration
        │
        ▼
Session
        │
        ▼
HTTP
```

注意 Configuration 影响 API Client, 但是 Business Logic 不知道 Timeout 是多少. 

## Hands-on Lab

建立: 

```
automation_project/

config/

    api.yaml
```

例如: 

```yaml
timeout: 10

verify_ssl: true

base_url: https://jsonplaceholder.typicode.com
```

注意目前只有三个配置不要一次增加几十项, 保持简单. 

## 读取配置

回顾 Chapter 6 可以继续使用: `from modules import loader`

假设: Chapter 6 已经拥有统一 YAML Loader. 

那么 API Client 只需要: 

```python
config = loader.load_yaml(
    "config/api.yaml"
)
```

随后: 

```python
DEFAULT_TIMEOUT = config["timeout"]
VERIFY_SSL = config["verify_ssl"]
BASE_URL = config["base_url"]
```

可以发现 HTTP Client 已经不再依赖硬编码. 

## 为什么不是 Environment Variable? 

很多教程会说应该全部使用 Environment Variable. 

例如: 

```
API_TIMEOUT

API_SERVER

VERIFY_SSL
```

对于大型生产系统这是常见方案, 但是对于当前 Workbook 我们已经建立 YAML Configuration Framework. 

因此继续保持一致. 不要为了介绍一种新技术, 破坏整个课程的统一架构. 后续如果涉及部署环境, 再讨论 Environment Variable 的作用. 

## Workflow 的变化

现在请求流程变成: 

```
Configuration
        │
        ▼
API Client
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

Business Logic 仍然只有 

```python
response = api_client.get("/posts/1")
```

甚至 URL 都可以进一步简化. 

## Base URL

目前代码: 

```python
url = "https://jsonplaceholder.typicode.com/posts/1"
```

实际上每一次都重复: `https://jsonplaceholder.typicode.com`

因此 API Client 完全可以负责拼接. 

例如: 

```python
Business Logic: 

response = api_client.get(
    "/posts/1"
)
```

API Client 内部: 

```python
url = BASE_URL + endpoint
```

最终发送 `https://jsonplaceholder.typicode.com/posts/1`

Business Logic 开始真正脱离 HTTP 地址. 以后服务器迁移. 

例如: 

api.company.com ➡ api2.company.com

只需要修改配置文件. 

整个项目无需修改代码. 

## Engineering Analysis

这里实际上体现了前几章一直强调的一句话: 

>变化的东西放到配置, 不变化的东西放到代码. 

观察目前所有内容变化的: 

- Timeout

- Base URL

- SSL Verification

固定的: 

- Request Engine

- Status Validation

- Exception Handling

- Logging Workflow

这种划分让整个 API Client 既灵活, 又稳定. 

## Engineering Best Practice

一个成熟的 API Client 通常会把以下内容作为配置项: 

- Base URL

- Timeout

- SSL Verification

- 默认请求头(后续章节)

- 默认认证方式(后续章节)

而请求生命周期、异常处理、日志记录等通信流程, 应保持在代码中实现, 而不是交给配置文件控制. 

## Engineering Insight

到这里, api_client.py 已经完成了从"代码示例"到"可配置通信模块"的演进. 

整个模块已经具备了三个明显的企业特征: 

```
API Client

├── Stable Public Interface
├── Centralized Communication Logic
└── Externalized Configuration
```

这三者共同决定了模块的可维护性. 

未来如果企业需要: 

- 更换 API Server. 

- 调整 Timeout. 

- 修改 SSL 策略. 

都可以通过配置完成, 而无需修改业务代码或请求流程. 

这正是前面 Chapter 5 与 Chapter 6 所建立的数据驱动思想, 在 API Automation 中的自然延续. 

## Engineering Checklist

完成本节后, 应能够回答以下问题? 

- 为什么 Timeout 应属于配置, 而不是业务逻辑? 

- 哪些内容适合放入配置文件? 哪些不适合? 

- 为什么 Base URL 应集中管理? 

- 为什么本 Workbook 当前阶段继续采用 YAML, 而不是 Environment Variable? 

- "变化的东西放到配置, 不变化的东西放到代码" 在 API Client 中是如何体现的? 

- 引入配置后, Business Logic 获得了哪些好处? 

## Summary

本节为 `api_client.py` 引入了统一配置管理: 

- 将 Timeout、Base URL、SSL Verification 等运行参数从代码中剥离. 

- 复用前面章节建立的 YAML 配置框架, 保持整个 Workbook 的一致性. 

- 让 API Client 成为一个可配置、可扩展的通信模块, 而不是依赖硬编码的示例程序. 

至此, `api_client.py` 已经具备了企业级 HTTP Client 的核心组成部分: **统一接口、共享 Session、统一请求引擎、集中通信策略以及外部配置管理**. 下一节将在这一基础上引入Authentication(认证), 说明如何在不破坏现有架构的前提下, 为所有请求统一添加认证信息. 