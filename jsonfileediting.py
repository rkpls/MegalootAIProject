import json

# Load the JSON file
with open('data/uncommonitems.json', 'r') as file:
    data = json.load(file)

# Iterate over the items and update the ID field
for index, item in enumerate(data["items"], start=1):
    item["price"] = index + 137 

# Save the updated JSON back to the file
with open('data/uncommonitems.json', 'w') as file:
    json.dump(data, file, indent=4)

print("IDs updated successfully!")
