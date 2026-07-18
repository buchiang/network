## Theory

上一节我们学习了 HTTP Method. 

Method 决定我要做什么, 但是服务器仍然不知道我要操作什么. 

例如：GET

仅仅说明：读取数据, 但是读取：

- 哪个设备? 

- 哪个接口? 

- 哪个 VLAN? 

- 哪个用户? 

这些信息由 URL 提供. 

因此：

> 一个完整的 HTTP Request 至少需要回答两个问题：

我要做什么?  ➡ Method ➡ 我要操作什么? ➡ URL

Method 与 URL 共同决定了一次请求的含义. 

## Engineering Discussion

### URL 的作用

URL（Uniform Resource Locator, 统一资源定位符）的作用非常简单告诉服务器, 请求发送到哪里. 

例如：`https://controller.company.com/devices`

表示：客户端希望访问 devices 这一类资源. 

如果：`https://controller.company.com/interfaces`

那么请求的对象变成了 interfaces

可以发现 Method 决定动作, URL 决定对象, 二者缺一不可. 

## 从网络工程师的角度理解 URL

回忆一下 CLI, 我们通常这样操作：`show ip interface brief` 这里实际上包含了两个信息：

第一：动作 show

第二：对象 ip interface

CLI 把动作, 对象写在一条命令里面, 而 HTTP 将它们进行了分离. 

例如：GET ➡ /interfaces

动作：GET

对象：interfaces. 

这种设计更加规范, 也是现代 API 的基本思想. 

## 什么是 Resource（资源）? 

Resource 是整个 API 世界最重要的概念之一. 

可以简单理解成：API 所管理的对象. 

例如一个网络控制器可能管理：

- Device

- Interface

- VLAN

- ACL

- User

- Policy

这些都是 Resource. 

注意 Resource 不是一个命令, 而是一个对象. 

例如：

Device 就是一种 Resource. 

Interface 也是一种 Resource. 

## Resource 与 CLI 的区别

CLI 更关注如何操作. 

例如：

```
show interface

configure terminal

interface GigabitEthernet0/0
```

API 更关注操作哪个对象. 

例如：/interfaces

表示：接口资源. 

而：/acl

表示：ACL 资源. 

这种设计意味着不同的操作可以作用于同一个 Resource. 

例如：GET /interfaces 读取接口. 

POST /interfaces 创建接口. 

DELETE /interfaces/Loopback0 删除接口. 

可以发现真正变化的是 Method. 

Resource 一直都是 interfaces. 

## Endpoint（接口端点）

很多 API 文档都会反复出现 Endpoint. 

例如：

```
GET /devices

POST /devices

GET /interfaces
```

每一个都可能被称为一个 Endpoint. 从工程角度, 可以把 Endpoint 理解为服务器提供的一个可访问接口. 

例如：

/devices 就是一个 Endpoint. 

/interfaces 也是一个 Endpoint. 

客户端可以向这些位置发送请求. 

服务器会根据：

```
Method

URL
```

共同决定执行什么操作. 

## URL 与 Endpoint 的关系

很多初学者会把 URL, Endpoint 认为完全一样. 实际上它们并不是同一个概念. 

例如：`https://controller.company.com/api/v1/interfaces`

完整的是 URL

而 `/api/v1/interfaces`

通常称为 API Endpoint. 

也就是说 Endpoint 更强调服务器暴露出来的 API 接口, URL 更强调客户端访问资源所使用的完整地址, 在很多日常交流中, 两者经常混用, 但理解它们的侧重点, 有助于阅读正式的 API 文档. 

## 一个完整请求是如何定位资源的? 

现在, 我们已经具备了三个核心概念：

Method ➡ Resource ➡ Endpoint

例如：

GET ➡ /devices 

表示：读取所有 Device Resource. 

如果 GET ➡ /devices/R1

则表示：读取编号为 R1 的 Device Resource. 

如果 DELETE ➡ /devices/R1

则表示：删除 R1

因此 Method 决定做什么, URL / Endpoint 决定作用于哪个 Resource. 

## Engineering Architecture

站在 Enterprise Automation Platform 的角度来看, HTTP Request 可以进一步抽象成：

Business Logic ➡ Operation ➡ Method ➡ Resource ➡ Endpoint ➡ HTTP Request

例如：

Business Logic 获取所有设备

最终可以转换为：GET ➡ /devices

Business Logic 删除接口

最终可以转换为：DELETE ➡ /interfaces/Loopback0

注意业务逻辑描述的是"我要完成什么业务"; HTTP Request 描述的是"如何向服务器表达这个业务". 

这是 Layered Architecture 的体现：上层关注业务, 下层关注通信细节. 

## Engineering Insight

阅读 API 文档时, 不要先看代码示例, 而应先识别三个问题：

- Resource 是什么? 

- 这个 Resource 对应哪些 Endpoint? 

- 每个 Endpoint 支持哪些 Method? 

只要回答了这三个问题, 就已经理解了一个 API 的基本结构. 

不同厂商的 API 在命名和组织方式上会有所差异, 但这种围绕 Resource + Method 的设计思想在现代 HTTP API 中非常普遍. 

## Engineering Checklist

完成本节后, 应能够回答以下问题：

- URL 在 HTTP Request 中承担什么职责? 

- Resource 与 CLI 中的命令有什么区别?

- Endpoint 可以如何理解? 

- URL 与 Endpoint 的侧重点有什么不同? 

- 为什么同一个 Resource 可以对应多个不同的 Method? 

- 如何从 Business Logic 映射到 HTTP Request? 

## Summary

本节建立了 HTTP API 中用于定位操作对象的核心概念：

- URL：客户端访问资源的完整地址. 

- Endpoint：服务器暴露出的可访问 API 接口. 

- Resource：API 所管理的业务对象, 如 Device、Interface、VLAN 等. 

至此, 我们已经理解了一个 HTTP Request 的三个关键组成部分：

- Method：执行什么操作. 

- URL / Endpoint：操作哪个资源. 

- Resource：被操作的业务对象. 