import logging
import cv2
import os
import easyocr
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process
from utils import capture_screen
import numpy as np

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def scrape_map_names():
    """
    Scrape all map names from the Bloons TD 6 Maps category on the Bloons Fandom website.
    :return: List of map names.
    """
    url = "https://bloons.fandom.com/wiki/Category:Bloons_TD_6_Maps"
    logging.info(f"Scraping map names from {url}...")

    response = requests.get(url)
    if response.status_code != 200:
        logging.error(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    map_names = set()

    # Extract all map links and titles
    for a_tag in soup.find_all("a", {"class": "category-page__member-link"}):
        map_name = a_tag.text.strip()
        if map_name:  # Ensure it's not empty
            map_names.add(map_name.upper())  # Uppercase for uniformity

    map_names = list(map_names)
    logging.info(f"Scraped {len(map_names)} map names.")
    return map_names


def preprocess_image(image):
    """
    Preprocess the image for OCR.
    :param image: Image to process.
    :return: Preprocessed image.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    resized = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    return resized


def fuzzy_match(detected_name, map_names):
    """
    Match the detected name to the closest name in the map list using fuzzy matching.
    :param detected_name: Name detected via OCR.
    :param map_names: List of official map names.
    :return: Best match and confidence score.
    """
    match, score = process.extractOne(detected_name, map_names, scorer=fuzz.token_sort_ratio)
    return match, score


def detect_map_names(map_names, save_tmp=True):
    """
    Detect map names on the current screen and match them to the official list.
    :param map_names: List of official map names.
    :param save_tmp: Whether to save cropped images for debugging.
    """
    logging.info("Capturing the current screen...")
    full_screen = capture_screen()
    preprocessed_screen = preprocess_image(full_screen)

    # Create tmp folder to save regions
    tmp_folder = "tmp"
    if save_tmp and not os.path.exists(tmp_folder):
        os.makedirs(tmp_folder)

    # Define map slots
    screen_height, screen_width = preprocessed_screen.shape
    map_slots = [
        (0.17 * screen_width, 0.1 * screen_height, 0.38 * screen_width, 0.155 * screen_height),   # Top-left
        (0.405 * screen_width, 0.1 * screen_height, 0.6 * screen_width, 0.155 * screen_height),  # Top-middle
        (0.61 * screen_width, 0.1 * screen_height, 0.85 * screen_width, 0.145 * screen_height),  # Top-right
        (0.17 * screen_width, 0.4 * screen_height, 0.38 * screen_width, 0.455 * screen_height),  # Bottom-left
        (0.405 * screen_width, 0.4 * screen_height, 0.6 * screen_width, 0.455 * screen_height),  # Bottom-middle
        (0.61 * screen_width, 0.4 * screen_height, 0.85 * screen_width, 0.445 * screen_height)   # Bottom-right
    ]

    detected_names = []

    for idx, (x1, y1, x2, y2) in enumerate(map_slots):
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        map_region = preprocessed_screen[y1:y2, x1:x2]

        # Save for debugging
        if save_tmp:
            region_path = os.path.join(tmp_folder, f"map_slot_{idx + 1}.png")
            cv2.imwrite(region_path, map_region)
            logging.info(f"Saved map slot {idx + 1} to {region_path}")

        # Perform OCR
        result = reader.readtext(map_region, detail=0)
        detected_text = " ".join(result).strip().upper()
        if not detected_text:
            detected_text = "UNKNOWN"

        # Fuzzy match the detected name
        best_match, confidence = fuzzy_match(detected_text, map_names)
        detected_names.append((detected_text, best_match, confidence))

        logging.info(f"Slot {idx + 1} | Detected: {detected_text} | Matched: {best_match} (Confidence: {confidence}%)")

    # Log the final detected names
    logging.info("\n===== Final Results =====")
    for idx, (detected, matched, confidence) in enumerate(detected_names):
        logging.info(f"Slot {idx + 1}: Detected: {detected} | Matched: {matched} | Confidence: {confidence}%")


if __name__ == "__main__":
    # Step 1: Scrape map names
    official_map_names = scrape_map_names()

    # Step 2: Detect map names and match them to official names
    if official_map_names:
        detect_map_names(official_map_names)
    else:
        logging.error("No map names were scraped. Exiting.")
