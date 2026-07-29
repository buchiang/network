from modules import device_service

device = {
    "hostname":"R1",
    "ip": "10.0.0.1"
}
result = device_service.creat_device(device)

try:
    print(result)

except Exception as e:
    print(f"Unable to retrieve inventory: \n\t{e}\n")