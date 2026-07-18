import requests


def get(url):
    """
    Send an HTTP GET request.

    Args:
        url (str): API endpoint.

    Returns:
        requests.Response: HTTP response object.
    """
    return requests.get(url)


def post(url, payload):
    """
    Send an HTTP POST request.

    Args:
        url (str): API endpoint.
        payload (dict): Request payload.

    Returns:
        requests.Response: HTTP response object.
    """
    return requests.post(url, json=payload)