import cv2
import pytesseract
from PIL import Image
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


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
image_path = 'path/to/your/tooltip/image.png'
text, icons = extract_tooltip_data(image_path)
print("Detected Icons:")
print(icons)
