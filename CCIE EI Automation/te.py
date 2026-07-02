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