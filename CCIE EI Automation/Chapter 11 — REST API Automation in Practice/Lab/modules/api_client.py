import requests
from modules.logger import logger
from modules import loader

config = loader.load_yaml("configs/api.yaml")

DEFAULT_TIMEOUT = config["timeout"]
VERIFY_SSL = config["verify_ssl"]
BASE_URL = config["base_url"]
AUTH_ENABLED = config["authentication"]["enabled"]
AUTH_TYPE = config["authentication"]["type"]
AUTH_TOKEN = config["authentication"]["token"]


session = requests.Session()

def _check_status(response):
    """
    Check the HTTP response status code.
    """
    return 200 <= response.status_code < 300

def _build_headers():
    """
    Build the headers for the HTTP request.
    """
    headers = {}

    if AUTH_ENABLED:

        if AUTH_TYPE == "Bearer":
            headers["Authorization"] = f"Bearer {AUTH_TOKEN}"

    return headers

def _request(method, endpoint, **kwargs):
    """
    Send an HTTP request using the specified method.
    """
    url = BASE_URL + endpoint

    logger.info(f"Sending {method} request to {url}")

    try:
        response = session.request(method, 
                                   url, 
                                   timeout=DEFAULT_TIMEOUT,
                                   verify=VERIFY_SSL,
                                   headers=_build_headers(), 
                                   **kwargs)
        
        logger.info(f"Response.status_code: {response.status_code}")

        if not _check_status(response):
            logger.error(f"Http Error: {response.status_code}")
            return None

        return response

    except requests.RequestException as error:
        logger.error(f"HTTP request failed: {error}")
        return None

def get(endpoint, params=None):
    """
    Send an HTTP GET request.
    """
    return _request("GET", 
                    endpoint,
                    params=params)

def post(endpoint, payload):
    """
    Send an HTTP POST request.
    """
    return _request("POST", 
                    endpoint, 
                    json=payload)