import pyautogui
import cv2
import numpy as np
import time
import logging
import os
import re
from exceptions import *
from paths import *
from enums import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def spin_until(condition_func, duration=5, interval=0.1, *args, **kwargs):
    """
    Generic spin function to repeatedly check a condition within a time limit.
    :param condition_func: The condition function to evaluate. Should return True or False.
    :param duration: Total time to spin (in seconds).
    :param interval: Time interval between checks (in seconds).
    :param args: Positional arguments to pass to the condition function.
    :param kwargs: Keyword arguments to pass to the condition function.
    :return: True if the condition is met within the duration, False otherwise.
    """
    start_time = time.time()

    while time.time() - start_time < duration:
        if condition_func(*args, **kwargs):
            return True  # Condition met
        time.sleep(interval)

    return False  # Timeout reached

def capture_screen():
    """Capture the current screen and return it as a NumPy array."""
    # logging.info("Capturing the current screen...")
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def validate_template_path(template_path):
    """
    Validate and load a template image from a given path.
    :param template_path: Path to the template image.
    :return: Loaded template image in grayscale.
    """
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"Template image not found at {template_path}")
    return template

def screen_check_once(screenshot, template_path, threshold=0.8):
    """
    Single check if a screen matches a given template.
    :param screenshot: Image of the current screen.
    :param template_path: Path to the template image.
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :raises TemplateMatchException: If the screen does not match the template.
    :return: True if the screen matches the template, False otherwise.
    """
    template = validate_template_path(template_path)
    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    if max_val < threshold:
        raise TemplateMatchException(template_path, max_val, threshold)
    return True

def screen_check_with_spin(template_path, duration=5, interval=0.1, threshold=0.8):
    """
    Spin function to repeatedly check if a screen matches a given template.
    :param template_path: Path to the template image.
    :param duration: Total time to spin (in seconds).
    :param interval: Time interval between checks (in seconds).
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :return: True if the screen matches the template, False otherwise.
    """
    def condition():
        screenshot = capture_screen()
        try:
            return screen_check_once(screenshot, template_path, threshold)
        except TemplateMatchException:
            return False

    return spin_until(condition, duration=duration, interval=interval)

def check_current_screen(threshold=0.8):
    """
    Check the current game screen and return the corresponding GameState.
    Sequentially checks screen templates and identifies the active state.
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :return: GameState enum representing the current screen.
    """
    logging.info("Checking the current game screen...")

    # Capture the current screen
    frame = capture_screen()

    # Define screens to check, in order of priority
    screen_checks = [
        (GameState.DESKTOP, DESKTOP_TEMPLATE_PATH),
        # (GameState.LAUNCHING, LOADING_GAME_TEMPLATE_PATH),
        (GameState.START, START_SCREEN_TEMPLATE_PATH),
        (GameState.MAIN_MENU, MAIN_MENUE_SCREEN_PATH),
    ]

    # Check each screen template
    for state, template_path in screen_checks:
        try:
            if screen_check_once(frame, template_path, threshold):
                logging.info(f"Screen detected: {state.name}")
                return state
        except TemplateMatchException:
            logging.debug(f"No match for {state.name} screen template: {template_path}")

    # If no screen matches, return UNKNOWN
    logging.warning("No matching screen detected. Returning UNKNOWN state.")
    return GameState.UNKNOWN

def click_button(template_path, threshold=0.8, duration=0.5, clicks=1):
    """
    Generalized function to find and click a button on the screen.
    :param template_path: Path to the button image template.
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :param duration: Time in seconds for the mouse to move to the button (default: 0.5).
    :param clicks: Number of clicks to perform (default: 1).
    :raises ButtonNotFoundException: If the button is not found on the screen.
    """
    frame = capture_screen()
    template = validate_template_path(template_path)
    screenshot_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        button_center = (max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2)
        pyautogui.moveTo(button_center[0], button_center[1], duration=duration)
        pyautogui.click(clicks=clicks)
        logging.info(f"Clicked the button at {template_path}.")
    else:
        raise ButtonNotFoundException(template_path, max_val)

def click_item_with_spin(template_path, duration=5, interval=0.1, threshold=0.8, duration_click=0.5, clicks=1):
    """
    Repeatedly check and click an item (e.g., button, chest) on the screen within a time limit.
    :param template_path: Path to the template image.
    :param duration: Total time to spin (in seconds).
    :param interval: Time interval between checks (in seconds).
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :param duration_click: Time in seconds for the mouse to move to the item (default: 0.5).
    :param clicks: Number of clicks to perform (default: 1).
    :return: True if the item is clicked, False otherwise.
    """
    def condition():
        try:
            click_button(template_path, threshold, duration_click, clicks)
            return True
        except ButtonNotFoundException:
            return False

    if not spin_until(condition, duration=duration, interval=interval):
        logging.error(f"Item not found for template at {template_path}")
        raise ButtonNotFoundException(template_path, 0, threshold)

    logging.info(f"Successfully clicked item at {template_path}")
    return True

def check_start_screen(threshold=0.8):
    """
    Check if the start screen is visible.
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :raises TemplateMatchException: If the start screen is not detected.
    :return: True if the start screen is detected, False otherwise.
    """
    logging.info("Checking for the start screen...")
    return screen_check_with_spin(START_SCREEN_TEMPLATE_PATH, threshold=threshold)

def check_daily_reward(duration=5, interval=0.1, threshold=0.8, duration_click=0.5):
    """
    Continuously check and collect rewards within a time limit.
    Ensures the game is on the START screen before attempting to collect rewards.

    :param duration: Total time to collect rewards (in seconds).
    :param interval: Time interval between checks (in seconds).
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :param duration_click: Time in seconds for the mouse to move to the click location (default: 0.5).
    :return: The number of rewards collected.
    """
    logging.info("Verifying game state before checking daily rewards...")

    # Ensure we are on the START screen
    current_state = check_current_screen(threshold=threshold)
    if current_state != GameState.START:
        logging.warning(f"Game is not on the START screen. Current state: {current_state.name}. Skipping rewards check.")
        return 0

    logging.info("Game is on the START screen. Proceeding to check daily rewards.")

    rewards_folder = "images/rewards"  # Path to the rewards folder
    reward_regex = re.compile(r"reward\d+\.png")  # Regular expression for reward images

    # Get a list of all reward images matching the pattern
    reward_templates = [
        os.path.join(rewards_folder, file)
        for file in os.listdir(rewards_folder)
        if reward_regex.match(file)
    ]

    collected_rewards = set()  # Track collected rewards
    start_time = time.time()
    rewards_collected_count = 0

    while time.time() - start_time < duration:
        frame = capture_screen()

        for template_path in reward_templates:
            if template_path in collected_rewards:
                continue  # Skip already collected rewards

            # Spin for up to 1 second to detect the chest
            if spin_until(lambda: screen_check_once(capture_screen(), template_path, threshold), duration=1, interval=0.1):
                logging.info(f"Reward detected using template: {template_path}")

                # Click the center of the screen
                screen_width, screen_height = pyautogui.size()
                pyautogui.moveTo(screen_width // 2, screen_height // 2, duration=duration_click)
                pyautogui.click()
                logging.info("Clicked the center of the screen to collect the reward.")

                collected_rewards.add(template_path)
                rewards_collected_count += 1

        # Check and close the reward collected screen
        close_daily_reward_screen(threshold=threshold, duration_click=duration_click)

        time.sleep(interval)

    # Log the result summary
    if rewards_collected_count > 0:
        logging.info(f"Daily rewards collection completed. Total rewards collected: {rewards_collected_count}.")
    else:
        logging.warning("No rewards detected during the collection period.")

    return rewards_collected_count


def collect_reward(duration=5, interval=0.1, threshold=0.8, click_duration=0.5):
    """
    Continuously check and collect rewards within a time limit.
    Ensures the game is on the START screen before proceeding.
    Handles daily rewards by matching screen contents with reward templates and clicking on matches.
    Closes the daily reward collected screen if detected.

    :param duration: Total time to collect rewards (in seconds).
    :param interval: Time interval between checks (in seconds).
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :param click_duration: Time in seconds for the mouse to move to the click location (default: 0.5).
    :return: The number of rewards collected.
    """
    logging.info("Verifying game state before starting reward collection...")

    # Ensure we are on the START screen
    current_state = check_current_screen(threshold=threshold)
    if current_state != GameState.START:
        logging.warning(f"Game is not on the START screen. Current state: {current_state.name}. Skipping reward collection.")
        return 0

    logging.info("Game is on the START screen. Proceeding with reward collection.")

    rewards_folder = "images/rewards"  # Path to the rewards folder
    reward_regex = re.compile(r"reward\d+\.png")  # Regular expression for reward images

    # Get a list of all reward images matching the pattern
    reward_templates = [
        os.path.join(rewards_folder, file)
        for file in os.listdir(rewards_folder)
        if reward_regex.match(file)
    ]

    collected_rewards = set()
    start_time = time.time()
    rewards_collected_count = 0

    while time.time() - start_time < duration:
        frame = capture_screen()

        for template_path in reward_templates:
            if template_path in collected_rewards:
                continue  # Skip already collected rewards

            try:
                if screen_check_once(frame, template_path, threshold):
                    logging.info(f"Reward detected using template: {template_path}")
                    pyautogui.moveTo(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2, duration=click_duration)
                    pyautogui.click()
                    logging.info("Clicked to collect the reward.")
                    collected_rewards.add(template_path)
                    rewards_collected_count += 1
            except TemplateMatchException as e:
                logging.debug(f"No match for template: {template_path}. Error: {e}")

        close_daily_reward_screen(threshold=threshold, duration_click=click_duration)
        time.sleep(interval)

    logging.info(f"Total rewards collected: {rewards_collected_count}.")
    return rewards_collected_count

def wait_for_loading_screen_to_finish(timeout=30, interval=0.5, threshold=0.8):
    """
    Wait for the loading screen to disappear after starting the game.

    :param timeout: Maximum time to wait for the loading screen to finish (in seconds).
    :param interval: Time interval between checks (in seconds).
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :raises GameLaunchTimeoutException: If the loading screen does not disappear within the timeout period.
    """
    logging.info("Waiting for the loading screen to finish...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            # Check if the loading screen is still present
            if screen_check_with_spin(LOADING_SCREEN_PATH, duration=interval, threshold=threshold):
                logging.info("Loading screen still active. Waiting...")
            else:
                logging.info("Loading screen finished. Proceeding...")
                return  # Exit when the loading screen disappears
        except TemplateMatchException:
            logging.info("Loading screen no longer detected. Proceeding...")
            return  # Exit if loading screen is not detected

    raise GameLaunchTimeoutException("Loading screen did not finish within the timeout period.")


def close_daily_reward_screen(threshold=0.8, duration_click=0.5):
    """
    Detect if the daily reward collected screen is visible and close it by clicking the "X" button.
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :param duration_click: Time in seconds for the mouse to move to the "X" button (default: 0.5).
    :return: True if the screen was closed, False otherwise.
    """
    logging.info("Checking if the daily reward collected screen is visible...")
    
    try:
        # Check for the collected reward screen
        if screen_check_with_spin(DAILY_REWARD_COLLECTED_TEMPLATE, duration=3, interval=0.1, threshold=threshold):
            logging.info("Daily reward collected screen detected.")
            
            # Click the "X" button
            click_item_with_spin(X_BUTTON_TEMPLATE_PATH, duration=3, interval=0.1, threshold=threshold, duration_click=duration_click)
            logging.info("Closed the daily reward collected screen.")
            return True
    except TemplateMatchException as e:
        logging.debug(f"Screen check for daily reward collected failed: {e}")
    except ButtonNotFoundException as e:
        logging.warning(f"'X' button not found: {e}")

    logging.info("Daily reward collected screen not detected.")
    return False
