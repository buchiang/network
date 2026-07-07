from netmiko import ConnectHandler
#设备信息
devices = {
    "device_type": "cisco_ios", 
    "host": "10.1.1.1",
    "username": "admin",
    "password": "cisco123",
    "secret": "cisco123",
}

connection = ConnectHandler(**devices)

try:
    #进入特权模式
    connection.enable()
except Exception as e:
    print(f"进入特权模式失败: {e}")
    connection.disconnect()
    exit()
    