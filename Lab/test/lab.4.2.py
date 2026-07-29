from netmiko import ConnectHandler

# 设备信息
device = {
    "device_type": "cisco_ios",
    "host": "12.1.1.1",
    "username": "admin",
    "password": "cisco123",
    "secret": "cisco123",
}

def connect_device(devices):
    connection = ConnectHandler(**devices)
    connection.enable()
    return connection

def excute_show_command(connection, command):
    output = connection.send_command(command)
    return output

def disconnect_device(connection):
    connection.disconnect()

connection = connect_device(device)


while True:
    command = input("Enter the command ('q' for Exit):\n")
    try:
        if command != "q":
            print(excute_show_command(connection, command))
        else:
            disconnect_device(connection)
            break
    except Exception as e:
        print(f"The problem is {e}")

