import json

class ItemManager:
    def __init__(self, json_file_path):
        with open(json_file_path, 'r') as f:
            self.items_data = json.load(f)['items']

    def get_item_stats(self, item_name):
        for item in self.items_data:
            if item['name'].lower() == item_name.lower():
                return item
        return None

    def upgrade_item(self, item_name):
        # Logic to check if upgrade is possible and return success
        item_stats = self.get_item_stats(item_name)
        if item_stats:
            print(f"Upgrading {item_name}...")
        else:
            print(f"Item {item_name} not found!")

