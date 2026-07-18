## Theory

在上一节中, 我们知道一个 HTTP Request 的第一部分就是 Method. 

Method 用来告诉服务器: 

>客户端希望执行什么操作. 

HTTP 协议定义了多种 Method. 

不过, 对于网络自动化工程师来说, 真正需要掌握的主要有以下几种: 

- GET

- POST

- PUT

- PATCH

- DELETE

它们几乎覆盖了绝大多数企业 API 的使用场景. 

## Engineering Discussion

为什么需要 Method? 假设没有 Method, 会发生什么? 

例如: `https://controller.company.com/interfaces`

服务器只能知道客户端访问了 interfaces, 但是服务器不知道客户端到底想干什么. 

例如是不是: 

- 查询接口? 

- 创建接口? 

- 删除接口? 

- 修改接口? 

同一个 URL, 可以执行很多不同的操作. 因此 HTTP 使用 Method 来表达动作(Action). 

于是: GET /interfaces

表示: 获取接口信息. 

而: POST /interfaces

表示: 创建新的接口. 

URL 不变, 动作发生变化, 这就是 Method 存在的意义. 

## GET

GET 的作用, GET 表示: 

>读取(Read)资源. 

GET 不应该修改服务器上的数据, 它只是请求服务器返回已有的信息. 

例如: GET /interfaces

可以理解成: 请把所有接口信息返回给我. 

或者: GET /devices

表示: 获取设备列表. 

对于网络工程师来说, GET 最接近 CLI 中的 `show`

例如: 

```
show version

show ip interface brief

show inventory
```

这些命令都是读取信息, 不会修改设备. 因此在自动化中, 大量的查询操作都会使用 GET. 

### GET 的工程特点

GET 通常具有以下特点: 

- 不修改数据

- 可以重复执行

- 主要用于查询

- 返回服务器已有的数据

因此 GET 非常适合: 

- Inventory 查询

- Compliance 数据获取

- 状态检查

- 监控系统

- Dashboard

## POST

POST 表示: 

>创建(Create)新的资源. 

例如 POST /interfaces 并不是读取接口, 而是创建一个新的 Interface. 服务器真正的数据放在 Body. 

例如: 

```
{
    "name": "Loopback100",
    "ip": "10.100.100.1"
}
```

服务器收到以后创建新的资源. 因此 POST 更接近企业中的 Provisioning. 

### POST 的工程特点

POST 通常: 

- 创建资源

- 提交数据

- 可能产生新的对象

- 服务器状态发生变化

因此 POST 不适合无限重复执行. 

因为: 

第一次, 创建成功. 

第二次, 可能会创建第二个对象. 

或者服务器返回 `Already Exists`. 

## PUT

PUT 表示: 

>整体替换(Replace)资源. 

例如服务器原来保存 

```
Interface

Name = Loopback0

Description = Old

IP = 1.1.1.1
```

客户端发送 PUT: 

```
Name = Loopback0

Description = New

IP = 2.2.2.2
```

服务器通常会认为用新的内容替换整个对象. 而不是只修改 Description. 因此 PUT 更像重新提交整个配置. 

### PUT 的工程特点

PUT 通常: 

- 更新整个对象

- 完整覆盖资源

- 客户端发送完整内容

因此如果遗漏字段, 服务器可能会把遗漏内容删除, 这一点需要特别注意. 

## PATCH

PATCH 与 PUT 很容易混淆. 

PATCH 表示: 局部修改(Partial Update). 

例如原来的配置: 

```
Hostname = R1

Location = DC1

Owner = Network Team
```

如果只想修改 Location. 

PATCH 可以发送 Location = DC2

服务器只修改 Location. 

其他字段保持不变. 

因此 PATCH 更接近日常运维中的修改一个配置项. 而不是重新提交整个配置. 

## PUT 与 PATCH 的区别

这是企业面试中经常出现的问题, 举一个简单例子. 

假设服务器保存: 

```
{
    "hostname":"R1",
    "location":"DC1",
    "owner":"Network"
}
```

PUT: 

```
{
    "hostname":"R1"
}
```

服务器可能认为整个资源就是 hostname 另外两个字段被覆盖掉. 

而 PATCH: 

```
{
    "hostname":"R2"
}
```

服务器通常理解为只修改 hostname, 其他内容保持不变. 

因此 PUT 是 Replace, PATCH 是 Update, 这是最大的区别. 

## DELETE

DELETE 表示删除资源. 

例如: `DELETE /interfaces/Loopback100`

表示删除: Loopback100. 

服务器执行完成后资源消失. 

对于网络工程来说 DELETE 往往对应: 

- 删除对象

- 删除策略

- 删除接口

- 删除 ACL

- 删除配置项

因此 DELETE 操作通常需要更加谨慎. 

## CRUD 思维

在企业开发中, 经常会看到一个术语: 

>CRUD. 

它表示四种最基本的数据操作. 

| Operation | HTTP Method |
| --------- | ----------- |
| Create    | POST        |
| Read      | GET         |
| Update    | PUT / PATCH |
| Delete    | DELETE      |

可以发现 HTTP Method 与 CRUD 几乎是一一对应的. 因此很多 API 文档都会按照 CRUD 来组织. 理解 CRUD, 也就理解了绝大多数 HTTP API 的基本设计. 

## HTTP Methods 与 CLI 的思维差异

在 CLI 中, 我们通常通过不同的命令表达不同的动作: 

`show running-config`

`interface Loopback0`

`no interface Loopback0`

每条命令都包含了: 

- 操作

- 对象

而在 HTTP 中动作与对象被分离. 

例如 GET /interfaces

动作是: GET. 

对象是: interfaces. 

或者 DELETE /interfaces/Loopback0

动作: DELETE. 

对象: Loopback0. 

这种设计使 API 更加统一, 也便于程序自动生成和处理请求. 

## Engineering Insight

对于有 CLI 背景的网络工程师来说, 最大的思维转变之一就是不要把 HTTP Method 理解成命令. 

Method 并不是命令名称, 它表达的是操作语义(Operation Semantics). 

真正的业务对象由 URL 指定, 而 Method 只是说明"对这个对象执行什么操作". 

这种动作(Method)与资源(Resource)分离的设计, 是现代 HTTP API 能够保持一致性和可扩展性的关键原因. 

后续无论学习 Cisco、VMware、AWS 还是其他平台的 API, 你都会不断看到这种模式. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- 为什么 HTTP 需要 Method, 而不能只依赖 URL? 

- GET 与 POST 的职责分别是什么? 

- PUT 与 PATCH 的本质区别是什么? 

- 为什么 DELETE 操作通常需要更加谨慎? 

- CRUD 与 HTTP Method 是如何对应的? 

- 为什么说 Method 表达的是操作, 而不是资源? 

## Summary

本节建立了 HTTP Method 的核心工程模型: 

- GET: 读取资源, 不修改服务器状态. 

- POST: 创建新的资源, 通常会新增对象. 

- PUT: 整体替换资源, 提交完整内容. 

- PATCH: 局部更新资源, 仅修改指定字段. 

- DELETE: 删除资源, 需要谨慎使用. 

从这一节开始, 我们已经能够理解绝大多数 API 文档中的请求语义. 下一节将继续学习 HTTP Status Code(HTTP 状态码), 理解服务器如何通过状态码反馈请求的执行结果, 以及自动化程序应如何根据不同状态进行处理. 