import logging
import sys
import os
# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# Import modules after adjusting the path
from scripts.minnor.utils import *
from scripts.minnor.paths import *

logging.basicConfig(level=logging.INFO)


def click_btd6_icon():
  logging.info("Attempting to click BTD6 icon.")
  click_segment_if_screen(DESKTOP_DIR_BTD6_ICON,DESKTOP_DIR_DESKTOP, clicks=2)
  logging.info("Clicked BTD6 icon.")

def wait_for_start_screen():
  logging.info("Waiting for start screen.")
  wait_for_screen(SCREENS_DIR_STARTSCREEN, duration=60)
  logging.info("Found Start button.")


def click_start_button():
  wait_for_start_screen()
  logging.info("Attempting to click Start button.")
  click_if_segment(BUTTONS_DIR_BUTTONSTART)
  logging.info("Clicked Start button.")

def wait_for_main_menu():
  logging.info("Waiting for main menue screen.")
  wait_for_screen(SCREENS_DIR_MAINMENUSCREEN, duration=30)
  logging.info("Found main menue button.")


def claim_rewards(timeout=5, interval=0.5):
    """
    Click on rewards repeatedly until the collected screen is found.

    Args:
        timeout (int): Maximum time to spend checking (in seconds).
        interval (float): Time to wait between checks (in seconds).

    Returns:
        int: Total number of rewards collected.
    """
    templates = [
        REWARDS_DIR_REWARD1,
        REWARDS_DIR_REWARD2,
        REWARDS_DIR_REWARD3,
        REWARDS_DIR_REWARDINSTAMONKEY,
        REWARDS_DIR_REWARDMONEY,
    ]
    rewards_collected = 0
    start_time = time.time()

    logging.info("Starting reward collection process...")

    while time.time() - start_time < timeout:
        # Check for the collected screen to stop
        if check_segment(SCREENS_DIR_DAILYREWARDCOLLECTEDSCREEN, threshold=0.8, debug=True):
            logging.info("Daily reward collection screen found. Exiting reward collection.")
            return rewards_collected

        # Check and click on the X button if found
        if check_segment(BUTTONS_DIR_BUTTONX, threshold=0.8, debug=True):
            logging.info("Found close button (X). Clicking to close.")
            click(BUTTONS_DIR_BUTTONX)
            return rewards_collected

        # Iterate over reward templates and click on found rewards
        for template in templates:
            if check_segment(template, threshold=0.8, debug=True):
                logging.info(f"Found reward: {template}. Clicking to collect.")
                click(template)
                rewards_collected += 1
                time.sleep(interval)  # Avoid multiple clicks on the same reward

        # Add a small wait before re-checking
        time.sleep(interval)

    logging.warning("Reward collection timeout reached.")
    return rewards_collected


def collect_daily_reward_spin(timeout=5, interval=0.5):
    """
    Attempt to claim the daily reward by repeatedly checking for unopened or opened chests.
    
    Args:
        timeout (int): Maximum time to spend checking (in seconds).
        interval (float): Time to wait between checks (in seconds).
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        if check_segment(REWARDS_DIR_DAILYCHEST):
            logging.info("Found unopened chest. Proceeding to claim.")
            click_if_segment(REWARDS_DIR_DAILYCHEST)
            total_rewards = claim_rewards(timeout=5, interval=0.5)  # Collect rewards
            logging.info(f"Collected {total_rewards} rewards.")            
            return 
        elif check_segment(REWARDS_DIR_DAILYCHESTOPENED):
            logging.info("Found opened chest. Continuing...")
            return 
        else:
            logging.info("Chest not found. Retrying...")
        time.sleep(interval)  # Wait before retrying

    logging.warning("Failed to locate the daily reward within the timeout period.")


def collect_daily_reward():
  wait_for_main_menu()
  logging.info("Attemptig to claim text")
  collect_daily_reward_spin()
  logging.info("Done with daily reward...")

def btd6_start():
  """
  Full workflow to start BTD6, from desktop detection to game main menue.
  Will automatically use lattests save but this can be altered
  """
  logging.info("Starting BTD6...")
  try:
    click_btd6_icon()
    # wait_for_start_screen()
    click_start_button()
    # wait_for_main_menu()
    collect_daily_reward()
  except DesktopNotVisibleException as e:
    logging.error(f"Error: {e}")
    exit(1)
  except ClickException as e:
    logging.error(f"Error: {e}")
    exit(1)
  except TimeoutException as e:
    logging.error(f"Error: {e}")
    exit(1)
  except Exception as e:
    logging.error(f"Unexpected error: {e}")
    exit(1)

if __name__ == "__main__":
  btd6_start()
