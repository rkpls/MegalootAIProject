import cv2

# Load the existing image
input_image_path = "image.png"  # Change to the correct image file
output_image_path = "output_image.png"

# Coordinates for the pink spots
coordinates = [
    (200, 840), (200, 1076), (200, 1312), (200, 1548), (434, 840), (434, 1076), (434, 1312), (434, 1548),

    (714, 840), (948, 840), (1182, 840), (1416, 840), (1650, 840),
    (714, 1074), (948, 1074), (1182, 1074), (1416, 1074), (1650, 1074),
    (714, 1308), (948, 1308), (1182, 1308), (1416, 1308), (1650, 1308),
    (714, 1544), (948, 1544), (1182, 1544), (1416, 1544), (1650, 1544),

    (600, 1956), (833, 1956), (1066, 1956), (1299, 1956)
]

# Load the image
image = cv2.imread(input_image_path)

# Check if image is loaded successfully
if image is None:
    raise FileNotFoundError(f"Image at {input_image_path} not found!")

# Define the color for the pink spot (BGR format in OpenCV)
pink_color = (203, 192, 255)  # OpenCV uses BGR instead of RGB

# Function to draw a pink spot (small 5x5 circle)
def draw_spot(image, x, y, color):
    cv2.circle(image, (x, y), 5, color, -1)  # Draw filled circle

# Place pink spots at the specified coordinates
for coord in coordinates:
    x, y = coord
    draw_spot(image, x, y, pink_color)

# Save the modified image as a copy
cv2.imwrite(output_image_path, image)
cv2.waitKey(0)
cv2.destroyAllWindows()
