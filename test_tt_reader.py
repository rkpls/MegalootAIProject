import cv2
import pytesseract
from PIL import Image
import numpy as np

# Configure pytesseract path to your installation of Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
\
def extract_tooltip_data(image_path):
    # Load the tooltip image
    image = cv2.imread(image_path)
    
    # Convert to RGB for pytesseract
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Use pytesseract to extract text
    text = pytesseract.image_to_string(rgb_image)
    print("Extracted Text:")
    print(text)
    
    # Process image to detect icons
    # Assuming icons have distinct colors or features, you may use template matching or simple color detection
    # For demonstration, we'll use a placeholder function
    icons = detect_icons(image)
    
    return text, icons

def detect_icons(image):
    # Placeholder for icon detection logic
    # You might use methods like template matching if you have sample images of the icons
    detected_icons = ["icon1", "icon2"]  # Example output
    return detected_icons

# Example usage
image_path = 'tt.png'
text, icons = extract_tooltip_data(image_path)
print("Detected Icons:")
print(icons)

"""
    none: #bob7cc,
    wood: #6f5e48,
    swift: #a9dae3,
    scout: #ae683b,
    silver: #858cb1,
    gold: #f89e10,
    hunter: #77853f,
    warrior: #443d3a,
    mercenaryy: #734d40,
    Ice: #72d0fc,
    mana: #c34f9e,
    orion: #a7635c,
    flesh: #a96558,
    arcane: #19a3d7,
    zepyron: #5e42b1,
    shadow: #4b4a49,
    turtle: #5f5143,
    darkness: #454561,
    poverty: #4a4440,
    thorn: #4e3740,
    thunder: #dfad27,
    demonic: #812f38,
    unchained: #9a9fc0,
    berserker: #48473f,
    cursed: #3e3155,
    royal: #007as0,
    vampire: #ab284a,
    jade: #00a793,
    chromalure: #37994d,
    celestial: #be4193,
    cataclysm: #927c67,
    magma: #e25900,
    legacy: #fdf0b1
    
"""