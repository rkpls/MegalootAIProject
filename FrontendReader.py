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

coords_equipped = [(20, 127), (20, 166), (20, 205), (20, 244), (59, 127), (59, 166), (59, 205), (59, 244)]
coords_inventory = [(106, 127), (145, 127), (184, 127), (223, 127), (262, 127), (106, 166), (145, 166), (184, 166), (223, 166), (262, 166), (106, 205), (145, 205), (184, 205), (223, 205), (262, 205), (106, 244), (145, 243), (184, 243), (223, 244), (262, 244)]
coords_shop = [(87, 313), (126, 313), (165, 313), (204, 313)]
coords = coords_equipped + coords_inventory + coords_shop

floor_no = int(1)

standard_pytesseract_config = '-l eng --oem 1 --psm 13'

def store_image(image, file):
    cv2.imwrite(file, image)

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
                screenshot = cv2.resize(cv2.cvtColor(img_cropped, cv2.COLOR_BGRA2BGR), (640, 360), interpolation=cv2.INTER_CUBIC)
                store_image(screenshot, "images/screenshot.png")
                return screenshot

    def process_screenshot(imgget, id):
        x, y = FrontendReader.coords[id]
        box = (x, y, x + 26, y + 26)
        img = Image.fromarray(imgget)
        icon = img.crop(box)
        store_image(icon, f"images/{id}_icon.png")
        return icon, id

    def capture_item(id):
        img_rescaled = FrontendReader.capture_screenshot()
        id, icon = FrontendReader.process_screenshot(img_rescaled)
        id, data = FrontendReader.identify(id, icon)
        return id, data

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
        print(f"[INFO] identifing Item at {id}")
        db_path = "data/items.json"
        temp_path = "data/temp.json"
        db = FrontendReader.load_json(db_path)
        if db is None:
            db = {"items": []}
        try:
            db_temp = FrontendReader.load_json(temp_path)
        except FileNotFoundError:
            db_temp = {}
        icon_histogram = FrontendReader.image_to_feature(icon)
        found_item = None
        for item in db.get('items', []):
            stored_histogram = np.array(item.get('histogram'))
            if FrontendReader.compare_histograms(icon_histogram, stored_histogram):
                found_item = item
                break
        if found_item is None and id >= 28:
            img = FrontendReader.capture_screenshot()
            tt_box = TooltipReader.get_ttbox(img)
            id, name, i_rarity, i_class, value, gold_factor, data = TooltipReader.analyze(id, tt_box)
            item_data = {
                "histogram": icon_histogram.tolist(),
                "name": name,
                "i_rarity": i_rarity,
                "i_class": i_class,
                "value": value,
                "gold_factor": gold_factor,
                "data": data
            }
            found_item = item_data
        if found_item is None and id < 28:
            found_item = None
        db_temp[str(id)] = found_item
        with open(temp_path, 'w') as temp_file:
            json.dump(db_temp, temp_file, indent=4)
        print(f"[DATA] Found Item: {db_temp}")
        return id, found_item

    def identify_all():
        img = FrontendReader.capture_screenshot()
        for id in range(32):
            icon, _ = FrontendReader.process_screenshot(img, id)
            id, item_data = FrontendReader.identify(id, icon)
            DataManager.save_temporary(id, item_data)
        db_temp = DataManager.load_json("data/temp.json")
        DataManager.save_permanent("items", db_temp)
    
    def cash():
        img = FrontendReader.capture_screenshot()
        crop_img = img[104:117, 255:281]
        gray_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        _, img_b_w = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        h, w = img_b_w.shape[:2]
        scal_img = cv2.resize(img_b_w, (w * 8, h * 8), interpolation=cv2.INTER_NEAREST)
        store_image(scal_img, "images/gold_image.png")
        custom_config = r'-l eng --oem 1 --psm 13 -c tessedit_char_whitelist=.0123456789KMB'
        text = pytesseract.image_to_string(Image.fromarray(scal_img), config=custom_config)
        value_str = text.strip()
        if not any(c.isdigit() or c == '.' for c in value_str[:-1]) and not value_str.isdigit():
            print("[ERROR] Invalid OCR result:", value_str)
            return None
        multiplier = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        if value_str[-1] in multiplier:
            try:
                numeric_value = float(value_str[:-1])  # Handle decimals
                cash = int(numeric_value * multiplier[value_str[-1]])
            except ValueError:
                print("[ERROR] Invalid numeric value:", value_str)
                return None
        else:
            try:
                cash = int(float(value_str))
            except ValueError:
                print("[ERROR] Invalid numeric value:", value_str)
                return None
        print(f"[DATA] Current cash: {cash}")
        return cash


    def next_floor(img):
        global floor_no
        crop_img = img[9:22, 182:198]
        gray_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        _, img_b_w = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        h, w = img_b_w.shape[:2]
        scal_img = cv2.resize(img_b_w, (w * 8, h * 8), interpolation=cv2.INTER_NEAREST)        
        store_image(scal_img, "images/floor_image.png")
        custom_config = r'--oem 1 --psm 13 -c tessedit_char_whitelist=0123456789'
        current_floor = floor_no
        try:
            current_floor = int(pytesseract.image_to_string(Image.fromarray(scal_img), config=custom_config))
            print(f"[DATA] Current Floor: {current_floor}")
        except:
            print("[ERR] could not process floor number")
        if current_floor > floor_no:
            floor_no = current_floor
            return True, floor_no
        return False, floor_no

    def next_fight(img):
        levels = {1: 43.85, 2: 42.73, 3: 38.76, 4: 37.75, 5: 33.81, 6: 32.81, 7: 28.85, 8: 27.84, 9: 23.88, 10: 22.87, 11: 18.93, 12: 17.96}
        img_gray = cv2.cvtColor(img[9:21, 218:289], cv2.COLOR_BGR2GRAY)
        store_image(img_gray, "images/fight_image.png")
        cur_level = np.mean(img_gray)
        fight_no = None
        for level, brightness in levels.items():
            if abs(cur_level - brightness) <= 0.5:
                fight_no = level
                break
        if fight_no is not None:
            print(f"[DATA] Current Fight: {fight_no}")
        else:
            print("[ERR] no fight match found")
        return False, fight_no

    
    def is_dead():
        img = FrontendReader.capture_screenshot()
        img_np = np.array(img)
        avg_color = np.mean(img_np, axis=(0, 1))
        threshold_color = tuple(int("151520"[i:i+2], 16) for i in (0, 2, 4))
        if all(avg_color[i] < threshold_color[i] for i in range(3)):
            print("[DATA] I died, Sadge")
            return True
        return False

    def player_stats():
        crop_img = FrontendReader.capture_screenshot()[37:37+44, 72:72+177]
        store_image(crop_img, f"images/player_stats.png")
        hex_hp_color = "A01136"
        hex_armor_color = "434C5B"
        hp_color = np.array([int(hex_hp_color[i:i+2], 16) for i in (0, 2, 4)])
        armor_color = np.array([int(hex_armor_color[i:i+2], 16) for i in (0, 2, 4)])
        hp_deviation = (hp_color * 0.1).astype(int)
        armor_deviation = (armor_color * 0.1).astype(int)
        hp_img_b_w = cv2.inRange(crop_img, hp_color - hp_deviation, hp_color + hp_deviation)
        armor_img_b_w = cv2.inRange(crop_img, armor_color - armor_deviation, armor_color + armor_deviation)
        h_p, w_p = hp_img_b_w.shape[:2]
        h_a, w_a = armor_img_b_w.shape[:2]
        hp_scal_img = cv2.resize(hp_img_b_w, (w_p * 8, h_p * 8), interpolation=cv2.INTER_NEAREST)#[19:32, 50:109]
        armor_scal_img = cv2.resize(armor_img_b_w, (w_a * 8, h_a * 8), interpolation=cv2.INTER_NEAREST)#[0:13, 68:121]
        store_image(hp_scal_img, "images/health.png")
        store_image(armor_scal_img, "images/armor.png")
        custom_config = r'-l eng --oem 1 --psm 13 -c tessedit_char_whitelist= /0123456789'
        try:
            health = pytesseract.image_to_string(Image.fromarray(hp_scal_img), config=custom_config)
        except:
            health = 0
        try:
            armor = pytesseract.image_to_string(Image.fromarray(armor_scal_img), config=custom_config)
        except:
            armor = 0
        if health:
            print(f"[DATA] Player health is {health}")
        if armor:
            print(f"[DATA] Player armor is {armor}")

    #cur_live, max_life = FrontendReader.life()
    #print(f"[INFO] Health: {cur_life} out of {max_life}")
    #cur_armor, max_armor = FrontendReader.armor()
    #print(f"[INFO] Armor: {cur_armor} out of {max_armor}")