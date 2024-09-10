import os
import cv2
from mss import mss
import numpy as np
import pygetwindow as gw

class ScreenCapture:
    def __init__(self, screenshot_folder):
        self.sct = mss()
        self.item_size = 125  # Item size is 125x125px for 2880x1800 resolution
        self.screenshot_folder = screenshot_folder

        # Create screenshot folder if it doesn't exist
        os.makedirs(self.screenshot_folder, exist_ok=True)

    def capture(self, save=False):
        monitor = self.sct.monitors[1]  # Capture the primary monitor
        img = np.array(self.sct.grab(monitor))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        if save:
            # Save the screenshot for comparison
            screenshot_path = os.path.join(self.screenshot_folder, "screenshot.png")
            self.save_screenshot(screenshot_path, img)
            print(f"Screenshot saved at: {screenshot_path}")

        return img

    def save_screenshot(self, path, img):
        # Save the screenshot
        cv2.imwrite(path, img)

    def is_megaloot_in_focus(self):
        active_window_title = gw.getActiveWindowTitle()
        return active_window_title and "Megaloot" in active_window_title

    def get_item_coordinates(self):
        # Coordinates for equipped items (single pixel to analyze)
        equipped_coords = [
            (88, 658), (262, 658), (88, 834), (262, 834),
            (88, 1008), (262, 1008), (88, 1184), (262, 1184)
        ]

        # Inventory items are a 5x4 grid (top-left corners provided)
        inventory_coords = []
        top_left_inventory = (474, 658)
        bottom_right_inventory = (1176, 1184)
        x_step = (bottom_right_inventory[0] - top_left_inventory[0]) // 4
        y_step = (bottom_right_inventory[1] - top_left_inventory[1]) // 3
        
        for i in range(4):  # 4 rows
            for j in range(5):  # 5 columns
                x = top_left_inventory[0] + j * x_step
                y = top_left_inventory[1] + i * y_step
                inventory_coords.append((x, y))

        # Coordinates for shop items (top-left corners provided)
        shop_coords = [(390, 1496), (566, 1496), (742, 1496), (916, 1496)]

        return equipped_coords, inventory_coords, shop_coords

    def mark_pixels_on_items(self, img, item_coords):
        """Mark analyzed pixels on all items in the image with a pink dot."""
        marked_img = img.copy()

        for x, y in item_coords:
            cv2.circle(marked_img, (x, y), 5, (255, 0, 255), -1)  # Pink dot on the analyzed pixel

        return marked_img

    def get_single_pixel_color(self, img, x, y):
        """Extract the color of a single pixel."""
        return img[y, x]  # Get the color at (x, y)
