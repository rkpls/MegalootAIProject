import cv2
import json
import numpy as np
import os

def load_image(image_path):
    return cv2.imread(image_path)

def extract_pixel_colors(image):
    # Reshape the image data for JSON serialization
    return image.reshape(-1, 3).tolist()

def create_image_from_colors(colors, image_size=(16, 16)):
    # Reconstruct the image from flat RGB values
    image_array = np.array(colors, dtype=np.uint8).reshape(image_size[0], image_size[1], 3)
    return image_array

def crop_center(image, new_size=(12, 12)):
    # Calculate the coordinates to crop the image to the new size centered
    start_x = (image.shape[1] - new_size[0]) // 2
    start_y = (image.shape[0] - new_size[1]) // 2
    return image[start_y:start_y + new_size[1], start_x:start_x + new_size[0]]

def process_icons(image, num_cols, num_rows, icon_width, icon_height, output_dir):
    icons_data = {}
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Create directory if it doesn't exist
    
    for i in range(num_cols):
        for j in range(num_rows):
            x = i * icon_width
            y = j * icon_height
            icon = image[y:y+icon_height, x:x+icon_width]
            icon_resized = cv2.resize(icon, (16, 16))  # Resize icon to 16x16 pixels
            icon_cropped = crop_center(icon_resized, (12, 12))  # Crop the icon to 12x12 pixels
            pixel_colors = extract_pixel_colors(icon_cropped)
            icon_id = f'icon_{j*num_cols + i}'
            icons_data[icon_id] = {'colors': pixel_colors}
            # Save individual icon image
            icon_image = create_image_from_colors(pixel_colors, (12, 12))
            cv2.imwrite(os.path.join(output_dir, f'{icon_id}.png'), icon_image)
    return icons_data

def save_data_to_json(data, json_path):
    with open(json_path, 'w') as json_file:
        json.dump(data, json_file, separators=(',', ':'))

# Load the image
image_path = '50commonitems_1.png'
image = load_image(image_path)

# Assuming dimensions and grid layout need to be defined
num_cols, num_rows = 10, 5  # Example grid layout
icon_width, icon_height = image.shape[1] // num_cols, image.shape[0] // num_rows

# Process icons and extract data
output_directory = 'data/icons'
icons_data = process_icons(image, num_cols, num_rows, icon_width, icon_height, output_directory)

# Save data to JSON
json_path = 'data/50iconcolorscommon1.json'
save_data_to_json(icons_data, json_path)

print(f"Data saved to {json_path}")
print(f"Individual icons saved in {output_directory}")
