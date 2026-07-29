from modules import device_service

devices = device_service.get_devices(
    hostname="R1"
)
"""
因为 hostname="R1", 所以在 get_device 里 hostname 就不再是 None, 
params 字典变为 {'Hostname': 'R1'}, API_client 里 
response = api_client.get(endpoint.DEVICE,params={"Hostname": "R1"}
request 会自动转换生成 GET /devices?hostname=R1 来补全 URL
"""
try:
    for device in devices:
        print(device)

except Exception as e:
    print(f"Unable to retrieve inventory: \n\t{e}\n")