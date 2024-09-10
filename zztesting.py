from PIL import Image

def extract_snippets(image_path, coords, snippet_size=(26, 26)):
    # Load the image
    image = Image.open(image_path)

    # List to hold the extracted images
    snippets = []

    # Extract snippets based on the provided coordinates
    for x, y in coords:
        # Define the bounding box for the snippet
        box = (x, y, x + snippet_size[0], y + snippet_size[1])
        snippet = image.crop(box)
        snippets.append(snippet)

        # Optionally save the snippet
        snippet.save(f"snippet_{x}_{y}.png")
        print(f"Snippet saved at ({x}, {y})")

    return snippets

# Coordinates from the user
coordinates = [(20, 127), (20, 166), (20, 205), (20, 244)]

# Path to the image file
image_path = "/mnt/data/image.png"

# Extract snippets
extract_snippets(image_path, coordinates)
