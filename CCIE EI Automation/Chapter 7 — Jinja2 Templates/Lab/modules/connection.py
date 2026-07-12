from netmiko import ConnectHandler

def conect_device(device):
    try:
        connection = ConnectHandler(**device)
        connection.enable
        return connection
    except Exception as e:
        print(f"Failed to connect device {e}")
        raise

def execute_show_command(connection, command):
    try:
        output = connection.send_command(command)
        return output
    except Exception as e:
        print(f"Failed to excute command: {e}")
        raise

def disconnect_device(connection):
    try:
        connection.disconnect()
    except Exception as e:
        print(f"Failed to disconnect from device "{e})
        raise
    