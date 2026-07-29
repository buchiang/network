import automation.logs.test.devices as devices
from netmiko import ConnectHandler

def conncet_device(device):
    connection = ConnectHandler(**device)
    connection.enable
    return connection

def execute_show_command(connection, command):
    output = connection.send_command(command)
    return output

def disconnect_device(connection):
    connection.disconnect()

connection = conncet_device(device=devices)