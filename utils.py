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
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def spin_until(condition_func, duration=5, interval=0.1, *args, **kwargs):
    """
    Generic spin function to repeatedly check a condition within a time limit.
    """
    start_time = time.time()
    while time.time() - start_time < duration:
        if condition_func(*args, **kwargs):
            return True
        time.sleep(interval)
    return False


def capture_screen():
    """Capture the current screen and return it as a NumPy array."""
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def validate_template_path(template_path):
    """
    Validate and load a template image from a given path.
    """
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"Template image not found at {template_path}")
    return template


def screen_check_once(screenshot, template_path, threshold=0.8):
    """
    Check if a screen matches a given template.
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
    """
    logging.info(f"Checking screen for template: {template_path}")
    return spin_until(
        lambda: screen_check_once(capture_screen(), template_path, threshold),
        duration=duration,
        interval=interval
    )


def wait_for_screen(template_path, timeout=60, interval=0.5, threshold=0.8):
    """
    Generic function to wait for a specific screen to appear.
    """
    logging.info(f"Waiting for the screen: {template_path}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if screen_check_once(capture_screen(), template_path, threshold):
                logging.info(f"Screen detected: {template_path}")
                return True
        except TemplateMatchException:
            pass  # Continue checking
        time.sleep(interval)
    raise GameLaunchTimeoutException(f"Screen '{template_path}' did not appear within {timeout} seconds.")


def click_button(template_path, threshold=0.8, duration=0.5, clicks=1):
    """
    Find and click a button on the screen.
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
        logging.info(f"Clicked button at {template_path}")
    else:
        raise ButtonNotFoundException(template_path, max_val)


def click_item_with_spin(template_path, duration=5, interval=0.1, threshold=0.8, duration_click=0.5, clicks=1):
    """
    Repeatedly check and click an item (e.g., button, chest) on the screen within a time limit.
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


def check_current_screen(threshold=0.8):
    """
    Check the current game screen and return the corresponding GameState.
    """
    logging.info("Checking the current game screen...")
    frame = capture_screen()
    screen_checks = [
        (GameState.DESKTOP, DESKTOP_TEMPLATE_PATH),
        (GameState.START, START_SCREEN_TEMPLATE_PATH),
        (GameState.MAIN_MENU, MAIN_MENU_TEMPLATE_PATH),
    ]
    for state, template_path in screen_checks:
        try:
            if screen_check_once(frame, template_path, threshold):
                logging.info(f"Screen detected: {state.name}")
                return state
        except TemplateMatchException:
            pass
    logging.warning("No matching screen detected. Returning UNKNOWN state.")
    return GameState.UNKNOWN

def check_daily_reward(duration=5, interval=0.1, threshold=0.8, click_duration=0.5):
    """
    Continuously check and collect rewards within a time limit.
    Starts by clicking on the reward chest box if detected.
    If the chest has already been collected, it checks for the 'chest opened' template and moves on.
    """
    logging.info("Starting daily reward collection...")

    # Step 1: Attempt to find and click the daily reward chest
    try:
        logging.info("Looking for the daily reward chest...")
        spin_until(
            lambda: click_button(DAILY_REWARD_CHEST_PATH, threshold=threshold, duration=click_duration, clicks=1),
            duration=2,
            interval=0.1
        )
        logging.info("Daily reward chest clicked. Proceeding to collect rewards.")
    except ButtonNotFoundException:
        # Step 2: If chest not found, check if it's already opened
        logging.info("Daily reward chest not found. Checking if the chest was already opened...")
        try:
            if screen_check_with_spin(DAILY_REWARD_OPENED_TEMPLATE, duration=2, interval=0.1, threshold=threshold):
                logging.info("Daily reward chest has already been collected. Moving on.")
                return 0
        except TemplateMatchException:
            logging.warning("Daily reward chest and opened chest template not detected. No rewards to collect.")
            return 0

    # Step 3: Proceed to collect rewards if the chest was clicked
    rewards_folder = "images/rewards"
    reward_regex = re.compile(r"reward\d+\.png")
    reward_templates = [os.path.join(rewards_folder, file) for file in os.listdir(rewards_folder) if reward_regex.match(file)]
    collected_rewards = set()
    start_time = time.time()
    rewards_collected_count = 0

    while time.time() - start_time < duration:
        frame = capture_screen()

        for template_path in reward_templates:
            if template_path in collected_rewards:
                continue  # Skip already collected rewards

            try:
                # Check for rewards and click the center of the screen
                if screen_check_once(frame, template_path, threshold):
                    logging.info(f"Reward detected using template: {template_path}")
                    pyautogui.moveTo(pyautogui.size()[0] // 2, pyautogui.size()[1] // 2, duration=click_duration)
                    pyautogui.click()
                    logging.info("Clicked to collect the reward.")
                    collected_rewards.add(template_path)
                    rewards_collected_count += 1
            except TemplateMatchException:
                logging.debug(f"No match for template: {template_path}")

        # Step 4: Check and close the daily reward collected screen
        close_daily_reward_screen(threshold=threshold, duration_click=click_duration)
        time.sleep(interval)

    # Final logging
    if rewards_collected_count > 0:
        logging.info(f"Daily rewards collection completed. Total rewards collected: {rewards_collected_count}.")
    else:
        logging.info("No additional rewards detected during the collection period.")

    return rewards_collected_count




def close_daily_reward_screen(threshold=0.8, duration_click=0.5):
    """
    Detect and close the daily reward collected screen.
    """
    try:
        if screen_check_with_spin(DAILY_REWARD_COLLECTED_TEMPLATE, duration=3, threshold=threshold):
            logging.info("Daily reward collected screen detected.")
            click_button(X_BUTTON_TEMPLATE_PATH, threshold=threshold, duration=duration_click)
            logging.info("Closed the daily reward collected screen.")
            return True
    except (TemplateMatchException, ButtonNotFoundException):
        pass
    return False
