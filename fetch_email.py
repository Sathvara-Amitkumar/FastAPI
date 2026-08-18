import json

with open("app/data/products.json") as f:
    data = json.load(f)

unique_email = []
for idx in data:
    item = idx['seller']['email'].split("@")[-1]
    print(item)

    if item in unique_email:
        continue
    unique_email.append(item)

print(unique_email)
print(len(unique_email))