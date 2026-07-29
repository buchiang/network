from modules import inventory_service

posts = inventory_service.get_post()

if posts is None:
    print("Failed to retrieve posts from the API.")
else:
    print("=" * 50)
    print(f"Retrieved {len(posts)} posts from the API.")
    print("=" * 50)

    print(f"\nTitle: {posts['title']}")
    print(f"\nBody: {posts['body']}")