import logging
import time
import sys
import os
import tensorflow as tf
import numpy as np
from PIL import Image
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.minor.utils import *
from scripts.minor.paths import *
from scripts.minor.hero_classes import *
from scripts.minor.enums import UserInputMode, HeroStatus

# Paths and constants
HERO_LIST_PATH = "txts/heros.txt"  # File path to hero names
OCR_NAME_REGION = (50, 150, 400, 800)  # Default region for detecting hero name
STATUS_REGION = (400, 500, 700, 850)  # Default region for detecting status
MODEL_PATH = "datasets/txt/text_recognition_model.h5"  # Path to the trained model
logging.basicConfig(level=logging.INFO)


def load_hero_list(file_path):
    """
    Load the list of hero names from a file.

    Args:
        file_path (str): Path to the hero list file.

    Returns:
        list[str]: List of hero names.
    """
    if not os.path.exists(file_path):
        logging.error(f"Hero list file not found: {file_path}")
        return []

    with open(file_path, "r") as f:
        heroes = [line.strip() for line in f.readlines()]
    logging.info(f"Loaded {len(heroes)} heroes from file.")
    return heroes


def display_hero_list(heroes):
    """
    Display the hero list with numbers for user selection.

    Args:
        heroes (list[str]): List of hero names.
    """
    print("\n=== Hero List ===")
    for idx, hero in enumerate(heroes, start=1):
        print(f"{idx}. {hero}")
    print("=================")


def preprocess_image(image):
    """
    Preprocess the image for the model.

    Args:
        image (np.array): Cropped image array.

    Returns:
        np.array: Preprocessed image with 3 channels (RGB).
    """
    img = Image.fromarray(image).convert("RGB")  # Ensure the image has 3 channels (RGB)
    img = img.resize((256, 64))  # Resize to match the model input size
    img = np.array(img) / 255.0  # Normalize pixel values to [0, 1]
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img



def load_model(model_path):
    """
    Load the trained model.

    Args:
        model_path (str): Path to the saved model file.

    Returns:
        tf.keras.Model: Loaded model.
    """
    try:
        model = tf.keras.models.load_model(model_path)
        logging.info(f"Model loaded from {model_path}")
        return model
    except Exception as e:
        logging.error(f"Failed to load model: {e}")
        exit(1)


def check_current_name(model, label_to_name, debug=False):
    """
    Detect the hero name using the trained model.

    Args:
        model (tf.keras.Model): Trained CNN model.
        label_to_name (dict): Mapping of label indices to hero names.
        debug (bool): If True, save a debug image with the name region highlighted.

    Returns:
        str: Detected hero name, or None if not detected.
    """
    # Capture the screen
    screenshot = capture_screen(debug=True)
    height, width, _ = screenshot.shape

    # Adjust region size
    vertical_scale = 0.07
    horizontal_scale = 0.4
    vertical_offset = 50 / height
    horizontal_offset = 50

    # Calculate region dimensions
    region_height = int(height * vertical_scale)
    region_width = int(width * horizontal_scale)
    y1 = int(height * vertical_offset) - 10  # Move region up by 10 pixels
    y2 = y1 + region_height
    center_x = width // 2
    x1 = center_x - region_width // 2 + horizontal_offset + 45
    x2 = center_x + region_width // 2 + horizontal_offset

    # Crop the region
    name_region = screenshot[y1:y2, x1:x2]

    # Preprocess the cropped region
    preprocessed_image = preprocess_image(name_region)

    # Predict using the model
    predictions = model.predict(preprocessed_image)
    predicted_label = np.argmax(predictions, axis=-1)[0]

    # Get the corresponding hero name
    detected_name = label_to_name.get(predicted_label, "Unknown")

    if debug:
        debug_image = screenshot.copy()
        cv2.rectangle(debug_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        debug_path = "debug_name_region.png"
        cv2.imwrite(debug_path, debug_image)
        logging.info(f"Debug image saved to {debug_path}")

    logging.info(f"Detected hero name: {detected_name}")
    return detected_name


def check_current_status():
    """
    Detect the current hero's status (Selectable, Selected, or Locked).

    Returns:
        HeroStatus: The detected status.
    """
    screenshot = capture_screen(debug=True)
    y1, y2, x1, x2 = STATUS_REGION
    button_region = screenshot[y1:y2, x1:x2]
    gray = cv2.cvtColor(button_region, cv2.COLOR_BGR2GRAY)

    if check_segment(HEROES_SELECT, debug=True):
        return HeroStatus.SELECTABLE
    elif check_segment(HEROES_SELECTED, debug=True):
        return HeroStatus.SELECTED
    elif check_segment(HEROES_UNLOCK, debug=True):
        return HeroStatus.LOCKED
    return None


if __name__ == "__main__":
    # Load hero list
    heroes = load_hero_list(HERO_LIST_PATH)
    if not heroes:
        logging.error("No heroes loaded. Exiting.")
        exit(1)

    # Load the trained model
    model = load_model(MODEL_PATH)

    # Map hero names to indices
    label_to_name = {idx: hero for idx, hero in enumerate(heroes)}

    # Detect the current hero name
    detected_hero_name = check_current_name(model, label_to_name, debug=True)
    print(f"Detected Hero Name: {detected_hero_name}")

    # Check current status
    hero_status = check_current_status()
    print(f"Hero Status: {hero_status}")
