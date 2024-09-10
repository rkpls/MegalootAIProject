from colors import ColorDetector
from screen_capture import ScreenCapture
import time

if __name__ == "__main__":
    # Set up paths and components
    screenshot_folder = "C:\\Users\\rikop\\Desktop\\megaloot\\screenshots"
    color_detector = ColorDetector()
    screen_capture = ScreenCapture(screenshot_folder)

    while True:
        if screen_capture.is_megaloot_in_focus():
            print("Megaloot is in focus, capturing items...")
            screen = screen_capture.capture(save=True)  # Save the screenshot for comparison

            # Get item coordinates (equipped, inventory, shop)
            equipped_coords, inventory_coords, shop_coords = screen_capture.get_item_coordinates()

            # Collect all coordinates for marking pink spots
            all_coords = equipped_coords + inventory_coords + shop_coords

            # Process all items
            for coord in all_coords:
                x, y = coord
                pixel_color = screen_capture.get_single_pixel_color(screen, x, y)
                rarity = color_detector.detect_rarity(pixel_color)
                print(f"Item at ({x}, {y}) is of rarity: {rarity}")

            # Mark the pink spots on all items and save the modified screenshot
            marked_img = screen_capture.mark_pixels_on_items(screen, all_coords)
            marked_screenshot_path = f"{screenshot_folder}/marked_screenshot.png"
            screen_capture.save_screenshot(marked_screenshot_path, marked_img)

        else:
            print("Megaloot is not in focus, waiting...")

        time.sleep(5)  # Adjust the interval as needed
