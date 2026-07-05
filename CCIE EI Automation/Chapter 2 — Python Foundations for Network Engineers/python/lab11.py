devices = [
    {
        "hostname": "R1"
    },
    {
        "hostname": "R2"
    },
    {
        "hostname": "R3"
    }
]

for device in devices:

    try:

        print(f"Connecting {device['hostname']}")

        if device["hostname"] == "R2":
            raise Exception("SSH Authentication Failed")

        print("Success")

    except Exception as e:

        print(f"Failed: {e}")

    print("-" * 30)