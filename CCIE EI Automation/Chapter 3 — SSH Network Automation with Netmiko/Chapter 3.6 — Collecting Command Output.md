# Learning Objectives

完成本课后，你应该能够：

- 使用变量保存多个 Cisco CLI 输出。

- 理解为什么自动化程序需要保存命令输出，而不仅仅是打印输出。

- 根据不同的业务需求组织多个命令的返回结果。

- 为下一步配置备份做好准备。

本课重点是"采集（Collect）"命令输出，而不是"处理（Parse）"命令输出。

如何分析和解析 CLI 输出将在后续章节介绍。

**打印（Print）只是验证。保存（Collect）才是自动化的目标。**

## Cisco Implementation

下面的程序连续采集两条命令。

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

注意：

这里出现了两个变量 `version` 以及 `interfaces`

它们分别保存不同命令的输出。这样做的目的不是方便打印。而是方便后续继续使用。

# Troubleshooting

| 现象            | 原因        | 解决方法                   |
| ------------- | --------- | ---------------------- |
| 第二条输出覆盖第一条    | 重复使用同一个变量 | 为不同命令使用不同变量            |
| 输出内容与 CLI 不一致 | 命令输入错误    | 手工执行相同命令验证             |
| 两个变量内容完全相同    | 两次执行了相同命令 | 检查 `send_command()` 参数 |
