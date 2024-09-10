import cv2
import numpy as np

class ColorFetcher:
    def __init__(self, screenshot_path):
        self.screenshot_path = screenshot_path

    def fetch_colors(self, coords):
        """Extracts the colors at the given coordinates."""
        img = cv2.imread(self.screenshot_path)
        slot_colors = {}

        for idx, (x, y) in enumerate(coords):
            pixel_color = img[y, x]  # Get the color at the coordinate
            slot_colors[f"slot_{idx}"] = pixel_color[:3]  # Extract RGB
            print(f"Slot {idx}: Color: {pixel_color[:3]}")

        return slot_colors

if __name__ == "__main__":
    # Path to the screenshot that contains all item slots
    screenshot_path = "C:\\Users\\rikop\\Desktop\\megaloot\\all_slots_screenshot.png"

    # Coordinates for all 32 item slots (equipped, inventory, and shop)
    item_coords = [
        # Equipped items (top-left corner of each item)
        (88, 658), (262, 658), (88, 834), (262, 834),
        (88, 1008), (262, 1008), (88, 1184), (262, 1184),
        
        # Inventory items (5x4 grid)
        (474, 658), (622, 658), (770, 658), (918, 658), (1066, 658),
        (474, 810), (622, 810), (770, 810), (918, 810), (1066, 810),
        (474, 962), (622, 962), (770, 962), (918, 962), (1066, 962),
        (474, 1114), (622, 1114), (770, 1114), (918, 1114), (1066, 1114),
        
        # Shop items
        (390, 1496), (566, 1496), (742, 1496), (916, 1496)
    ]

    # Fetch the colors for each item slot
    fetcher = ColorFetcher(screenshot_path)
    slot_colors = fetcher.fetch_colors(item_coords)

    # You can now use the fetched colors as needed
    print("Fetched slot colors:", slot_colors)
