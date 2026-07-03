devices = [
    {
        "hostname": "R1",
        "host": "10.1.1.1"
    },
    {
        "hostname": "R2",
        "host": "10.1.1.2"
    },
    {
        "hostname": "R3",
        "host": "10.1.1.3"
    }
]

def connect(device):
    print(f"Connecting to {device['hostname']}")
    print(f"IP Address: {device['host']}")
    print("-" * 30)

for device in devices:
    connect(device)
                                  
                           