# Learning Objectives

完成本课后，你应该能够：

- 理解 `send_command()` 的工作流程。

- 理解为什么 `send_command()` 返回的是一个 String。

- 理解 Python 与 Cisco CLI 之间的数据流。

- 理解为什么一次 SSH 连接可以连续执行多个 Show Command。

- 为后续采集设备信息做好准备。

本课重点不是学习新的 Cisco 命令。

本课重点是理解 `send_command()` 的工作机制。

## Cisco Implementation

下面的程序与上一课相比，只增加了一条 Show Command。

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "12.1.1.1",
    "username": "admin",
    "password": "cisco123",
}

connection = ConnectHandler(**device)

version = connection.send_command("show version")

interfaces = connection.send_command("show ip interface brief")

print(version)

print(interfaces)

connection.disconnect()
```

注意**整个程序只建立了一次 SSH。**但是执行了两条命令。

# Troubleshooting

| 现象            | 原因          | 检查方法                    |
| ------------- | ----------- | ----------------------- |
| 第一条命令成功，第二条失败 | 第一条命令后连接已断开 | 检查是否提前调用 `disconnect()` |
| 第二条命令输出异常     | CLI 命令输入错误  | 手工执行相同命令验证              |
| 两条命令都失败       | SSH 未建立     | 回到 Lesson 3.3 验证连接      |
