import os
import json
import cv2
import numpy as np
import pygetwindow as gw
import mss
from PIL import Image

class FrontendReader:
    def capture_screenshot(self):
        window = gw.getWindowsWithTitle("Megaloot")
        if window:
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                print("[INFO] Capturing Frontend")
                img = np.array(sct.grab(monitor))
                imgs = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                pil_img = Image.fromarray(cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB))
                img_bgr = pil_img.convert("P", palette=Image.ADAPTIVE, colors=256)
                img_bgr = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                imgxs = cv2.resize(img_bgr, (640, 360), interpolation=cv2.INTER_CUBIC)
                print("[INFO] Processing Frontend - Rescaling FHD")
                save_path = os.path.join("rescaled_image.png")
                cv2.imwrite(save_path, imgxs)
                return imgxs

    def process_screenshot(self, imgget):
        print("[INFO] Updating Items")
        coords_equipped = [(20, 127), (20, 166), (20, 205), (20, 244)]
        coords_inventory = [(106, 127), (145, 127), (184, 127), (223, 127), (262, 127), (106, 166), (145, 166), (184, 166), (223, 166), (262, 166), (106, 205), (145, 205), (184, 205), (223, 205), (262, 205), (106, 244), (145, 243), (184, 243), (223, 244), (262, 244)]
        coords_shop = [(87, 313), (126, 313), (165, 313), (204, 313)]
        img = Image.fromarray(imgget)
        print("[INFO] Checking Equipped")
        for index, (x, y) in enumerate(coords_equipped):
            box = (x, y, x + 26, y + 26)
            icon = img.crop(box)
            self.identify("equipped", icon, index)
        print("[INFO] Checking Inventory")
        for index, (x, y) in enumerate(coords_inventory):
            box = (x, y, x + 26, y + 26)
            icon = img.crop(box)
            self.identify("inventory", icon, index)
        print("[INFO] Checking Shop")
        for index, (x, y) in enumerate(coords_shop):
            box = (x, y, x + 26, y + 26)
            icon = img.crop(box)
            self.identify("shop", icon, index)

    def load_json(self, filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def write_json(self, filepath, data):
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file, indent=4)
                print(f"[INFO] Data written to {filepath}")
        except Exception as e:
            print(f"[ERROR] Failed to write to {filepath}: {str(e)}")

    def image_to_feature(self, image):
        image = image.convert('RGB')
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        hist = cv2.calcHist([open_cv_image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        return hist.flatten()

    def compare_histograms(self, a, b):
        return cv2.compareHist(a, b, cv2.HISTCMP_CORREL) >= 0.999



    def identify(self, pos, icon, index):
        db_path = "data/items.json"
        gear_path = "currentPlaythrough/gear.json"
        inventory_path = "currentPlaythrough/inventory.json"
        shop_path = "currentPlaythrough/shop.json"
        db = self.load_json(db_path)
        if db is None:
            db = {"items":[]}
        icon_hash = self.image_to_feature(icon)
        icon_data = next((item for item in db if item.get('hash') == icon_hash), None)
        if icon_data:
            if pos == "shop":
                shop = self.load_json(shop_path)
                if shop is None:
                    shop = [None] * 4
                shop[index] = icon_data
                self.write_json(shop_path, shop)
            elif pos == "inventory":
                inventory = self.load_json(inventory_path)
                if inventory is None:
                    inventory = [None] * 20
                inventory[index] = icon_data
                self.write_json(inventory_path, inventory)
            elif pos == "equipped":
                gear = self.load_json(gear_path)
                if gear is None:
                    gear = [None] * 8
                gear[index] = icon_data
                self.write_json(gear_path, gear)
        else:
            print("[INFO] New item detected!")
            
