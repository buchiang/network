from inventory.devices import devices
from modules.connection import connect_device
from modules.connection import disconnect_device
from modules.operations import collect_show_version

for device in devices:

    print("=" * 60)
    print(f"Connecting to {device['host']}")

    try:
        connection = connect_device(device)

        output = collect_show_version(connection)

        print(output)

        disconnect_device(connection)

    except Exception as error:
        print(f"FAILED: {device['host']}")
        print(error)