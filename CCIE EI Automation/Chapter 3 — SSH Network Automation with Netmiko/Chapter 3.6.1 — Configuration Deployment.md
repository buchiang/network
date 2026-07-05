# Learning Objectives

完成本课后，你应该能够：

- 理解为什么配置下发比 Show Command 风险更高。

- 使用 Netmiko 自动下发 Cisco IOS 配置。

- 理解 `send_config_set()` 的作用。

- 验证配置是否成功生效。

- 理解为什么自动化部署必须先验证，再修改。

**本课的目标不是学习复杂配置，而是建立安全的配置部署流程。**

Netmiko 提供了专门的配置接口 `sned.config_set()` 不必使用 `connection.send_command()`

并且 `sned.config_set()` 负责

- 自动进入 Configuration Mode

- 顺序发送配置命令

- 自动退出 Configuration Mode

因此**读取设备使用 `send_command()`，修改设备使用 `send_config_set()`。**

## Cisco Implementation

配置内容本课使用一个风险较低的实验。

创建 Loopback0, IP：1.1.1.1/32

配置命令：

```
commands = [
    "interface Loopback0",
    "ip address 1.1.1.1 255.255.255.255",
    "description Created by Netmiko",
]
```

这里再次应用了 Chapter 2 学习过的 List。每一个元素就是一条 Cisco CLI 配置命令。

### 下发配置

建立 SSH 后 `connection.send_config_set(commands)` 即可完成整个配置过程。

### 完整程序

```
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "10.10.10.11",
    "username": "admin",
    "password": "cisco123",
}

commands = [
    "interface Loopback0",
    "ip address 1.1.1.1 255.255.255.255",
    "description Created by Netmiko",
]

connection = ConnectHandler(**device)

connection.send_config_set(commands)

connection.disconnect()

print("Configuration deployment completed.")
```

# Troubleshooting

| 现象           | 原因                                           | 检查方法                                         |
| ------------ | -------------------------------------------- | -------------------------------------------- |
| Loopback 未创建 | 配置命令未成功执行                                    | 手工逐条输入配置验证                                   |
| SSH 成功但配置未变化 | 使用了 `send_command()` 而不是 `send_config_set()` | 检查代码                                         |
| 配置报错         | Cisco CLI 语法错误                               | 手工在设备上验证命令                                   |
| 再次运行脚本出现错误   | Loopback0 已存在，配置与当前状态冲突                      | 查看 `show running-config interface Loopback0` |


## Engineering Notes

本课还有一个重要的工程实践。

很多初学者喜欢把配置写成一个长字符串：

`commands = "interface Loopback0\nip address 1.1.1.1 255.255.255.255"`

虽然某些情况下可以工作，但不利于维护。

更推荐使用：

```
commands = [
    "interface Loopback0",
    "ip address 1.1.1.1 255.255.255.255",
    "description Created by Netmiko",
]
```

原因：

- 每个列表元素对应一条 Cisco CLI 命令。

- 修改、增加或删除配置时更加清晰。

- 更符合后续批量生成配置的方式。

因此，在本 Workbook 中，send_config_set() 的输入统一采用 List。