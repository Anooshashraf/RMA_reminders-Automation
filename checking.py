import json

with open("RMA_Screenshots/_group_list.json", "r") as f:
    content = f.read()
    print("First 500 characters of JSON:")
    print(content[:500])