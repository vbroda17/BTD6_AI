# New version of utils
import pyautogui
import cv2
import numpy as np
import logging
import time
import os
from scripts.minor.exceptions import *

def capture_screen(debug=False):
  """Capture the current screen and return it as a NumPy array."""
  if debug:
      logging.info("Captureing the screen")
  screenshot = pyautogui.screenshot()
  if debug:
    screenshot.save("debug_screenshot.png")
  return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)


def validate_template_path(template_path, debug=False):
  """
  Validate and load a template image from a given path.

  Args:
      template_path (str): Path to the template image.
      debug (bool): If True, log debug information.

  Returns:
      template (np.array): Loaded grayscale template image.

  Raises:
      FileNotFoundError: If the file does not exist.
      ValueError: If the template image cannot be loaded.
  """
  if debug:
    logging.debug(f"Validating template path: {template_path}")

  if not os.path.isfile(template_path):
    logging.error(f"Template image not found at: {template_path}")
    raise FileNotFoundError(f"Template image not found at: {template_path}")

  template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
  if template is None:
    logging.error(f"Failed to load template image at: {template_path}")
    raise ValueError(f"Failed to load template image at: {template_path}")

  if debug:
    logging.debug(f"Template image loaded successfully: {template_path}")
    logging.debug(f"Template shape: {template.shape}, dtype: {template.dtype}")

  return template



def click(image_path, threshold=0.8, duration=0.5, clicks=1, debug=False):
  """Locate an image on the screen and click it."""
  try:
    template = validate_template_path(image_path)
    screen = capture_screen()
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if debug:
        logging.info(f"Clicking {image_path}. Min: {min_val:.2f}, Max: {max_val:.2f}, Threshold: {threshold:.2f}")
    if max_val < threshold:
        raise ClickException(image_path, max_val, threshold)

    pyautogui.moveTo(max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2, duration=duration)
    pyautogui.click(clicks=clicks)
    
  except Exception as e:
    logging.error(f"Error during click for {image_path}: {e}")
    raise



def identify_screen(threshold=0.8):
  pass


def check_screen(image_path, threshold=0.8, debug=False):
  """Check if the given screen is visible."""
  try:
    template = validate_template_path(image_path)
    screen = capture_screen(debug=debug)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    if debug:
        logging.info(f"Checking for {image_path}. Found match value: {max_val:.2f}, Threshold: {threshold:.2f}")

    return max_val >= threshold
  except Exception as e:
    logging.error(f"Error during screen check for {image_path}: {e}")
    raise


def check_segment(segment_path, threshold=0.8, debug=False):
  """Check if a specific segment is visible on the screen."""
  try:
    template = validate_template_path(segment_path)
    screen = capture_screen(debug=debug)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    if debug:
      logging.info(f"Checking for segment: {segment_path}. Match value: {max_val}, Threshold: {threshold}")

    # Return whether the segment is visible
    return max_val >= threshold
  except Exception as e:
    logging.error(f"Error during check_segment for {segment_path}: {e}")
    raise


def wait_for_screen(image_path, threshold=0.8, duration=5):
  """Wait for a specific screen to appear within a timeout period."""
  start_time = time.time()
  while time.time() - start_time < duration:
      if check_screen(image_path, threshold):
          return True
      time.sleep(0.5)
  raise TimeoutException(time.time() - start_time, f"Screen not found: {image_path}")


def click_segment_if_screen(segment_path, screen_path, threshold=0.8, duration=0.5, clicks=1, debug=False):
  """"Will click a specified segment if on a specific screen"""
  if check_screen(screen_path, threshold=threshold, debug=debug):
    click(segment_path, threshold=threshold, duration=duration, clicks=clicks, debug=debug)

def click_if_segment(segment_path, threshold=0.8, duration=0.5, clicks=1, debug=False):
  if check_screen(segment_path, threshold=threshold, debug=debug):
    click(segment_path, threshold=threshold, duration=duration, clicks=clicks, debug=debug)

def match_template_location(screen, template, threshold=0.8):
    """
    Find the location of a template on the screen.

    Args:
        screen (np.array): Captured screen as a NumPy array.
        template (np.array): Template image to match.
        threshold (float): Minimum match confidence.

    Returns:
        tuple: (x, y) coordinates of the top-left corner of the best match, or None if not found.
    """
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return max_loc
    return None
