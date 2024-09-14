import os
from time import sleep
import json
import cv2
import numpy as np
import pygetwindow as gw
import mss
from PIL import Image

coords_equipped = [(20, 127), (20, 166), (20, 205), (20, 244), (59, 127), (59, 166), (59, 205), (59, 244)]
coords_inventory = [(106, 127), (145, 127), (184, 127), (223, 127), (262, 127), (106, 166), (145, 166), (184, 166), (223, 166), (262, 166), (106, 205), (145, 205), (184, 205), (223, 205), (262, 205), (106, 244), (145, 243), (184, 243), (223, 244), (262, 244)]
coords_shop = [(87, 313), (126, 313), (165, 313), (204, 313)]
coords = coords_equipped + coords_inventory + coords_shop

class FrontendReader:
    def capture_screenshot():
        if gw.getWindowsWithTitle("Megaloot"):
            with mss.mss() as sct:
                monitor = sct.monitors[1]
                img = np.array(sct.grab(monitor))
                screen_width, screen_height = monitor['width'], monitor['height']
                target_aspect_ratio = 16 / 9
                current_aspect_ratio = screen_width / screen_height
                if current_aspect_ratio > target_aspect_ratio:
                    new_width = int(screen_height * target_aspect_ratio)
                    offset_x = (screen_width - new_width) // 2
                    img_cropped = img[:, offset_x:offset_x + new_width]
                elif current_aspect_ratio < target_aspect_ratio:
                    new_height = int(screen_width / target_aspect_ratio)
                    offset_y = (screen_height - new_height) // 2
                    img_cropped = img[offset_y:offset_y + new_height, :]
                else:
                    img_cropped = img
                img_bgr = cv2.cvtColor(img_cropped, cv2.COLOR_BGRA2BGR)
                img_rescaled = cv2.resize(img_bgr, (640, 360), interpolation=cv2.INTER_CUBIC)
                save_path = os.path.join("rescaled_image.png")
                cv2.imwrite(save_path, img_rescaled)
                return img_rescaled

    def process_screenshot(imgget, id):
        x, y = FrontendReader.coords[id]
        box = (x, y, x + 26, y + 26)
        img = Image.fromarray(imgget)
        icon = img.crop(box)
        return icon, id

    def load_json(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def image_to_feature(image):
        image = image.convert('RGB')
        open_cv_image = np.array(image)
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        hist = cv2.calcHist([open_cv_image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        return hist.flatten()

    def compare_histograms(a, b):
        return cv2.compareHist(a, b, cv2.HISTCMP_CORREL) >= 0.999

    def identify(id, icon):
        db_path = "data/items.json"
        db = FrontendReader.load_json(db_path)
        if db is None:
            db = {"items":[]}
        icon_hash = FrontendReader.image_to_feature(icon)
        icon_data = next((item for item in db if item.get('hash') == icon_hash), None)
        if icon_data:
            try:
                items_data = FrontendReader.load_json(db_path)
                items_data[id] = icon_data
            except:
                icon_data = None
            return id, icon_data

    def capture_item(id):
        img_rescaled = FrontendReader.capture_screenshot()
        id, icon = FrontendReader.process_screenshot(img_rescaled)
        id, data = FrontendReader.identify(id, icon)
        return id, data
            
        
