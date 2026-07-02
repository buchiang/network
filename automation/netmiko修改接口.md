
```
from netmiko import ConnectHandler
#设备信息

devices = {
    "device_type": "cisco_ios",
    "host": "192.168.1.1",
    "username": "admin",
    "password": "admin",
    "secret": "enablepasword",
}

#接口信息

interface = "GigabitEthernet0/1"
ip_address = "192.168.100.1"
subnet_mask = "255.255.255.0"

#配置接口IP命令

commands = [
    f"interface {interface}",
    f"ip address {ip_address} {subnet_mask}",
    "no shutdown"
]

try:
    #连接到设备
    connection = ConnectHandler(**devices)
    #进入特权模式
    connection.enable()
    #发送配置命令
    output = connection.send_config_set(commands)

    print("配置结果:")
    print(output)

except Exception as e:
    print(f"连接或配置失败: {e}")


# 验证配置

show_output = connection.send_command(f"show run int {interface}")

print("接口配置验证:")
print(show_output)

#断连
connection.disconnect()
```

```
user@ubuntu22-desktop:~$ python3 modi_int.py
配置结果:
configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
R1(config)#interface Ethernet0/2
R1(config-if)#ip address 192.168.100.1 255.255.255.0
R1(config-if)#no shutdown
R1(config-if)#end
R1#
接口配置验证:
Building configuration...

Current configuration : 123 bytes
!
interface Ethernet0/2
 ip address 192.168.100.1 255.255.255.0
 ip nat inside
 ip virtual-reassembly in
 duplex auto
end
```

同样在路由器上能看到 `Jul  2 08:04:05.215: %SYS-5-CONFIG_I: Configured from console by admin on vty0 (10.10.10.100)`

