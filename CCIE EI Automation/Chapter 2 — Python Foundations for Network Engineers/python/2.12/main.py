from connection import connect

devices = [
    {
        "hostname": "R1"
    },
    {
        "hostname": "R2"
    }
]

for device in devices:

    connect(device)