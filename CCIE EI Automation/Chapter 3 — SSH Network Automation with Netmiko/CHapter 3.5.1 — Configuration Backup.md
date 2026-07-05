# Learning Objectives

完成本课后，你应该能够：

- 理解为什么配置备份是网络自动化中最基础的生产任务。

- 使用 Netmiko 自动获取 Cisco IOS 配置。

- 利用 Chapter 2 已学习的文件操作，将配置保存到本地。

- 验证备份文件是否完整、可读。

本课只关注配置备份（Backup），不会修改任何设备配置。

## Cisco Implementation

获取配置

建立连接后：

```
running_config = connection.send_command(
    "show running-config"
)
```

此时 `running_config` 保存的是完整的 Cisco 配置。

## 保存到文件

Chapter 2 已学习文件操作。

因此可以直接使用：

```
with open("R1_running.cfg", "w") as file:
    file.write(running_config)
```

这里没有引入新的 Python 知识，只是把前面学过的 File 操作应用到 Cisco 自动化场景。

## 完整程序

```
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "12.1.1.1",
    "username": "admin",
    "password": "cisco123",
}

connection = ConnectHandler(**device)

running_config = connection.send_command(
    "show running-config"
)

with open("R1_running.cfg", "w") as file:
    file.write(running_config)

connection.disconnect()

print("Configuration backup completed.")
```

# Troubleshooting

| 现象    | 原因                          | 检查方法               |
| ----- | --------------------------- | ------------------ |
| 文件为空  | `show running-config` 未成功执行 | 手工执行命令验证           |
| 文件未生成 | 文件写入失败                      | 检查程序运行目录           |
| 配置不完整 | CLI 输出异常                    | 手工比较 CLI 与备份文件     |
| 认证失败  | SSH 登录失败                    | 回到 Lesson 3.3 验证连接 |

## Engineering Notes

企业环境中，配置备份至少需要满足三个要求：

1. 完整性

备份必须包含完整 Running Configuration，而不是部分输出。

2. 可恢复性

备份文件应保持原始 CLI 格式，便于恢复或比较。

3. 可重复执行

同一个脚本每天运行，都应能够稳定完成备份，而不会影响设备运行。

本课先实现最基础的单设备备份。后续在多设备自动化中，我们将进一步扩展为批量备份多个 Cisco IOSv 设备。