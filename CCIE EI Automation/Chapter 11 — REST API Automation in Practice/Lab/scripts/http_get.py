from modules import api_client
from modules import inventory_service

posts = inventory_service.get_post()

if posts is not None:
    print("=" * 50)

    for key, value in posts.items():
        print(f"{key}: {value}\n")

    print("=" * 50)

else:
    print("Failed to retrieve data from the API.")

