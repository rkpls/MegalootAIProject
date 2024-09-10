
import cv2
import numpy as np
import os

class IconProcessor:
    def __init__(self, image_path, num_cols, num_rows):
        self.image_path = image_path
        self.num_cols = num_cols
        self.num_rows = num_rows
        self.image = self.load_image(image_path)
        self.icon_width = self.image.shape[1] // num_cols
        self.icon_height = self.image.shape[0] // num_rows

    def load_image(self, image_path):
        return cv2.imread(image_path)

    def extract_pixel_colors(self, image):
        return image.reshape(-1, 3).tolist()

    def crop_center(self, image, new_size=(12, 12)):
        start_x = (image.shape[1] - new_size[0]) // 2
        start_y = (image.shape[0] - new_size[1]) // 2
        return image[start_y:start_y + new_size[1], start_x:start_x + new_size[0]]

    def process_icons(self):
        icons_data = {}
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                x = i * self.icon_width
                y = j * self.icon_height
                icon = self.image[y:y+self.icon_height, x:x+self.icon_width]
                icon_resized = cv2.resize(icon, (16, 16))  # Resize icon to 16x16 pixels
                icon_cropped = self.crop_center(icon_resized, (12, 12))  # Crop the icon to 12x12 pixels
                pixel_colors = self.extract_pixel_colors(icon_cropped)
                icon_id = f'icon_{j*self.num_cols + i}'
                icons_data[icon_id] = {'colors': pixel_colors}
        return icons_data
