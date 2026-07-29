from netmiko import ConnectHandler

def connect_device(device):
    """
    Establish an SSH connection to a network device
    """
    try:
        connection = ConnectHandler(**device)
        connection.enable() #if device doesn't enable secret, can be deleted 
        return connection
    except Exception as e:
        print(f"Failed to connect device {e}")
        raise #only for reporting error 

def disconnect_device(connection):
    """
    Disconnect from the network device.
    """
    try:
        connection.disconnect()
    except Exception as e:
        print(f"Failed to disconnect from device {e}")
        raise
    