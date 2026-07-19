到这里，我认为 Chapter 10 已经完成了 Framework(框架)的设计. 

接下来应该开始真正讨论: 

>API Response Processing(API 响应处理)

很多初学者认为: `response.json()` 已经结束了. 实际上，这才是真正业务处理的开始. 

企业自动化项目中，大部分代码不是发送 HTTP Request，而是解析 API 返回的数据. 

因此，本节开始讨论: API Response Processing

## Theory

HTTP Response 可以分成两个部分: 

```
HTTP Response

├── Metadata
└── Payload
```

其中 Metadata 包括: 

- Status Code

- Headers

- Cookies

而真正的业务数据通常位于 Payload(响应内容). 

例如: 

```json
[
    {
        "id": 1,
        "title": "..."
    }
]
```

对于自动化工程来说真正有价值的是 Payload. 

## Engineering Discussion

目前 Service 写成: 

```python
response = api_client.get(endpoints.POSTS)

if response is None:
    return None

return response.json()
```

这里其实隐藏了两个步骤: 

HTTP Response ➡ JSON ➡ Python Object

注意 `response.json(): ` 并不是返回 JSON, 它返回的是 Python 数据结构. 

例如服务器返回: 

```json
{
    "hostname": "R1",
    "ip": "10.0.0.1"
}
```

经过 `response.json()` 以后得到的是: 

```python
{
    "hostname": "R1",
    "ip": "10.0.0.1"
}
```

这是 Python Dictionary, 而不是 JSON 字符串, 这一点要与 Chapter 6 保持一致. 

## API Payload ≠ Business Object

很多教程直接 `devices = response.json()`

然后认为已经得到业务对象, 严格来说还没有.

例如服务器返回: 

```python
{
    "hostname": "R1",
    "managementIp": "10.0.0.1",
    "serialNumber": "ABC123",
    "createdTime": "...",
    "lastUpdated": "...",
    "internalId": "..."
}
```

但是我们的 Workflow 可能真正需要: 

```python
{
    "hostname": "R1",
    "ip": "10.0.0.1"
}
```

很多字段只是平台内部字段, 并不是业务需要. 

## Service 的职责

因此 Service 除了调用 API, 还负责**数据整理(Data Transformation)**. 

例如: 

```python
def get_devices():

    response = api_client.get(endpoints.DEVICES)

    if response is None:
        return None

    devices = []

    for item in response.json():

        devices.append(
            {
                "hostname": item["hostname"],
                "ip": item["managementIp"]
            }
        )

    return devices
```

现在 Workflow 获得的是真正需要的数据, 而不是 API Server 的原始格式. 

## 为什么不要把原始 Payload 传到 Workflow? 

假设 Workflow 需要 `device["managementIp"]` 如果未来厂商升级 API: 

managementIp ➡ ipAddress

整个项目都会失效, 但是如果 Service 统一转换: 

```python
{
    "ip": item["managementIp"]
}
```

那么未来只需要修改Service, Workflow 完全不用改变. 

## Layered Architecture

现在数据流变成: 

HTTP Response ➡ SON Payload ➡ Service Transformation ➡ Business Object ➡ Workflow

注意 Workflow 永远不要依赖 Vendor API 的字段名称. 

## Engineering Analysis

这里体现了另一个重要原则: 

>隔离外部数据模型(External Data Model). 

API Server 返回的数据结构属于外部模型. 

Workflow 使用的数据结构属于内部模型. 

两者之间应该有 Service 作为转换层, 否则整个项目都会依赖外部平台的数据格式, 维护成本非常高. 

## Engineering Best Practice

企业项目通常建议: 

- API Client 返回 Response. 

- Service 完成 JSON 解析. 

- Service 将外部 Payload 转换为内部业务对象. 

- Workflow 只使用内部业务对象. 

- 不要让 Workflow 依赖厂商 API 的字段命名. 

这样可以有效降低厂商 API 变更带来的影响. 

## Engineering Insight

这一节完成了 API Automation 中最后一层解耦.

前面我们已经隔离了: 

- HTTP 通信. 

- Authentication. 

- Endpoint. 

- Configuration. 

现在我们进一步隔离了: **数据模型**, 也就是说即使未来: 

- API Endpoint 改变. 

- 字段名称改变. 

- 返回结构调整. 

只要 Service 保持输出一致, 整个 Workflow 都无需修改. 

这就是企业自动化平台中非常重要的一种能力: 

>屏蔽外部平台的变化，为上层提供稳定的数据模型. 

## Engineering Checklist

完成本节后，应能够回答以下问题: 

- response.json() 返回的是 JSON，还是 Python 对象? 

- 为什么 API Payload 不等于业务对象? 

- 为什么数据转换应由 Service 完成? 

- 为什么 Workflow 不应依赖厂商 API 的字段名称? 

- 什么是外部数据模型? 什么是内部数据模型? 

- Service 如何降低 API 升级带来的影响? 

## Summary

本节建立了 API Response Processing 的工程原则: 

- 将 API 返回的 JSON Payload 与业务对象明确区分. 

- 由 Service 完成 JSON 解析和数据转换. 

- 为 Workflow 提供稳定、统一的内部数据模型. 

- 将外部 API 的数据结构变化限制在 Service 层内部. 