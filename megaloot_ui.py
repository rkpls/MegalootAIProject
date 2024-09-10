import tkinter as tk
from tkinter import ttk

class MegalootUI:
    equipped_item_names = ["Helmet", "Chestplate", "Pants", "Boots", "Necklace", "Weapon", "Ring 1", "Ring 2"]

    def __init__(self, item_name, item_data, submit_callback):
        self.item_name = item_name
        self.item_data = item_data
        self.submit_callback = submit_callback
        self.rarity = None
        self.usage = None
        self.name = None

    def filter_items_by_usage(self, selected_usage):
        return [item['name'] for item in self.item_data['items'] if item['usage'] == selected_usage]

    def open_ui(self, position):
        def update_item_names(*args):
            usage = usage_var.get()
            filtered_items = self.filter_items_by_usage(usage)
            name_list['values'] = filtered_items
            name_list.current(0)

        root = tk.Tk()
        root.title("Megaloot AI - Item Identification")
        root.configure(bg="#2E2E2E")
        root.geometry("400x600")
        
        # Center the UI on the screen
        window_width, window_height = 400, 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        position_right = int(screen_width / 2 - window_width / 2)
        position_down = int(screen_height / 2 - window_height / 2)
        root.geometry(f"{window_width}x{window_height}+{position_right}+{position_down}")
    
        # Display the actual equipped item name based on the position (0 to 7)
        item_name = MegalootUI.equipped_item_names[position]

        label = tk.Label(root, text=f"Scanned Item: {item_name}", fg="white", bg="#2E2E2E", font=("Arial", 16))
        label.pack(pady=20)

        # Rarity dropdown with color names
        rarity_label = tk.Label(root, text="Select Rarity:", fg="white", bg="#2E2E2E", font=("Arial", 12))
        rarity_label.pack()
        rarity_list = ttk.Combobox(root, values=[
            "none", 
            "common", "uncommon", "rare", "legendary", 
            "mythic", "eternal", "abyssal", "cosmic", "divine"
        ])
        rarity_list.current(0)
        rarity_list.pack(pady=5)

        # Usage dropdown
        usage_label = tk.Label(root, text="Select Usage:", fg="white", bg="#2E2E2E", font=("Arial", 12))
        usage_label.pack()
        usage_var = tk.StringVar()
        usage_list = ttk.Combobox(root, textvariable=usage_var, values=["none", "helmet", "chestplate", "pants", "boots", "necklace", "weapon", "ring"])
        usage_list.current(0)
        usage_list.pack(pady=5)
        usage_var.trace_add('write', update_item_names)

        # Item name dropdown
        name_label = tk.Label(root, text="Select Item Name:", fg="white", bg="#2E2E2E", font=("Arial", 12))
        name_label.pack()
        name_list = ttk.Combobox(root)
        name_list.pack(pady=5)

        update_item_names()

        # Submit button
        close_button = tk.Button(root, text="Submit", command=lambda: self.submit_callback(rarity_list.get(), usage_list.get(), name_list.get(), root), bg="#4CAF50", fg="white", font=("Arial", 12))        
        close_button.pack(pady=10)

        root.mainloop()
