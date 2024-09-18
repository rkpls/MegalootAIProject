import os
import json
    
class DataManager:
    
    def load_json(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def save_temporary(id, item_data):
        db_path_temp = "data/temp.json"
        try:
            db_temp = DataManager.load_json(db_path_temp)
            if db_temp is None:
                db_temp = {}
        except Exception as e:
            print(f"[ERROR] Failed to load {db_path_temp}: {str(e)}")
            db_temp = {}
        db_temp[str(id)] = item_data
        try:
            with open(db_path_temp, 'w') as file:
                json.dump(db_temp, file, indent=4)
            print(f"[INFO] Temporary data for id {id} saved to {db_path_temp}")
        except Exception as e:
            print(f"[ERROR] Failed to write to {db_path_temp}: {str(e)}")
        
    def save_permanent(item_data):
        try:
            path = "data/items.json"
            db = DataManager.load_json(path)
            if db is None:
                db = {}
            item_id = item_data.get('id')
            db['items'] = [item for item in db['items'] if item.get('id') != item_id]
            db['items'].append(item_data)
            with open(path, 'w') as file:
                json.dump(db, file, indent=4)
            print(f"[INFO] Data written to {path}")
        except Exception as e:
            print(f"[ERR] Failed to write to {path}: {str(e)}")

    def reset_temp_file():
        path = "data/temp.json"
        empty_json = {{"id": i} for i in range(32)}
        with open(path, 'w') as json_file:
            json.dump(empty_json, json_file, indent=4)
            print("[INFO] New temporary Dataset created")

    def get_equipped():
        data = DataManager.load_json("data/temp.json")
        equipped_items = [item for item in data['items'] if 0 <= item['id'] <= 7 and 'name' in item]
        return len(equipped_items)

    def get_inventory():
        data = DataManager.load_json("data/temp.json")
        inventory_items = [item for item in data['items'] if 8 <= item['id'] <= 27 and 'name' in item]
        return len(inventory_items)

    def value_equipped():
        data = DataManager.load_json("data/temp.json")
        equipped_items_value = sum(item['value'] for item in data['items'] if 0 <= item['id'] <= 7 and 'value' in item)
        return equipped_items_value

    def value_inventory():
        data = DataManager.load_json("data/temp.json")
        inventory_items_value = sum(item['value'] for item in data['items'] if 8 <= item['id'] <= 27 and 'value' in item)
        return inventory_items_value
