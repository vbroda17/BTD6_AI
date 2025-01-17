import logging
import time
import sys
import os
import pytesseract

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from scripts.minor.utils import *
from scripts.minor.paths import *
from scripts.minor.hero_classes import *
from scripts.minor.enums import UserInputMode, HeroStatus

HERO_LIST_PATH = "txts/heros.txt"  # File path to hero names
OCR_NAME_REGION = (50, 150, 400, 800)  # Default region for detecting hero name
STATUS_REGION = (400, 500, 700, 850)  # Default region for detecting status

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


def click_through_heroes(heroes):
    # """
    # Click through all heroes in the list and validate their names dynamically.

    # Args:
    #     heroes (list[str]): List of hero names.

    # Returns:
    #     None
    # """
    # for idx, hero_name in enumerate(heroes):
    #     logging.info(f"Clicking hero {idx + 1}: {hero_name}")
    #     if idx == 0:
    #         click_first_hero()  # Click the first hero icon
    #     else:
    #         click_next_hero()  # Click the next hero icon

    #     # Validate the name using OCR
    #     detected_name = check_current_name()
    #     if detected_name == hero_name:
    #         logging.info(f"Validated hero name: {detected_name}")
    #     else:
    #         logging.warning(f"Hero name mismatch! Expected: {hero_name}, Detected: {detected_name}")
  pass

def select_hero_by_number(heroes, number):
  # """
  # Select a hero based on the number provided by the user.

  # Args:
  #     heroes (list[str]): List of hero names.
  #     number (int): The number corresponding to the hero in the list.

  # Returns:
  #     str: The name of the selected hero.
  # """
  # if number < 1 or number > len(heroes):
  #     logging.error("Invalid hero number. Please select a valid number.")
  #     return None

  # selected_hero = heroes[number - 1]
  # logging.info(f"Selected hero: {selected_hero}")

  # # Navigate to the selected hero
  # click_through_heroes(heroes[:number])
  # return selected_hero
  pass

def check_current_name():
    """
    Use OCR to detect the hero name at the top middle of the screen.

    Returns:
        str: Detected hero name, or None if not detected.
    """
    screenshot = capture_screen(debug=True)
    y1, y2, x1, x2 = OCR_NAME_REGION
    name_region = screenshot[y1:y2, x1:x2]
    gray = cv2.cvtColor(name_region, cv2.COLOR_BGR2GRAY)
    detected_name = pytesseract.image_to_string(gray, config="--psm 7").strip()

    logging.info(f"Detected hero name: {detected_name}")
    return detected_name


def check_current_status():
    # """
    # Detect the current hero's status (Selectable, Selected, or Locked).

    # Returns:
    #     HeroStatus: The detected status.
    # """
    # screenshot = capture_screen(debug=True)
    # y1, y2, x1, x2 = STATUS_REGION
    # button_region = screenshot[y1:y2, x1:x2]
    # gray = cv2.cvtColor(button_region, cv2.COLOR_BGR2GRAY)

    # if check_segment(BUTTONS_BUTTONSELECT, debug=True):
    #     return HeroStatus.SELECTABLE
    # elif check_segment(BUTTONS_BUTTONSELECTED, debug=True):
    #     return HeroStatus.SELECTED
    # elif check_segment(BUTTONS_BUTTONLOCKED, debug=True):
    #     return HeroStatus.LOCKED
    # return None
  pass

if __name__ == "__main__":
    heroes = load_hero_list(HERO_LIST_PATH)
    if not heroes:
        logging.error("No heroes loaded. Exiting.")
        exit(1)

    # Display hero list and prompt user for selection
    display_hero_list(heroes)
    check_current_name()
    # try:
    #     hero_number = int(input("Enter the number of the hero to select: "))
    #     select_hero_by_number(heroes, hero_number)

    #     # Detect hero status
    #     status = check_current_status()
    #     logging.info(f"Hero status: {status}")
    # except ValueError:
    #     logging.error("Invalid input. Please enter a valid number.")
