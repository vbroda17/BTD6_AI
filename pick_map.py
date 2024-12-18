import logging
import pyautogui
import random
from utils import *
from paths import *
from maps import maps_by_screen  # Import the maps_by_screen directly
import time

# Screen grid positions for map slots
MAP_POSITIONS = [
    (0.17, 0.1, 0.38, 0.155),  # Top-left
    (0.405, 0.1, 0.6, 0.155),  # Top-middle
    (0.61, 0.1, 0.85, 0.145),  # Top-right
    (0.17, 0.4, 0.38, 0.455),  # Bottom-left
    (0.405, 0.4, 0.6, 0.455),  # Bottom-middle
    (0.61, 0.4, 0.85, 0.445)   # Bottom-right
]

def click_play_button():
    """Ensure the game is on MAIN MENU and click 'Play'."""
    logging.info("Ensuring the game is on MAIN MENU screen...")
    screen_check_with_spin(MAIN_MENU_TEMPLATE_PATH, duration=5, interval=0.1)
    click_item_with_spin(PLAY_BUTTON_TEMPLATE_PATH, duration=5, interval=0.1)
    logging.info("Clicked the 'Play' button.")

def click_return_button():
    """Click the 'Return' button to exit map selection."""
    logging.info("Clicking 'Return' button to exit map selection.")
    click_item_with_spin(RETURN_BUTTON_TEMPLATE_PATH, duration=3, interval=0.1)

def reset_to_screen_one():
    """Reset to Screen 1 by clicking Intermediate and then Beginner."""
    logging.info("Resetting to Screen 1...")
    click_item_with_spin(BUTTON_INTERMEDIATE, duration=3, interval=0.1)
    time.sleep(0.5)
    click_item_with_spin(BUTTON_BEGINNER, duration=3, interval=0.1)
    time.sleep(0.5)
    logging.info("Screen reset to Screen 1.")

def navigate_to_screen(target_screen):
    """Navigate to the target screen by clicking the right arrow button."""
    logging.info(f"Navigating to Screen {target_screen}...")
    for _ in range(target_screen - 1):
        click_item_with_spin(RIGHT_ARROW_TEMPLATE_PATH, duration=2, interval=0.5)
        time.sleep(0.5)
    logging.info(f"Reached Screen {target_screen}.")

def click_map(slot_index, screen_width, screen_height):
    """Click the map at the specified slot index."""
    x1, y1, x2, y2 = MAP_POSITIONS[slot_index]
    x = int((x1 + x2) / 2 * screen_width)
    y = int((y1 + y2) / 2 * screen_height)
    pyautogui.moveTo(x, y, duration=0.5)
    pyautogui.click()
    logging.info(f"Clicked on map slot {slot_index + 1} at position ({x}, {y}).")

def pick_map():
    """
    Full workflow to reset to screen one, navigate to the correct screen, and pick a map.
    Allows user to input a specific map name, "random" for any random map, or "random <difficulty>" for a random map in a specific difficulty.
    Returns the selected map name.
    """
    logging.info("Starting the 'Pick Map' workflow...")
    try:
        # Click play button first
        click_play_button()

        # Ask the user for map input
        user_input = input("Enter the name of the map to pick (or 'random'/'random <difficulty>'): ").strip()

        # Determine the target map based on user input
        target_map = None
        if user_input.lower().startswith("random"):
            difficulty = user_input[7:].strip().upper() if len(user_input) > 6 else None

            if difficulty:
                # Random map within a specific difficulty
                eligible_maps = [(map_name, diff) for screen in maps_by_screen for map_name, diff in screen if diff == difficulty]
                if not eligible_maps:
                    logging.error(f"No maps found for difficulty '{difficulty}'.")
                    click_return_button()
                    return None
                target_map, _ = random.choice(eligible_maps)
            else:
                # Random map from any difficulty
                all_maps = [(map_name, diff) for screen in maps_by_screen for map_name, diff in screen]
                target_map, _ = random.choice(all_maps)
        else:
            target_map = user_input

        # Reset to screen one
        reset_to_screen_one()

        # Find the screen and position of the target map
        target_screen = None
        target_position = None
        for screen_num, screen_maps in enumerate(maps_by_screen, 1):
            for idx, (map_name, _) in enumerate(screen_maps):
                if map_name.upper() == target_map.upper():
                    target_screen = screen_num
                    target_position = idx
                    break
            if target_screen:
                break

        if target_screen is None or target_position is None:
            logging.error(f"Map '{target_map}' not found.")
            click_return_button()
            return None

        # Navigate to the correct screen and click the map
        navigate_to_screen(target_screen)
        screen_width, screen_height = pyautogui.size()
        click_map(target_position, screen_width, screen_height)

        logging.info(f"Successfully selected map '{target_map}'.")
        return target_map
    except Exception as e:
        logging.error(f"Error occurred during 'Pick Map' workflow: {e}")
        click_return_button()
        return None

if __name__ == "__main__":
    selected_map = pick_map()
    if selected_map:
        print(f"Map selected: {selected_map}")
    else:
        print("No map was selected.")
