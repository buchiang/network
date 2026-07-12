from inventory.devices import devices
from modules.connection import (connect_device, 
                                disconnect_device,
                                execute_show_command
)
from modules.operations import send_config_set

commands = [
    "show version",
    "show ip interface brief",
    "show ip route",
        ]

for device in devices:

    print("=" * 60)
    print(f"Connecting to {device['host']}")

    try:
        connection = connect_device(device)

        for command in commands:

            output = execute_show_command(connection, command)
            print(f"\nCommand: {command}")
            print("-" * 50)
            print(output)
            print("-" * 50)

        disconnect_device(connection)

    except Exception as error:
        print(f"FAILED: {device['host']}")
        print(error)