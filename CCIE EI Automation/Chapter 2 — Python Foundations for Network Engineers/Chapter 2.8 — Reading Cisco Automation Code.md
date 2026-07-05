
# Cisco 官方风格（简化版）

先看一段代码，不要求全部理解：

```
from netmiko import ConnectHandler #从 Netmiko 模块导入 ConnectHandler。

device = {
    "device_type": "cisco_ios",
    "host": "10.1.1.1",
    "username": "admin",
    "password": "Cisco123"
}

conn = ConnectHandler(**device)

output = conn.send_command("show version")

print(output)

conn.disconnect()
```

`**` 的真正含义是：

将 Dictionary 展开为关键字参数（Keyword Arguments）。

这是 Python 中一个非常重要的语法，以后不仅 Netmiko，很多第三方库都会使用。