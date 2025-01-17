import logging
import time
import pytesseract
import cv2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.minor.utils import *
from scripts.minor.paths import *
from scripts.minor.enums import UserInputMode

logging.basicConfig(level=logging.INFO)

def  wait_for_heroes_screen():
    pass

def check_all_heroes():
    pass

def click_first_hero():
    pass

def click_next_hero():
    pass

def check_current_hero():
    pass

def extract_hero_name(screenshot, debug=False):
    """
    Extract the hero's name from the top middle field of the screenshot.

    Args:
        screenshot (numpy.ndarray): The captured screen.
        debug (bool): Whether to save the cropped image for debugging.

    Returns:
        str: The detected hero name.
    """
    # Crop the region containing the hero name (coordinates will depend on your screen resolution)
    # Adjust these coordinates based on your specific layout
    hero_name_region = screenshot[100:200, 500:1000]  # Example coordinates (y1:y2, x1:x2)

    if debug:
        cv2.imwrite("debug_hero_name_region.png", hero_name_region)

    # Convert the cropped region to grayscale for better OCR accuracy
    gray = cv2.cvtColor(hero_name_region, cv2.COLOR_BGR2GRAY)

    # Use pytesseract to extract text
    hero_name = pytesseract.image_to_string(gray, config="--psm 7").strip()

    logging.info(f"Extracted hero name: {hero_name}")
    return hero_name


def check_current_status():
    pass

def check_current_skin():
    pass    # THis one is actually being skipped now

if __name__ == "__main__":
    mode = UserInputMode.DEBUG
    if mode == UserInputMode.DEFAULT:
        pass
    elif mode == UserInputMode.GUIDED:
        pass
    elif mode == UserInputMode.FREE:
        pass
    elif mode == UserInputMode.DEBUG:
        logging.info("Starting hero scanner in debug mode...")
        extract_hero_name()
        logging.info("Finished with debugmode and program.")



