# New version of utils
import pyautogui
import cv2
import numpy as np
import logging
import time
from exceptions import *


def capture_screen(debug=False):
  """Capture the current screen and return it as a NumPy array."""
  if debug:
      logging.log("Captureing the screen")
  screenshot = pyautogui.screenshot()
  if debug:
    screenshot.save("debug_screenshot.png")
  return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def click(image_path, threshold=0.8, duration=0.5, clicks=1):
  """
  Locate an image on the screen and click it.
  """
  screen = capture_screen()
  template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
  result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
  if max_val < threshold:
      raise ClickException(image_path, max_val, threshold)
  pyautogui.click(x=max_loc[0], y=max_loc[1], clicks=clicks, duration=duration)


def identify_screen(threshold=0.8):
  pass

def check_for_screen(image_path, threshold=0.8, debug=False):
  """Check if the given screen is visible."""
  screen = capture_screen()
  template = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
  result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
  _, max_val, _, _ = cv2.minMaxLoc(result)
  if debug:
     logging.log('Checking for {image_path}. found {max_val} and threshold {threshold}')
  return max_val >= threshold


def wait_for_screen(image_path, threshold=0.8, duration=5):
  """Wait for a specific screen to appear within a timeout period."""
  start_time = time.time()
  while time.time() - start_time < duration:
      if check_for_screen(image_path, threshold):
          return True
      time.sleep(0.5)
  raise TimeoutException(time.time() - start_time, f"Screen not found: {image_path}")


def click_segment_if_screen(segment_path, screen_path, threshold=0.8, duration=0.5, clicks=1):
   pass

def click_if_segment(segment_path, threshold=0.8, duration=0.5, clicks=1):
   pass