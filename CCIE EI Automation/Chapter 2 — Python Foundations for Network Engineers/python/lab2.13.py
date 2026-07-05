hostname = "R1"

config = f"""
hostname {hostname}

interface Loopback0
 ip address 1.1.1.1 255.255.255.255
"""

with open(
    "R1.cfg",
    "w"
) as file:

    file.write(config)

print("Backup Finished")