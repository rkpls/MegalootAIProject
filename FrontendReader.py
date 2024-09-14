import os
from time import sleep
import json
import cv2
import numpy as np
import pygetwindow as gw
import mss
from PIL import Image
import pytesseract
from TooltipReader import TooltipReader
from DataManager import DataManager
from IOControl import IOControl

coords_equipped = [(20, 127), (20, 166), (20, 205), (20, 244), (59, 127), (59, 166), (59, 205), (59, 244)]
coords_inventory = [(106, 127), (145, 127), (184, 127), (223, 127), (262, 127), (106, 166), (145, 166), (184, 166), (223, 166), (262, 166), (106, 205), (145, 205), (184, 205), (223, 205), (262, 205), (106, 244), (145, 243), (184, 243), (223, 244), (262, 244)]
coords_shop = [(87, 313), (126, 313), (165, 313), (204, 313)]
coords = coords_equipped + coords_inventory + coords_shop

previous_level = 1
last_floor = 0

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
                return cv2.resize(cv2.cvtColor(img_cropped, cv2.COLOR_BGRA2BGR), (640, 360), interpolation=cv2.INTER_CUBIC)

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

    def identify_all():
        db_path_temp = "data/temp.json"
        img = FrontendReader.capture_screenshot()
        for id in range(32):
            icon, _ = FrontendReader.process_screenshot(img, id)
            id, icon_data = FrontendReader.identify(id, icon)
            if icon_data is None and id in range(28, 32):
                IOControl.check_item(id)
                img = FrontendReader.capture_screenshot
                tt_img = FrontendReader.capture_screenshot()
                TooltipReader.analyze(id, tt_img)
        
        # Save the identified item or None to the temporary file
            DataManager.save_temporary(id, icon_data)
            
            
            
    def capture_item(id):
        img_rescaled = FrontendReader.capture_screenshot()
        id, icon = FrontendReader.process_screenshot(img_rescaled)
        id, data = FrontendReader.identify(id, icon)
        return id, data
    
    
    def next_floor():
        sleep(0.1)
        global last_floor
        img = FrontendReader.capture_screenshot()
        cropped_img = img[10:22, 182:214]
        grayscale_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        _, image_black_white = cv2.threshold(grayscale_img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'
        current_floor = pytesseract.image_to_string(Image.fromarray(image_black_white), config=custom_config)
        try:
            int(current_floor)
            if current_floor > last_floor:
                last_floor = current_floor
                return True
            return False
        except:
            return False

    def next_fight():
        sleep(0.1)
        global previous_level
        brightness_levels = {1: 43.85,2: 42.73,3: 38.76,4: 37.75,5: 33.81,6: 32.81,7: 28.85,8: 27.84,9: 23.88,10: 22.87,11: 18.93,12: 17.96,13: 13.99}
        img = FrontendReader.capture_screenshot()
        try:
            current_level = np.mean(cv2.cvtColor(img[9:21, 218:289], cv2.COLOR_BGR2GRAY))
            for i, value in enumerate(brightness_levels):
                if abs(current_level - value) <= 0.2:
                    break
            if current_level < previous_level or current_level == 1 and previous_level == 13:
                previous_level = current_level
                return True
            return False
        except:
            return False    
    
    def is_dead():
        sleep(3)
        img = FrontendReader.capture_screenshot()
        img_np = np.array(img)
        avg_color = np.mean(img_np, axis=(0, 1))
        threshold_color = tuple(int("151520"[i:i+2], 16) for i in (0, 2, 4))
        if all(avg_color[i] < threshold_color[i] for i in range(3)):
            return True
        return False

    def cash():
        pass