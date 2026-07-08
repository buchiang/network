from netmiko import ConnectHandler
import logging

logging.basicConfig(
    filename="logs/automation.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

devices = {
    "device_type": "cisco_ios", 
    "host": "10.1.1.1",
    "username": "admin",
    "password": "cisco123",
    "secret": "cisco123",
}

try:
    connection = ConnectHandler(**devices)
    connection.enable()
except Exception as e:
    logging.error(e) #THE NEW FUNCTION
    print(e)
    connection.disconnect()
    exit()