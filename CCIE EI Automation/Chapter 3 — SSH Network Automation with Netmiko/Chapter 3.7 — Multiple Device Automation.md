# Learning Objectives

完成本课后，你应该能够：

- 理解为什么企业自动化必须支持多设备管理。

- 使用一个脚本连接多台 Cisco IOSv。

- 将 Chapter 2 学习的 List、Dictionary 和 for 循环应用到真实 Cisco 自动化场景。

- 理解"数据驱动（Data-Driven）"自动化的基本思想。

**本课目标不是增加新的 Netmiko API，而是将前面已经学习的知识组合起来，解决一个新的工程问题。**

### Problem

假设公司有三台 Router：

| Device | Management IP |
| ------ | ------------- |
| R1     | 10.10.10.11   |
| R2     | 10.10.10.12   |
| R3     | 10.10.10.13   |

如果挨个手工 SSH 费时费力, 增加配置错误可能性, 如果设备数量增加到50台路由器, 100台交换机呢?

自动化的目标就是 **相同的操作，只写一次代码。**

### 从"设备"到"设备集合"

前面的课程中，我们只有一台设备：

```python
device = {
    "device_type": "cisco_ios",
    "host": "10.10.10.11",
    "username": "admin",
    "password": "cisco123",
}
```

这是一台设备。现在需要管理三台设备。根据 Chapter 2 已学习的知识，一个自然的表示方式就是：

```
List
│
├── Device 1 (Dictionary)
├── Device 2 (Dictionary)
└── Device 3 (Dictionary)
```

也就是说一个 List 中保存多个 Device Dictionary。

![](image/3.2-0.png)

## Cisco Implementation

首先定义三台设备。

```python
r1 = {
    "device_type": "cisco_ios",
    "host": "12.1.1.1",
    "username": "admin",
    "password": "cisco123",
}

r2 = {
    "device_type": "cisco_ios",
    "host": "12.1.1.2",
    "username": "admin",
    "password": "cisco123",
}

r3 = {
    "device_type": "cisco_ios",
    "host": "23.1.1.3",
    "username": "admin",
    "password": "cisco123",
}
```

然后：

```python
devices = [
    r1,
    r2,
    r3,
]
```

到这里为止，没有新的 Python 知识。全部来自 Chapter 2：

- Dictionary

- List

## 使用 for 循环

现在开始真正的自动化。`for device in devices:` 这句话表示依次取出 List 中的每一台设备。

然后 `connection = ConnectHandler(**device)` 每循环一次就连接一台 Router。

## 完整程序

```python
from netmiko import ConnectHandler

r1 = {
    "device_type": "cisco_ios",
    "host": "12.1.1.1",
    "username": "admin",
    "password": "cisco123",
}

r2 = {
    "device_type": "cisco_ios",
    "host": "12.1.1.2",
    "username": "admin",
    "password": "cisco123",
}

r3 = {
    "device_type": "cisco_ios",
    "host": "23.1.1.3",
    "username": "admin",
    "password": "cisco123",
}

devices = [
    r1,
    r2,
    r3,
]

for device in devices:

    connection = ConnectHandler(**device)

    output = connection.send_command("show version")

    print(output)

    connection.disconnect()
```

整个程序只写了一次：

```python
ConnectHandler()
send_command()
disconnect()
```

却完成了三台 Router 的自动化。

# Troubleshooting

| 现象                 | 原因                 | 检查方法                    |
| ------------------ | ------------------ | ----------------------- |
| 第一台成功，第二台失败        | 第二台设备不可达或认证失败      | 单独使用 OpenSSH 验证第二台      |
| 所有设备失败             | 程序或网络环境存在共同问题      | 回到 Lesson 3.3 检查 SSH 基础 |
| 输出混乱               | 连续打印多个设备结果，不易区分    | 后续课程将增加设备标识输出           |
| 存在未关闭的 SSH Session | 未执行 `disconnect()` | 使用 `show users` 验证      |

## Engineering Notes

目前程序能够工作，但还有一个工程问题。运行后，终端会连续打印三个 show version 输出。

如果三台设备运行不同 IOS 版本很难判断哪一段输出属于哪一台设备。

这是程序第一次暴露出可读性（Readability的问题。

在企业开发中程序不仅要能够运行。还要能够让工程师快速理解输出结果。因此，在下一课，我们将学习如何组织自动化输出，使结果更加清晰、便于分析。