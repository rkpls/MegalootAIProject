import os
from time import sleep, time
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

floor_no = int(1)
fight_no = int(1)

standard_pytesseract_config = '-l eng --oem 1 --psm 13'

def store_image(image, file):
    cv2.imwrite(file, image)

class FrontendReader:
    def capture_screenshot(window_title="windowtitle", timeout=10):
        start_time = time()
        window = None

    # Wait for the window to become active
        while time() - start_time < timeout:
            windows = gw.getWindowsWithTitle(window_title)
            if windows:
                window = windows[0]
                if window.isActive:
                    break
                else:
                    window.activate()
                    sleep(0.1)  # Brief pause to allow the window to activate
            else:
                sleep(0.1)
        if not window:
            print(f"[ERROR] Window '{window_title}' not found or did not become active within {timeout} seconds.")
            return None
    # Get window position and size
        window_rect = {"top": window.top,"left": window.left,"width": window.width,"height": window.height}
    # Detect which monitor the window is on
        with mss.mss() as sct:
            monitor = None
            for mon in sct.monitors[1:]:  # Skip sct.monitors[0] which is all monitors
                if (window_rect["left"] >= mon["left"] and
                    window_rect["left"] < mon["left"] + mon["width"] and
                    window_rect["top"] >= mon["top"] and
                    window_rect["top"] < mon["top"] + mon["height"]):
                    monitor = mon
                    break

            if not monitor:
                print(f"[ERROR] Monitor for window '{window_title}' not found.")
                return None
        # Adjust the window_rect to be relative to the monitor
            relative_rect = {"top": window_rect["top"] - monitor["top"],"left": window_rect["left"] - monitor["left"],"width": window_rect["width"],"height": window_rect["height"]}
        # Set up the monitor area to capture
            monitor_area = {"top": monitor["top"] + relative_rect["top"],"left": monitor["left"] + relative_rect["left"],"width": relative_rect["width"],"height": relative_rect["height"]}
        # Capture the window area
        img = np.array(sct.grab(monitor_area))
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        # Adjust aspect ratio to 16:9 by cropping if necessary
        screen_width, screen_height = img.shape[1], img.shape[0]
        target_aspect_ratio = 16 / 9
        current_aspect_ratio = screen_width / screen_height

        if current_aspect_ratio > target_aspect_ratio:
        # Image is wider than 16:9, crop sides
            new_width = int(screen_height * target_aspect_ratio)
            offset_x = (screen_width - new_width) // 2
            img_cropped = img[:, offset_x:offset_x + new_width]
        elif current_aspect_ratio < target_aspect_ratio:
        # Image is taller than 16:9, crop top and bottom
            new_height = int(screen_width / target_aspect_ratio)
            offset_y = (screen_height - new_height) // 2
            img_cropped = img[offset_y:offset_y + new_height, :]
        else:
            img_cropped = img
        screenshot = cv2.resize(
            img_cropped,
            (640, 360),
            interpolation=cv2.INTER_AREA
        )
        store_image(screenshot, "images/screenshot.png")
        return screenshot


    def process_screenshot(imgget, id):
        x, y = coords[id]
        icon = imgget[y:y+26, x:x+26]
        store_image(icon, f"images/{id}_icon.png")
        return icon, id

    def load_json(filepath):
        with open(filepath, 'r') as file:
            return json.load(file)

    def image_to_feature(image):
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist

    def compare_histograms(a, b):
        return cv2.compareHist(a, b, cv2.HISTCMP_CORREL) >= 0.95

    def identify(id, icon):
        print(f"[INFO] Identifying item at position {id}")
        db_path = "data/items.json"
        db = FrontendReader.load_json(db_path)
        temp_path = "data/temp.json"
        temp = FrontendReader.load_json(temp_path)
        icon_histogram = FrontendReader.image_to_feature(icon)
        found_item = None
        for item in temp.get('items', []):
            stored_histogram = np.array(item.get('histogram'))
            if FrontendReader.compare_histograms(icon_histogram, stored_histogram):
                found_item = item
                print(f"[INFO] Unchanged item at position {id}")
                break
        for item in db.get('items', []):
            stored_histogram = np.array(item.get('histogram'))
            if FrontendReader.compare_histograms(icon_histogram, stored_histogram):
                found_item = item
                print(f"[INFO] Changed item at position {id}")
                break
        if found_item is None:
            print(f"[INFO] New item at position {id}")
            IOControl.check_item(id)
            img = FrontendReader.capture_screenshot()
            tt_box = TooltipReader.get_ttbox(img)
<<<<<<< Updated upstream
            id, name, i_rarity, i_class, value, gold_factor, data = TooltipReader.analyze(id, tt_box)
            item_data_permanent = {"histogram": icon_histogram.tolist(),"name": name,"i_rarity": i_rarity,"i_class": i_class,"value": value,"gold_factor": gold_factor,"data": data}
            item_data_temporary = {"id": id,"name": name,"i_rarity": i_rarity,"i_class": i_class,"value": value,"gold_factor": gold_factor,"data": data}
            DataManager.save_permanent(item_data_permanent)
            item_data_temporary = {"id": id, "name": None}
            DataManager.save_temporary(id, item_data_temporary)
            item_data = item_data_temporary
        else:
            temp_data = DataManager.load_json("data/temp.json")
=======
            try:
                id, name, i_rarity, i_class, value, gold_factor, data = TooltipReader.analyze(id, tt_box)
                item_data_permanent = {"histogram": icon_histogram.tolist(),"name": name,"i_rarity": i_rarity,"i_class": i_class,"value": value,"gold_factor": gold_factor,"data": data}
                item_data_temporary = {"id": id,"name": name,"i_rarity": i_rarity,"i_class": i_class,"value": value,"gold_factor": gold_factor,"data": data}
                DataManager.save_permanent(item_data_permanent)
            except:
                item_data_temporary = {"id": id, "histogram":icon_histogram, "name": 0}
            DataManager.save_temporary(item_data_temporary, id)
            item_data = item_data_temporary  # For returning and further processing
        else:
            # Load temporary data if available, or create item_data without 'id'
            temp_data = FrontendReader.load_json(temp_path)
>>>>>>> Stashed changes
            if temp_data:
                item_data = temp_data
            else:
                item_data = found_item.copy()
                item_data['id'] = id
                item_data.pop('histogram', None)
                DataManager.save_temporary(item_data, id)
        return id, item_data

    def capture_item(id):
        img_rescaled = FrontendReader.capture_screenshot()
        icon, id = FrontendReader.process_screenshot(img_rescaled, id)
        id, data = FrontendReader.identify(id, icon)
        return id, data

    def identify_all():
        img = FrontendReader.capture_screenshot()
        for id in range(32):
            icon, _ = FrontendReader.process_screenshot(img, id)
            id, item_data = FrontendReader.identify(id, icon)
            DataManager.save_temporary(id, item_data)
        DataManager.save_permanent("data/items.json", item_data)

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
            print("[ERR] Invalid OCR result:", value_str)
            return None
        multiplier = {'K': 1000, 'M': 1000000, 'B': 1000000000}
        if value_str[-1] in multiplier:
            try:
                numeric_value = float(value_str[:-1])  # Handle decimals
                cash = int(numeric_value * multiplier[value_str[-1]])
            except ValueError:
                print("[ERR] Invalid numeric value:", value_str)
                return None
        else:
            try:
                cash = int(float(value_str))
            except ValueError:
                print("[ERR] Invalid numeric value:", value_str)
                return None
        print(f"[DATA] Current cash: {cash}")
        return cash


    def next_floor(img):
        global floor_no
        crop_img = img[9:22, 182:199]
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
        global fight_no
        levels = {1: 45.03, 2: 43.98, 3: 39.86, 4: 38.80, 5: 34.71, 6: 33.68, 7: 29.63, 8: 28.61, 9: 24.58, 10: 23.44, 11: 19.41, 12: 18.40, 13: 14.38}
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
        gray_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        _, img_b_w = cv2.threshold(gray_img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        store_image(img_b_w, f"images/player_stats.png")
        armor_img = img_b_w[0:13, 67:67+51]
        hp_img = img_b_w[19:19+13, 53:53+51]
        ar_h, ar_w = armor_img.shape[:2]
        hp_h, hp_w = hp_img.shape[:2]
        armor_scal_img = cv2.resize(armor_img, (ar_w * 8, ar_h * 8), interpolation=cv2.INTER_NEAREST)
        hp_scal_img = cv2.resize(hp_img, (hp_w * 8, hp_h * 8), interpolation=cv2.INTER_NEAREST)
        store_image(armor_scal_img, "images/armor.png")
        store_image(hp_scal_img, "images/health.png")
        custom_config = r'-l eng --oem 1 --psm 13 -c tessedit_char_whitelist= /0123456789'
        try:
            armor = pytesseract.image_to_string(Image.fromarray(armor_scal_img), config=custom_config)
        except:
            armor = 0
        try:
            health = pytesseract.image_to_string(Image.fromarray(hp_scal_img), config=custom_config)
        except:
            health = 0
        if health:
            print(f"[DATA] Player health is {health}")
        if armor:
            print(f"[DATA] Player armor is {armor}")

    #cur_live, max_life = FrontendReader.life()
    #print(f"[INFO] Health: {cur_life} out of {max_life}")
    #cur_armor, max_armor = FrontendReader.armor()
    #print(f"[INFO] Armor: {cur_armor} out of {max_armor}")