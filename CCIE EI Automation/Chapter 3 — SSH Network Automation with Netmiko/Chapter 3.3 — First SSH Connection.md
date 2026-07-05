
# Learning Objectives

完成本课后，你应该能够：

- 理解为什么 Netmiko 使用 ConnectHandler() 建立 SSH 连接。

- 使用 Netmiko 成功登录 Cisco IOSv。

- 理解设备信息为什么使用 Dictionary 保存。

- 正确关闭 SSH 连接。

- 能够验证 SSH Session 是否成功建立和释放。

本课只关注 SSH 连接的建立与关闭。

命令执行`（send_command()）`将在下一课介绍

Netmiko 是专门面向网络设备的 SSH 自动化库。

对于 Cisco IOS，它负责：

- 建立 SSH 连接

- 完成身份认证

- 建立 CLI 会话

- 返回可操作的连接对象

本课只关注前三步。

## ConnectHandler()

Netmiko 使用统一的入口函数 `ConnectHandler()` 建立 SSH 连接。连接建立成功后，它会返回一个连接对象。

整个过程如下：

```
Python Script
⬇
ConnectHandler()
⬇
SSH Authentication
⬇
Cisco IOS CLI
⬇
Connection Object
```

后续所有自动化操作，都将基于这个连接对象完成。

## Why

为什么 Netmiko 不直接要求用户输入：

- IP

- 用户名

- 密码

而是使用一个 Dictionary？

例如：

```
device = {
    "device_type": "cisco_ios",
    "host": "10.10.10.11",
    "username": "admin",
    "password": "cisco123",
}
```

原因很简单。一个网络设备本身就是由多个属性组成：

```
Cisco Device
├── Device Type
├── IP Address
├── Username
└── Password
```

Dictionary 非常适合描述这种键值关系。随着课程深入，还会增加新的设备属性，因此这种表示方式具有良好的扩展性。

## Cisco Implementation

### Step 1

创建文件：first_login.py

### Step 2

编写代码：

```
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "10.10.10.11",
    "username": "admin",
    "password": "cisco123",
}

connection = ConnectHandler(**device)

print("SSH connection established.")

connection.disconnect()

print("SSH connection closed.")
```

本课只出现两个新的 Netmiko 接口：

- `ConnectHandler()`

- `disconnect()`

其余内容均为 Chapter 2 已掌握的 Python 知识。

## Code Analysis

按照程序执行顺序分析：

### 第一步

```
device = {
    ...
}
```

这里只是在内存中创建一个 Dictionary。

此时：

- 没有建立 TCP 连接

- 没有建立 SSH 连接

- 没有访问 Cisco Router

### 第二步

`connection = ConnectHandler(**device)`

程序开始建立 SSH 连接。如果认证成功返回一个连接对象，并赋值给 `connection` 以后所有自动化操作都会使用这个对象。

### 第三步

`connection.disconnect()` 主动关闭 SSH Session。程序结束前释放连接，是良好的工程实践。
