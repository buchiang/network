devices = [
    {
        "hostname": "R1",
        "host": "10.10.10.1"
    },
    {
        "hostname": "R2",
        "host": "12.1.1.2"
    },
    {
        "hostname": "R3",
        "host": "23.1.1.3"
    }
]

for device in devices:
    print(f"Connecting to {device['hostname']}")
    print(f"IP Address: {device['host']}")
    print("-" * 30)