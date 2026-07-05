# Learning Objectives

完成本课后，你应该能够：

- 理解 send_command() 的作用。

- 使用 Netmiko 自动执行 Cisco Show Command。

- 获取 Cisco CLI 返回的数据。

- 理解为什么 show 命令适合作为自动化的第一步。

本课只学习 Show Command。

不涉及配置修改（Configuration Mode），这是后续课程的内容。

## 第一个 Show Command

```
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "12.1.1.1",
    "username": "admin",
    "password": "cisco123",
}

connection = ConnectHandler(**device)

output = connection.send_command("show version")

print(output)

connection.disconnect()
```

相比上一课，只增加了一条新的 Netmiko API：

`connection.send_command()`

其它内容保持不变。

## Code Analysis

程序按照下面顺序执行。

### 第一步

建立 SSH：

`connection = ConnectHandler(**device)`

成功后建立一个 SSH Session。

### 第二步

执行：

```
output = connection.send_command(
    "show version"
)
```

发生了什么？


```
Python
↓
SSH Session
↓
Cisco CLI
↓
执行：show version
↓
Cisco 返回结果
↓
保存到变量 output
```

注意这里 `output`是一个 String。这并不是新的 Python 知识。Chapter 2 已经学习过 String 可以保存任意文本。这里保存的是 Cisco CLI 输出。

### 第三步

打印 `print(output)` Python 将整个字符串显示到终端。

### 第四步

关闭连接 `connection.disconnect()` 程序结束。

# Troubleshooting

| 现象                    | 原因      | 检查方法               |
| --------------------- | ------- | ------------------ |
| 没有输出                  | SSH 未建立 | 回到 Lesson 3.3 检查连接 |
| Timeout               | 网络问题    | `ping`、OpenSSH     |
| Authentication Failed | 用户认证失败  | 手工 SSH 登录          |
| 输出为空                  | 命令输入错误  | 手工验证命令是否存在         |
