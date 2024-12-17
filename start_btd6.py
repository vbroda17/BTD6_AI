import time
import logging
from utils import *
from exceptions import *
from paths import *
from enums import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def is_desktop_visible():
    """
    Check if the desktop is visible.
    :raises DesktopNotVisibleException: If the desktop is not visible.
    :return: True if the desktop is visible.
    """
    logging.info("Checking if the desktop is visible...")
    if not wait_for_screen(DESKTOP_TEMPLATE_PATH, timeout=5, interval=0.1):
        raise DesktopNotVisibleException("Desktop not detected.")
    logging.info("Desktop detected.")
    return True


def click_btd6_icon():
    """
    Find and double-click the BTD6 desktop icon.
    """
    logging.info("Attempting to click the BTD6 desktop icon...")
    click_item_with_spin(BTD6_ICON_PATH, duration=5, interval=0.1, threshold=0.8, clicks=2)
    logging.info("Successfully clicked the BTD6 desktop icon.")


def wait_for_start_screen():
    """
    Wait for the start screen to appear.
    :raises GameLaunchTimeoutException: If the start screen does not appear within the timeout period.
    """
    logging.info("Waiting for the start screen to appear...")
    if not wait_for_screen(START_SCREEN_TEMPLATE_PATH, timeout=60, interval=0.5):
        raise GameLaunchTimeoutException("Start screen did not appear within the timeout period.")
    logging.info("Start screen detected.")


def click_start_button(threshold=0.8, duration=0.5):
    """
    Verify the start screen and click the 'Start' button.
    :param threshold: Confidence threshold for template matching.
    :param duration: Mouse move duration in seconds.
    """
    logging.info("Attempting to click the 'Start' button...")
    click_item_with_spin(START_BUTTON_TEMPLATE_PATH, duration=5, interval=0.1, threshold=threshold, duration_click=duration)
    logging.info("Successfully clicked the 'Start' button.")


def wait_for_main_menu():
    """
    Wait for the main menu screen to appear.
    :raises GameLaunchTimeoutException: If the main menu does not appear within the timeout period.
    """
    logging.info("Waiting for the main menu screen to appear...")
    if not wait_for_screen(MAIN_MENU_TEMPLATE_PATH, timeout=30, interval=0.5):
        raise GameLaunchTimeoutException("Main menu screen did not appear within the timeout period.")
    logging.info("Main menu screen detected.")


# Specific holder functions
def start_btd6():
    """
    Full workflow to start BTD6, from desktop detection to game setup.
    """
    logging.info("Starting BTD6...")
    try:
        # Step 1: Verify desktop is visible
        is_desktop_visible()

        # Step 2: Launch the BTD6 application
        click_btd6_icon()

        # Step 3: Wait for the game to load to the start screen
        wait_for_start_screen()

        # Step 4: Click the 'Start' button
        click_start_button()

        # Step 5: Wait for the main menu screen to appear
        wait_for_main_menu()

        # Step 6: Collect daily rewards if available
        check_daily_reward()

        # Future steps:
        # elif is_btd6_launched(): 
        #   sync_game_and_script()

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

    logging.info("BTD6 successfully started and initialized.")


if __name__ == "__main__":
    start_btd6()
