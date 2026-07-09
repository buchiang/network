from inventory.devices import devices
from modules.connection import (connect_device, 
                                disconnect_device)
from modules.operations import send_config_set

commands = [
        "interface loopback100",
        "description Configured by Automation",
        ]

for device in devices:

    print("=" * 60)
    print(f"Connecting to {device['host']}")

    try:
        connection = connect_device(device)

        output = send_config_set(connection, commands)
        print(output)
        
        disconnect_device(connection)

    except Exception as error:
        print(f"FAILED: {device['host']}")
        print(error)