from modules import api_client
from modules import endpoint

def create_posts(payload):
    """
    Create a new post via the API.
    """
    response = api_client.post(endpoint.POSTS, payload)

    if response is None:
        return None

    return response.json()

def get_post():

    response = api_client.get(endpoint.GET_POST)

    if response is None:
        return None
    
    return response.json()