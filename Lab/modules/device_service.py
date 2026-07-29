from modules import api_client
from modules import endpoint

def get_devices(hostname=None):

    params = {}

    if hostname is not None:
        params["hostname"] = hostname

    response = api_client.get(
        endpoint.DEVICE,
        params=params
    )

    if response is None:
        return None

    return response.json()


def creat_device(device):
    payload = {
        "hostname": device["hostname"],
        "managementIP": device["ip"]
    }
    response = api_client.post(endpoint.DEVICE, payload)

    if response is None:
        return None

    return response.json()

