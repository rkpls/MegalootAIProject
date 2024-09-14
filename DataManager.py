import json
    
class DataManager:    

    def save_temporary(id, name, rarity, gold_factor, data):
        try:
            filepath = "data/temp.json"
            with open(filepath, 'w') as file:
                json.dump(id, name, rarity, gold_factor, data, file, indent=4)
                print(f"[INFO] Data written to {filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to write to {filepath}: {str(e)}")
        
    def save_permanent(icon, name, rarity, price, gold_factor, data):
        try:
            filepath = "data/items.json"
            with open(filepath, 'w') as file:
                json.dump(icon, name, rarity, price, gold_factor, data, file, indent=4)
                print(f"[INFO] Data written to {filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to write to {filepath}: {str(e)}")