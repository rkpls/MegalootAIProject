from time import sleep
import re
import cv2
import pytesseract
import numpy as np
import colorsys
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

icon_colors = {
    "none": "#b0b7cc",
    "wood": "#6f5e48",
    "swift": "#a9dae3",
    "scout": "#ae683b",
    "silver": "#858cb1",
    "gold": "#f89e10",
    "hunter": "#77853f",
    "warrior": "#443d3a",
    "mercenary": "#734d40",
    "ice": "#72d0fc",
    "mana": "#c34f9e",
    "orion": "#a7635c",
    "flesh": "#a96558",
    "arcane": "#19a3d7",
    "zepyron": "#5e42b1",
    "shadow": "#4b4a49",
    "turtle": "#5f5143",
    "darkness": "#454561",
    "poverty": "#4a4440",
    "thorn": "#4e3740",
    "thunder": "#dfad27",
    "demonic": "#812f38",
    "unchained": "#9a9fc0",
    "berserker": "#48473f",
    "cursed": "#3e3155",
    "royal": "#0070a0",
    "vampire": "#ab284a",
    "jade": "#00a793",
    "chromalure": "#37994d",
    "celestial": "#be4193",
    "cataclysm": "#927c67",
    "magma": "#e25900",
    "legacy": "#fdf0b1"
}

class TooltipReader:

    def get_ttbox(img):
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_bound = np.array([0, 50, 0])
        upper_bound = np.array([10, 255, 50])
        mask = cv2.inRange(hsv_img, lower_bound, upper_bound)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            tt_img = img[y:y+h, x:x+w]
            return tt_img
        else:
            return None
    
    def hex_to_hsv(hex_color):
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        hsv = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
        return (hsv[0] * 180, hsv[1] * 255, hsv[2] * 255)

    def detect_icons(id, tt_img):
        height, width, _ = tt_img.shape
        cropped_img = tt_img[6:12, 10:16]
        detected_icons = []
        hsv_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
        for icon_name, hex_color in icon_colors.items():
            lower, upper = TooltipReader.create_color_bounds(hex_color)
            mask = cv2.inRange(hsv_image, lower.astype(np.uint8), upper.astype(np.uint8))
            if cv2.countNonZero(mask) > 0:
                detected_icons.append(icon_name)
        return id, detected_icons

    def extract_price_tag(id, tt_img):
        height, width, _ = tt_img.shape
        cropped_img = tt_img[0:22, 0:width-24]  
        hsv_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2HSV)
        lower_bound = np.array([15, 180, 240])
        upper_bound = np.array([25, 255, 255])
        mask = cv2.inRange(hsv_img, lower_bound, upper_bound)
        preprocessed_img = cv2.bitwise_not(mask)
        preprocessed_img_rgb = cv2.cvtColor(preprocessed_img, cv2.COLOR_GRAY2RGB)
        custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789KMT'
        text = pytesseract.image_to_string(Image.fromarray(preprocessed_img_rgb), config=custom_config)
        return id, text
    
    def extract_rarity_name(id, tt_img):
        height, width, _ = tt_img.shape
        if id > 27:
            cropped_img = tt_img[0:22, 25:width-45]
        else:
            cropped_img = tt_img[0:22, 25:width]
        grayscale_img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        _, image_black_white = cv2.threshold(grayscale_img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist= 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        text = pytesseract.image_to_string(Image.fromarray(image_black_white), config=custom_config)
        split_text = text.split(' ', 1)
        if len(split_text) == 2:
            rarity, name = split_text
        else:
            rarity, name = split_text[0], ""
        return id, rarity.strip(), name.strip()

    def extract_item_features(id, tt_img):
        height, width, _ = tt_img.shape
        cropped_img = tt_img[24:height-9, :]
        new_height = cropped_img.shape[0] - (cropped_img.shape[0] % 16)
        adjusted_img = cropped_img[:new_height, :]
        num_snippets = new_height // 16
        snippets = []
        for i in range(num_snippets):
            snippet = adjusted_img[i*16:(i+1)*16, :]
            snippets.append(snippet)
        gold_snippet = snippets[-1]
        gold_snippet = gold_snippet[: , 15:30]
        grayscale_img = cv2.cvtColor(gold_snippet, cv2.COLOR_BGR2GRAY)
        _, image_black_white = cv2.threshold(grayscale_img, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist= 0123456789KMB%'
        gold_factor = pytesseract.image_to_string(Image.fromarray(image_black_white), config=custom_config)
        gold_factor_int = int(''.join(re.findall(r'\d+', gold_factor)))
        data_snippets = snippets
        results = []
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist= 0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ%'
        for snippet in data_snippets:
            snippet_value = snippet[: , 15:32]
            snippet_type = snippet[: , 47:width]
            snippet_value_gray = cv2.cvtColor(snippet_value, cv2.COLOR_BGR2GRAY)
            snippet_type_gray = cv2.cvtColor(snippet_type, cv2.COLOR_BGR2GRAY)
            _, snippet_value_black_white = cv2.threshold(snippet_value_gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            _, snippet_type_black_white = cv2.threshold(snippet_type_gray, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            type = pytesseract.image_to_string(Image.fromarray(snippet_type_black_white), config=custom_config)
            value = pytesseract.image_to_string(Image.fromarray(snippet_value_black_white), config=custom_config)
            results.append(value.strip())
            results.append(type.strip())
        return id, gold_factor_int, results



    def analyze(id, tt_img):
        if id > 27:
            id, price = TooltipReader.extract_price_tag(0, tt_img)
        else:
            price = 0
        id, i_class = TooltipReader.detect_icons(id, tt_img)
        id, rarity, name = TooltipReader.extract_rarity_name(id, tt_img)
        id, gold_factor, data = TooltipReader.extract_item_features(id, tt_img)
        return id, name, rarity, i_class, price, gold_factor, data

