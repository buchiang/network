fl = [
      {'name':'jen',
       'language': 'python'},
      {'name': 'sarah',
       'language': 'c'},
      {'name': 'edward',
      'language': 'ruby'},
      {'name': 'phil',
       'language': 'python'},
    
        ]
device = []

for item in fl:

    device.append(
        {"host": item["name"],
         "ip": item["language"]}
    )

for d in device:
    for k, v in d.items():
        print(k, v)