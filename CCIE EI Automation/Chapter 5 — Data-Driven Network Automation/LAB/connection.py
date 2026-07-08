from netmiko import ConnectHandler

"""
import logging

logging.basicConfig(
    filename="automation/logs/automation.log",
    level=logging.INFO,
    format="%(asctime)s %(levlename)s %(message)s"
)
"""

def connect_device(device):
    try:
        connection = ConnectHandler(**device)
        connection.enable
        return connection
    except Exception as e:
        print(f"Failed to connect device {e}")
        #logging.error(e)

def ececute_show_command(connection, command):
    try:
        output = connection.send_command(command)
        return output
    except Exception as e:
        print(f"Failed to execute command: {e}")

def disconnect_device(connection):
    try:
        connection.disconnect()
    except Exception as e:
        print(f"Failed to disconnect from device: {e}")