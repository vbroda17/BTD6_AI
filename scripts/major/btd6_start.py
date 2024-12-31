import logging
import sys
import os
# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# Import modules after adjusting the path
from scripts.minnor.utils import *
from scripts.minnor.exceptions import *



def click_btd6_icon():
  logging.info("Attempting to click BTD6 icon.")
  click()

def wait_for_start_screen():
  pass

def click_start_button():
  wait_for_start_screen()

def wait_for_main_menu():
  pass


def btd6_start():
  """
  Full workflow to start BTD6, from desktop detection to game main menue.
  Will automatically use lattests save but this can be altered
  """
  logging.info("Starting BTD6...")
  try:
    click_btd6_icon()
    wait_for_start_screen()
    click_start_button()
    wait_for_main_menu()
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
