Theory

在上一节中, 我们已经知道, 一个 HTTP Request 主要包含四个组成部分: 

```
HTTP Request
│
├── Method
├── URL
├── Headers
└── Body
```

Method 决定做什么, URL 决定操作哪个资源, 那么Headers 又负责什么? 答案是描述这次通信, 而不是描述业务. 这是理解 HTTP Header 最重要的一句话. 

## Engineering Discussion

### Header 的职责

可以把 Header 理解成请求的元数据(Metadata). 它不会告诉服务器创建哪个接口. 也不会告诉服务器接口 IP 地址是多少. 

这些属于业务数据(Business Data). Header 负责的是告诉服务器, 如何理解这次请求. 

例如: 

- 数据是什么格式? 

- 客户端希望接收什么格式的数据? 

- 身份认证信息是什么? 

- 是否启用压缩? 

- 使用什么语言? 

这些信息都属于 Header. 

一个生活中的例子

假设我们要寄一个包裹. 包裹里面放的是: 

- Loopback0

- IP Address

- Description

这些就是真正的业务数据, 而快递单上写的是: 

- 寄件人

- 收件人

- 联系电话

- 是否加急

这些并不是包裹里面的内容, 它们只是帮助快递公司完成运输, HTTP Header 的作用与此类似, 它不是业务内容, 而是帮助服务器正确处理请求. 

## Header 与 Body 的职责划分

这是企业开发中非常重要的一条原则. 

可以简单总结为: 

| Header   | Body          |
| -------- | ------------- |
| 描述通信     | 描述业务    |
| Metadata | Business Data |
| 请求如何处理   | 请求处理什么        |

例如: 假设我们希望创建一个新的 Interface. 

真正的接口信息: 

```
Interface = Loopback100

IP = 10.1.1.1

Description = Management
```

应该放在 Body, 而不是 Header. 

如果告诉服务器我是 JSON 格式. 

这属于 Header. 因为它描述的是数据格式. 而不是接口配置. 

## 为什么要区分 Header 与 Body? 

很多初学者会问既然都是发送给服务器, 为什么还要分两个地方? 

原因在于职责不同. 

例如: 服务器收到请求以后, 首先需要回答我应该如何解析这些数据? 

如果不知道数据到底是什么格式, 服务器甚至无法读取真正的数据. 

因此 Header 通常会先被处理. 随后服务器再解析 Body. 

整个流程可以表示为: 

HTTP Request ➡ 读取 Headers ➡ 确定通信方式 ➡ 解析 Body ➡ 执行业务逻辑

因此 Header 更接近通信层, Body 更接近业务层. 

## 常见 Header 类型

虽然 HTTP Header 有很多种, 但对于自动化工程师来说, 最常见的几类只有以下几种. 

### Content-Type

Content-Type 告诉服务器请求体(Body)采用什么数据格式. 

例如: 后续章节中, 我们会大量使用: application/json

表示: Body 是 JSON. 

服务器收到以后, 就会按照 JSON 进行解析. 

如果: Content-Type 与实际数据格式不一致, 服务器可能无法正确处理请求. 

### Accept

Accept 表示客户端希望服务器返回什么格式的数据. 

例如: 客户端可以告诉服务器请返回 JSON. 

服务器如果支持, 就会按照请求的格式返回数据. 

这里要注意: 

- Content-Type 描述的是"我发送给你的数据是什么格式". 

- Accept 描述的是"我希望你返回给我的数据是什么格式". 

它们分别对应请求和响应, 职责不同. 

### Authorization

很多企业 API 都需要身份认证. 

客户端需要告诉服务器我是谁. 

这类认证信息通常放在 Authorization Header. 

至于: 

- 用户名密码

- Token

- 其他认证机制

不同平台实现不同, 本章只建立概念. 具体认证方式将在后续章节结合实际 API 介绍. 

## Header 在 Enterprise Automation Platform 中的位置

回到我们的平台架构. 

Business Logic: 创建 Device 并不会关心 Header 如何构造. 它只关心
业务. 真正负责组织 HTTP Request 的, 应该是 Connection Layer. 

例如: 

Business Logic ➡ Connection Layer ➡ Method ➡ URL ➡ Headers ➡ Body

可以看到 Header 属于通信层的一部分, 而不是业务逻辑的一部分. 

这与前面一直强调的 Business Logic Separation 完全一致. 

如果未来认证方式发生变化, 

例如: Token 更新, 或者需要增加新的 Header, 理论上 Business Logic 不需要修改, 只需要调整 Connection Layer 的实现即可. 

## Engineering Best Practice

在企业项目中, 不建议让业务代码到处拼接 Header. 

例如: 

```python
#不推荐(示意)

create_device()

↓

手动添加 Authorization

↓

手动添加 Content-Type

↓

发送请求
```

更合理的做法是由 Connection Layer 统一负责构建 Header. 

业务模块只描述我要完成什么业务. 

这样可以避免

- 重复代码

- Header 不一致.

- 认证方式分散

- 后期维护困难

这种职责划分, 与我们在 Chapter 8 和 Chapter 9 中建立的工程思想保持一致. 

## Engineering Insight

对于网络工程师来说, 可以把 Header 理解为通信协议的配置, 而不是网络设备的配置. 配置设备接口、ACL、路由等属于业务数据, 应放在 Body 中, 而认证方式、数据格式、压缩方式等属于通信行为, 应放在 Header 中. 这种区分不仅符合 HTTP 协议的设计原则, 也有助于保持自动化平台各层职责清晰. 

## Engineering Checklist

完成本节后, 应能够回答以下问题: 

- Header 的职责是什么? 

- 为什么说 Header 描述的是通信, 而不是业务? 

- Header 与 Body 的职责有什么区别? 

- Content-Type 与 Accept 分别表示什么? 

- Authorization Header 的作用是什么? 

- 为什么 Header 应由 Connection Layer 统一管理, 而不是由 Business Logic 自行构造? 

## Summary

本节建立了 HTTP Header 的工程模型: 

- Header: 承载请求的元数据(Metadata), 描述通信方式. 

- Body: 承载真正的业务数据(Business Data). 

- Content-Type: 声明请求体的数据格式. 

- Accept: 声明客户端期望的响应格式. 

- Authorization: 携带身份认证信息. 

到目前为止, 我们已经完整理解了一个 HTTP Request 的四个组成部分: 

- Method: 执行什么操作. 

- URL / Endpoint: 操作哪个资源. 

- Headers: 如何进行通信. 

- Body: 传递什么业务数据. 