from inventory.devices import devices
from modules.connection import connect_device
from modules.connection import disconnect_device
from modules.connection import ececute_show_command

for device in devices:
    print(f"Connecting to {device['host']}") #暂时使用
    connection = connect_device(device)
    #output = ececute_show_command(connection, "show ip int br")
    #print(f"\n{output}")
    #print("-" * 30)
    disconnect_device(connection)
    print(f"Disconnected from {device['host']}")#暂时使用