from modules.connection import (
    connect_device,
    disconnect_device,
    execute_show_command
)
import json

with open("inventory/devices.json", "r") as file:
    devices = json.load(file)

for device in devices:
    connection = connect_device(device)
    try:

        output = execute_show_command(
            connection,
            "show version"
        )
        print("=" * 60)
        print(f"CONNECTING TO DEVICE: {device['host']}".upper())
        print(f"\n{output}")
        print("=" * 60)

        disconnect_device(connection)
    except Exception as e:
        print(e)