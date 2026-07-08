from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "12.1.1.1",
    "username": "admin",  
    "password": "cisco123",
    "secret": "cisco123",
}

def connect_device(device):
    connection = ConnectHandler(**device)
    connection.enable()
    return connection

def execute_show_command(connection, command):
    output = connection.send_command(command)
    return output

def disconnect_device(connection):
    connection.disconnect()

connection = connect_device(device)

output = execute_show_command(connection, "show ip interface brief")
print(output)

disconnect_device(connection)