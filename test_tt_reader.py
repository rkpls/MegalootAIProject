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

#libs, tesseract path and icon_colors here...

def show_image(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def preprocess_image_for_ocr(image):
    # Convert image to grayscale
    show_image("original", image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    show_image("filter", gray_image)
    scale_factor = 4.0
    width = int(gray_image.shape[1] * scale_factor)
    height = int(gray_image.shape[0] * scale_factor)
    upscaled_image = cv2.resize(gray_image, (width, height), interpolation=cv2.INTER_LINEAR)
    show_image("upscale", upscaled_image)
    # Apply adaptive thresholding to obtain a binary image
    final_image = cv2.adaptiveThreshold(upscaled_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    show_image("final", final_image)
    return final_image

def hex_to_hsv(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    hsv = colorsys.rgb_to_hsv(rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)
    return (hsv[0] * 180, hsv[1] * 255, hsv[2] * 255)

def create_color_bounds(hex_color, tolerance=10):
    hsv_color = hex_to_hsv(hex_color)
    lower_bound = np.array([max(int(hsv_color[0] - tolerance), 0), max(int(hsv_color[1] - 40), 0), max(int(hsv_color[2] - 40), 0)])
    upper_bound = np.array([min(int(hsv_color[0] + tolerance), 180), min(int(hsv_color[1] + 40), 255), min(int(hsv_color[2] + 40), 255)])
    return lower_bound, upper_bound

def detect_icons(image):
    detected_icons = []
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    for icon_name, hex_color in icon_colors.items():
        lower, upper = create_color_bounds(hex_color)
        mask = cv2.inRange(hsv_image, lower.astype(np.uint8), upper.astype(np.uint8))
        if cv2.countNonZero(mask) > 0:
            detected_icons.append(icon_name)
    return detected_icons

def extract_tooltip_data(image_path):
    image = cv2.imread(image_path)
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist= ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    preprocessed_image = preprocess_image_for_ocr(image)
    text = pytesseract.image_to_string(Image.fromarray(preprocessed_image), config=custom_config)
    icons = detect_icons(image)
    return text, icons

image_path = 'tt.png'
text, icons = extract_tooltip_data(image_path)
print(text)
print(icons)