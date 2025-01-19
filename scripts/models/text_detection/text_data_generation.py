import os
import random
import json
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

# Paths
TXT_FOLDER = "texts"
DATASET_FOLDER = "datasets/text"
IMAGES_FOLDER = os.path.join(DATASET_FOLDER, "images")
METADATA_FILE = os.path.join(DATASET_FOLDER, "metadata.json")
FONT_PATH = "fonts/LuckiestGuy-Regular.ttf"

# Helper Functions
def random_color():
    """Generate a random color (RGB)."""
    return tuple(random.randint(0, 255) for _ in range(3))

def generate_random_non_black_color():
    """Generate a random RGB color that is not black."""
    while True:
        color = random_color()
        if color != (0, 0, 0):
            return color

def generate_random_gradient(width, height):
    """Generate a random gradient for the background."""
    start_color = generate_random_non_black_color()
    end_color = generate_random_non_black_color()
    gradient = Image.new("RGB", (width, height))
    for y in range(height):
        for x in range(width):
            r = int(start_color[0] + (end_color[0] - start_color[0]) * (x / width))
            g = int(start_color[1] + (end_color[1] - start_color[1]) * (x / width))
            b = int(start_color[2] + (end_color[2] - start_color[2]) * (x / width))
            gradient.putpixel((x, y), (r, g, b))
    return gradient

def apply_augmentations(image):
    """Apply random augmentations to an image."""
    if random.random() < 0.4:
        image = image.filter(ImageFilter.GaussianBlur(random.uniform(0, 2)))
    if random.random() < 0.4:
        image = ImageOps.solarize(image, threshold=random.randint(50, 200))
    if random.random() < 0.4:
        image = ImageOps.invert(image)
    if random.random() < 0.4:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(random.uniform(0.5, 1.5))
    return image

def generate_text_image_smaller(text, font_path, output_path, black_only_outline=True, mode="variable"):
    """
    Generate an image with the given text in smaller, scaled style.

    Args:
        text (str): The text to render.
        font_path (str): Path to the .ttf font file.
        output_path (str): Path to save the generated image.
        black_only_outline (bool): Whether to use only black for the text outline.
        mode (str): Mode of text placement ("variable" or "full").
    """
    # Randomize font size
    base_font_size = random.randint(40, 80)
    font = ImageFont.truetype(font_path, base_font_size)

    # Calculate text size
    temp_image = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Add padding and random scaling
    padding = 40
    max_shift = 30
    text_width += padding * 2 + max_shift
    text_height += padding * 2 + max_shift

    # Ensure enough space for rotation
    max_rotation = 5  # Reduced rotation angle
    diag = int((text_width**2 + text_height**2)**0.5)
    canvas_width = diag + padding
    canvas_height = diag + padding

    if mode == "full":
        canvas_width = text_width + padding * 2
        canvas_height = text_height + padding * 2

    # Create canvas with gradient background
    background = generate_random_gradient(canvas_width, canvas_height)
    image = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
    image.paste(background)
    draw = ImageDraw.Draw(image)

    # Random text position
    shift_x = random.randint(0, max_shift)
    shift_y = random.randint(0, max_shift)
    x = (canvas_width - text_width) // 2 + (shift_x if mode == "variable" else 0)
    y = (canvas_height - text_height) // 2 + (shift_y if mode == "variable" else 0)

    # Draw text outline
    # outline_color = (0, 0, 0) if black_only_outline else generate_random_non_black_color()
    outline_color = (0, 0, 0)
    for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=outline_color)

    # Fill the text
    draw.text((x, y), text, font=font, fill=generate_random_non_black_color())

    # Rotate image
    angle = random.uniform(-max_rotation, max_rotation)
    image = image.rotate(angle, expand=True, fillcolor=(255, 255, 255))

    # Apply augmentations
    image = apply_augmentations(image)

    # Save image
    image.save(output_path)

def generate_text_image_larger(text, font_path, output_path, black_only_outline=True, mode="variable"):
    """
    Generate an image with the given text in larger style.

    Args:
        text (str): The text to render.
        font_path (str): Path to the .ttf font file.
        output_path (str): Path to save the generated image.
        black_only_outline (bool): Whether to use only black for the text outline.
        mode (str): Mode of text placement ("variable" or "full").
    """
    # Randomize font size
    base_font_size = random.randint(40, 80)
    font = ImageFont.truetype(font_path, base_font_size)

    # Calculate text size
    temp_image = Image.new("RGB", (1, 1))
    temp_draw = ImageDraw.Draw(temp_image)
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

    # Add padding
    padding = 20
    canvas_width = text_width + padding * 2
    canvas_height = text_height + padding * 2

    if mode == "variable":
        extra_whitespace = random.randint(0, text_width)
        canvas_width += extra_whitespace

    # Create the canvas
    background = generate_random_gradient(canvas_width, canvas_height)
    image = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
    image.paste(background)
    draw = ImageDraw.Draw(image)

    x = (canvas_width - text_width) // 2
    y = (canvas_height - text_height) // 2

    # Draw text outline
    # outline_color = (0, 0, 0) if black_only_outline else generate_random_non_black_color()
    outline_color = (0, 0, 0)
    for offset in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:
        draw.text((x + offset[0], y + offset[1]), text, font=font, fill=outline_color)

    # Fill the text
    draw.text((x, y), text, font=font, fill=generate_random_non_black_color())

    # Rotate image
    angle = random.uniform(-5, 5)
    image = image.rotate(angle, expand=True, fillcolor=(255, 255, 255))

    # Apply augmentations
    image = apply_augmentations(image)

    # Save image
    image.save(output_path)

def build_dataset(smaller_ratio=0.5, mode_ratio=0.5):
    """
    Build a dataset of text images and metadata.

    Args:
        smaller_ratio (float): Proportion of images generated by `generate_text_image_smaller`.
        mode_ratio (float): Proportion of "variable" mode (vs. "full").
    """
    os.makedirs(IMAGES_FOLDER, exist_ok=True)
    metadata = []

    for txt_file in os.listdir(TXT_FOLDER):
        if txt_file.endswith(".txt"):
            txt_path = os.path.join(TXT_FOLDER, txt_file)
            with open(txt_path, "r") as f:
                for line in f:
                    text = line.strip()
                    if text:
                        for i in range(50):
                            filename = f"{text.replace(' ', '_')}_{i}.png"
                            output_path = os.path.join(IMAGES_FOLDER, filename)

                            if random.random() < smaller_ratio:
                                generate_text_image_smaller(
                                    text, FONT_PATH, output_path, mode="variable" if random.random() < mode_ratio else "full"
                                )
                            else:
                                generate_text_image_larger(
                                    text, FONT_PATH, output_path, mode="variable" if random.random() < mode_ratio else "full"
                                )

                            metadata.append({"file_name": filename, "text": text})

    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=4)
    print(f"Dataset created with {len(metadata)} entries.")

if __name__ == "__main__":
    build_dataset()
