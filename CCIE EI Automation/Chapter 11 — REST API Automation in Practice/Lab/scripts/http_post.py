from modules import inventory_service

payload = {
    "title": "Automation Workbook",
    "body": "Chapter 10",
    "userId": 1
}

post = inventory_service.create_posts(payload)

print("=" * 50)

for key, value in post.items():
    print(f"{key}: {value}\n")

print("=" * 50)