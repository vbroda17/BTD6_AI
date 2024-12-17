import numpy as np
import time
import logging
from utils import *
from exceptions import *
from paths import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Functions for certain use cases
def is_desktop_visible():
    """
    Check if the desktop is visible.
    :raises DesktopNotVisibleException: If the desktop is not visible.
    :return: True if the desktop is visible.
    """
    logging.info("Checking if the desktop is visible...")
    if not screen_check_with_spin(DESKTOP_TEMPLATE_PATH, duration=5, interval=0.1):
        raise DesktopNotVisibleException()
    logging.info("Desktop detected.")
    return True

def click_btd6_icon():
    """
    Find and double-click the BTD6 desktop icon.
    """
    logging.info("Attempting to click the BTD6 desktop icon...")
    click_item_with_spin(BTD6_ICON_PATH, duration=5, interval=0.1, threshold=0.8, clicks=2)
    logging.info("Successfully clicked the BTD6 desktop icon.")

def wait_for_start(timeout=60, check_interval=2):
    """
    Wait for the game to launch and display the start screen.
    :param timeout: Maximum time to wait for the start screen (in seconds).
    :param check_interval: Time interval between checks (in seconds).
    :raises GameLaunchTimeoutException: If the start screen does not appear within the timeout period.
    """
    logging.info("Waiting for the game to launch...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if check_start_screen():
                logging.info("Start screen detected. Game is ready.")
                return
            else:
                logging.info("Start screen not detected yet.")
        except TemplateMatchException as e:
            logging.warning(f"Screen check failed: {e}")

        time.sleep(check_interval)

    raise GameLaunchTimeoutException("Start screen did not appear within the timeout period.")

def click_start_button(threshold=0.8, duration=0.5):
    """
    Verify the start screen and click the 'Start' button.
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :param duration: Time in seconds for the mouse to move to the button (default: 0.5).
    :raises TemplateMatchException: If the start screen is not detected.
    :raises ButtonNotFoundException: If the 'Start' button is not found on the screen.
    """
    logging.info("Attempting to click the 'Start' button...")
    # Verify the start screen
    if not check_start_screen(threshold):
        raise TemplateMatchException(START_BUTTON_TEMPLATE_PATH, 0, threshold)

    # Click the 'Start' button
    click_item_with_spin(START_BUTTON_TEMPLATE_PATH, duration=5, interval=0.1, threshold=threshold, duration_click=duration)
    logging.info("Successfully clicked the 'Start' button.")

# Specific holder functions
def start_btd6():
    """
    Full workflow to start BTD6, from desktop detection to game setup.
    """
    logging.info("Starting BTD6...")
    try:
        # Standard workflow
        is_desktop_visible()  # Step 1: Verify desktop is visible
        click_btd6_icon()     # Step 2: Launch the BTD6 application
        wait_for_start()      # Step 3: Wait for the game to load to the start screen
        click_start_button()  # Step 4: Click the 'Start' button on the start screen
        wait_for_loading_screen_to_finish()  # Step 5: Wait for the loading screen to disappear
        check_daily_reward()  # Step 6: Collect daily rewards if available
        # Future steps:
        # elif is_btd6_launched(): 
        #   sync_game_and_script()  # This will sync if the game is already running or at a different menu

    except DesktopNotVisibleException as e:
        logging.error(f"Error: {e}")
        exit(1)

    except ButtonNotFoundException as e:
        logging.error(f"Error: {e}")
        exit(1)

    except GameLaunchTimeoutException as e:
        logging.error(f"Error: {e}")
        exit(1)

    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        exit(1)
    logging.info("BTD6 started...")

if __name__ == "__main__":
    start_btd6()
