# Learning Objectives

完成本课后，你应该能够：

- 理解为什么 Netmiko 使用 Dictionary 描述设备。

- 理解 Device Dictionary 中每个字段的作用。

- 理解 **device 的含义（基于 Chapter 2 已学的 Dictionary 与 Function）。

- 为后续单设备和多设备自动化做好准备。

本课仍然不会执行任何 CLI 命令。

本课只解决一个问题：如何正确描述一台网络设备。

上一课，我们使用了下面这段代码：

```python
device = {
    "device_type": "cisco_ios",
    "host": "10.10.10.11",
    "username": "admin",
    "password": "cisco123",
}
```
随后：

`connection = ConnectHandler(**device)`

能够成功建立 SSH 连接。很多教程到这里就结束了。但是，一个企业网络工程师应该继续思考：

- 为什么不用四个独立变量？

- 为什么不是 List？

- 为什么不是 Tuple？

- Dictionary 到底解决了什么问题？

理解这一点，对于后面的多设备自动化至关重要。

### 一台 Cisco 设备有哪些信息？

从网络工程的角度，一台设备至少包含以下信息：

| 属性          | 示例            |
| ----------- | ------------- |
| Device Type | `cisco_ios`   |
| IP Address  | `10.10.10.11` |
| Username    | `admin`       |
| Password    | `cisco123`    |

这些信息都具有一个共同特点, 每个值都有明确的名称。

例如：

- 10.10.10.11 本身并不能说明它是什么。

- 只有配合 host，程序才知道这是设备地址。

因此，用 Key → Value 的方式描述设备最自然。

### 为什么不用 List？

假设写成：

```python
device = [
    "cisco_ios",
    "10.10.10.11",
    "admin",
    "cisco123",
]
```

程序还能运行吗？也许可以自己写代码解析。但是阅读时 `device[2]` 你必须回忆 Index 2 是用户名还是密码？可读性很差。

### Dictionary 的优势

Dictionary：

```python
device = {
    "host": "10.10.10.11",
}
```

阅读时立即知道这是主机地址。代码的可读性远高于 `device[1]` 企业代码首先服务于阅读代码的人。不仅仅是 Python 解释器。

## Cisco Implementation

本课继续使用上一课的 Device Dictionary：

```python
device = {
    "device_type": "cisco_ios",
    "host": "10.10.10.11",
    "username": "admin",
    "password": "cisco123",
}
```

下面逐个分析字段。

### device_type

`"device_type": "cisco_ios"`

表示目标设备运行 Cisco IOS。Netmiko 会根据这个值选择对应的连接方式。

目前课程统一使用 "cisco_ios" 后续学习其他平台时，再介绍其他类型。

### host

`"host": "10.10.10.11"`

表示管理地址。这里填写的是 Ubuntu 能够访问的管理 IP。

不是：

- Loopback

- Router ID

- Hostname

而是实际建立 SSH 所使用的 IP。

### username

`"username": "admin"`

用于 SSH 身份认证。应与 Cisco 本地用户或 AAA 用户保持一致。

### password

`"password": "cisco123"`

用于 SSH 登录认证。实验阶段采用硬编码，便于专注学习 SSH 连接。后续课程将逐步演进到更安全的凭据管理方式。

## `**device` 是什么意思？

上一课出现了：

`ConnectHandler(**device)`

这里不引入新的 Python 语法，只利用 Chapter 2 已经学习的：

- Function

- Dictionary

可以这样理解：

`ConnectHandler()` 需要多个命名参数。而 device 正好保存了一组命名参数。

`**device` 的作用就是：

把 Dictionary 中的键和值作为函数参数传递给 ConnectHandler()。

因此，我们只需要维护一个 Device Dictionary，而不用一个一个写参数。后续随着设备信息增加，这种方式仍然保持一致。

## Troubleshooting

| 修改内容             | 预期现象              | 原因           |
| ---------------- | ----------------- | ------------ |
| 错误 IP            | 超时                | 无法建立 TCP/SSH |
| 错误用户名            | 认证失败              | SSH 身份认证失败   |
| 错误密码             | 认证失败              | SSH 身份认证失败   |
| 错误 `device_type` | Netmiko 无法按预期驱动设备 | 驱动类型与平台不匹配   |
