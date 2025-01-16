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
  click_segment_if_screen(START_BTD6_DESKTOP_BTD6_ICON,START_BTD6_DESKTOP_DESKTOP, clicks=2)
  logging.info("Clicked BTD6 icon.")

def wait_for_start_screen():
  logging.info("Waiting for start screen.")
  wait_for_screen(START_BTD6_LOADING_STARTSCREEN, duration=60)
  logging.info("Found Start button.")
  time.sleep(0.5)

def click_start_button():
  wait_for_start_screen()
  logging.info("Attempting to click Start button.")
  click_if_segment(BUTTONS_BUTTONSTART)
  logging.info("Clicked Start button.")

def handle_start_saved_game_screen(option="on_the_cloud"):
  """
  Handle the 'Choose Saved Game' screen by selecting the specified save option.

  Args:
      option (str): The save option to select. Possible values:
                    - "latest_save"
                    - "oldest_save"
                    - "this_device"
                    - "on_the_cloud"
  """
  logging.info("Checking for 'Choose Saved Game' screen.")
  
  # Paths for saved game options
  options_map = {
    "latest_save": START_BTD6_CHOOSE_SAVED_GAME_LATESTSAVE,
    "oldest_save": START_BTD6_CHOOSE_SAVED_GAME_OLDERSAVE,
    "this_device": START_BTD6_CHOOSE_SAVED_GAME_THISDEVICE,
    "on_the_cloud": START_BTD6_CHOOSE_SAVED_GAME_ONTHECLOUD,
  }
  
  # Validate the provided option
  if option not in options_map:
    logging.error(f"Invalid option '{option}' provided. Defaulting to 'oldest_save'.")
    option = "oldest_save"

  # Template for the selected option
  selected_template = options_map[option]

  # Check for the saved game screen
  if check_segment(START_BTD6_CHOOSE_SAVED_GAME_CHOOSESAVEDGAME, threshold=0.8):
    logging.info("Detected 'Choose Saved Game' screen. Proceeding to select save option.")
    
    # Click the specified save option
    click(selected_template)
    logging.info(f"Clicked on save option: {option.replace('_', ' ').title()}.")

    # # Find and click the nearest 'Use' button
    # screen = capture_screen(debug=True)
    # use_button_template = validate_template_path(START_BTD6_CHOOSE_SAVED_GAME_USE, debug=True)

    # # Locate the save option and use button on the screen
    # save_location = match_template_location(screen, validate_template_path(selected_template))
    # use_location = match_template_location(screen, use_button_template)

    # # Ensure a valid match
    # if save_location and use_location:
    #     logging.info(f"Found 'Use' button near selected save option. Clicking.")
    #     pyautogui.moveTo(use_location[0], use_location[1], duration=0.5)
    #     pyautogui.click()
    # else:
    #     logging.error("Unable to locate 'Use' button for the selected save option.")
  else:
    logging.info("'Choose Saved Game' screen not detected. Proceeding as normal.")

def wait_for_main_menu():
  logging.info("Waiting for main menue screen.")
  wait_for_screen(SCREENS_MAINMENUSCREEN, duration=30)
  logging.info("Found main menue button.")

def wait_for_choose_game_or_main_menu(timeout=60, interval=1, save_option="oldest_save"):
  """
  Wait for either the 'Choose Saved Game' screen or the main menu screen.
  Handles actions based on which screen appears.

  Args:
      timeout (int): Maximum time to wait for a screen to appear (in seconds).
      interval (float): Time to wait between screen checks (in seconds).
      save_option (str): Save option to select if the 'Choose Saved Game' screen is detected.
                          Options: 'latest_save', 'oldest_save', 'this_device', 'on_the_cloud'.

  Returns:
      None
  """
  logging.info("Waiting for either the 'Choose Saved Game' screen or the main menu screen...")
  start_time = time.time()

  while time.time() - start_time < timeout:
    # Check for the 'Choose Saved Game' screen
    if check_segment(START_BTD6_CHOOSE_SAVED_GAME_CHOOSESAVEDGAME, threshold=0.8):
      logging.info("Detected 'Choose Saved Game' screen.")
      handle_start_saved_game_screen(option=save_option)
      wait_for_main_menu()
      if check_segment(SCREENS_MAINMENUSCREEN, threshold=0.8):
        logging.info("Detected main menu screen. Proceeding to collect daily rewards.")
        collect_daily_reward()
      return

    # Check for the main menu screen
    if check_segment(SCREENS_MAINMENUSCREEN, threshold=0.8):
      logging.info("Detected main menu screen. Proceeding to collect daily rewards.")
      collect_daily_reward()
      return

    logging.info("No relevant screen detected. Retrying...")
    time.sleep(interval)

  logging.warning("Timeout reached without detecting any relevant screen.")

def claim_rewards(timeout=30, interval=1):
  """
  Attempt to claim rewards by clicking and checking the screen at regular intervals.
  
  Args:
      timeout (int): Maximum time to attempt clicking and checking (in seconds).
      interval (float): Time to wait between clicks (in seconds).
  
  Returns:
      int: Total number of rewards collected.
  """
  rewards_collected = 0
  start_time = time.time()

  logging.info("Starting reward collection process...")

  while time.time() - start_time < timeout:
    # Perform a click at the center of the screen
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(x=screen_width // 2, y=screen_height // 2)
    logging.info("Clicked on the screen.")

    # Wait for the specified interval
    time.sleep(interval)

    # Check if the collected screen is visible
    if check_segment(START_BTD6_CHEST_DAILYREWARDCOLLECTEDSCREEN, threshold=0.8, debug=True):
        logging.info("Daily reward collected screen detected. Ending reward collection.")
        break

    # Increment the rewards counter for each click
    rewards_collected += 1

  logging.info(f"Reward collection completed. Total rewards collected: {rewards_collected}")
  return rewards_collected

def collect_daily_reward_spin(timeout=5, interval=1.5):
  """
  Attempt to claim the daily reward by repeatedly checking for unopened or opened chests.
  
  Args:
      timeout (int): Maximum time to spend checking (in seconds).
      interval (float): Time to wait between checks (in seconds).
  """
  start_time = time.time()
  while time.time() - start_time < timeout:
    if check_segment(START_BTD6_CHEST_DAILYCHEST):
      logging.info("Found unopened chest. Proceeding to claim.")
      click_if_segment(START_BTD6_CHEST_DAILYCHEST)
      total_rewards = claim_rewards(timeout=5, interval=interval)  # Collect rewards
      logging.info(f"Collected {total_rewards} rewards.")
      click_if_segment(BUTTONS_BUTTONX)            
      return 
    elif check_segment(START_BTD6_CHEST_DAILYCHESTOPENED):
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
    wait_for_choose_game_or_main_menu()
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
