import json
from icon_processor import IconProcessor

def load_json_data(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def colors_are_close(color1, color2, tolerance=10):
    return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))

def compare_icon_data(new_data, stored_data, tolerance=10):
    matches = 0
    for icon_id in new_data:
        if icon_id in stored_data:
            all_colors_match = True
            for new_color, stored_color in zip(new_data[icon_id]['colors'], stored_data[icon_id]['colors']):
                if not colors_are_close(new_color, stored_color, tolerance):
                    all_colors_match = False
                    break
            if all_colors_match:
                matches += 1
    return matches

# Initialize the IconProcessor with the specific image and grid layout
processor = IconProcessor('Itemtest3x2.png', 3, 2)
current_icon_data = processor.process_icons()

# Load the previously stored data from JSON file
stored_icon_data = load_json_data('iconcolors.json')

# Compare the current data with the stored data and count matches with a tolerance
match_count = compare_icon_data(current_icon_data, stored_icon_data)

# Output the result
print(f"Number of matching icons: {match_count}")
