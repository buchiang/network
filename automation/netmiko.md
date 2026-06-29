netmiko 是一个 Python 的三方模块, 封装了常见网络设备的 SSH 管理功能

支持多种网络设备厂商 

提供简单的接口, 便于发送命令, 获取配置等操作

# 安装

CMD 或 powershell

```
pip install netmiko
```

## 验证

```
import netmiko

from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios", 
    "host": "192.168.1.1",
    "username": "admin",
    "password": "admin123",
    "sercet": "enable123", 
    "port": 22
}
```

## 建立 SSH

connect = ConnectHandle(**device)

connection.enable() 进入enable模式

output = connection.send_command("show ip interface brief")

print("设备返回结果")

print(output)

## 断开

connection.disconncet()

