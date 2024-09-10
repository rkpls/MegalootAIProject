import numpy as np

class ColorDetector:
    def __init__(self):
        # New color codes for item rarities and empty slots
        self.rarity_colors = {
            "common": (140, 148, 173),
            "uncommon": (90, 205, 44),
            "rare": (29, 165, 226),
            "legendary": (197, 69, 154),
            "mythic": (249, 160, 39),
            "eternal": (191, 25, 65),
            "abyssal": (122, 19, 43),
            "cosmic": (191, 65, 153),
            "divine": (252, 241, 180)
        }
        self.empty_colors = {
            "equipped": (76, 87, 99),  # Equipped empty slot
            "inventory": (10, 14, 25)  # Inventory empty slot
        }

    def color_distance(self, color1, color2):
        """Calculate the Euclidean distance between two RGB colors."""
        return np.linalg.norm(np.array(color1) - np.array(color2))

    def detect_rarity(self, pixel_color):
        """Detect item rarity based on a single pixel's RGB color."""
        pixel_color = tuple(pixel_color[:3])  # Ensure it's a tuple with RGB values

        # Check if slot is empty by matching exact empty slot colors
        if self.color_distance(pixel_color, self.empty_colors["equipped"]) < 10:
            return "empty (equipped)"
        if self.color_distance(pixel_color, self.empty_colors["inventory"]) < 10:
            return "empty (inventory)"

        # Find the closest matching rarity color
        closest_rarity = None
        min_distance = float('inf')

        for rarity, target_color in self.rarity_colors.items():
            distance = self.color_distance(pixel_color, target_color)
            if distance < min_distance:
                min_distance = distance
                closest_rarity = rarity

        return closest_rarity if closest_rarity else "unknown"
