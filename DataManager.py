import os
import json
    
class DataManager:
    
    def load_json(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def save_temporary(id, icon_data):
        db_path_temp = "data/temp.json"
        try:
            db_temp = DataManager.load_json(db_path_temp)
        except FileNotFoundError:
            db_temp = {}

        db_temp[str(id)] = icon_data

        with open(db_path_temp, 'w') as file:
            json.dump(db_temp, file, indent=4)
        
    def save_permanent(id, icon_data):
        try:
            path = "data/items.json"
            with open(path, 'w') as file:
                json.dump(id, icon_data, file, indent=4)
                print(f"[INFO] Data written to {path}")
        except Exception as e:
            print(f"[ERROR] Failed to write to {path}: {str(e)}")
            
    def reset_temp_file():
        path = "data/temp.json"
        empty_json = {"items": [{"id": i} for i in range(32)]}
        with open(path, 'w') as json_file:
            json.dump(empty_json, json_file, indent=4)
            print("[INFO] New temporary Dataset created")
            