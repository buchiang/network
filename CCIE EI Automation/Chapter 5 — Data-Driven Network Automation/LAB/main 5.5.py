from inventory.devices import devices
from modules.connection import connect_device
from modules.connection import disconnect_device

for device in devices:

    print("=" * 60)
    print(f"Connecting to {device['host']}")

    connection = connect_device(device)

    output = connection.send_command("show version")

    print(output)

    disconnect_device(connection)