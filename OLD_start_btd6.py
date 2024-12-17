import pyautogui
import cv2
import numpy as np
import time

# Global template paths
desktop_template_path = "images/desktop/desktop.png"
btd6_icon_path = "images/desktop/btd6_icon.png"
loading_game_template_path = "images/desktop/btd6_launch.png"
start_screen_template_path = "images/screens/startScreen.png"
start_button_template_path = "images/buttons/buttonStart.png"

def capture_screen():
    """
    Capture the screen and return it as a NumPy array.
    """
    screenshot = pyautogui.screenshot()
    frame = np.array(screenshot)
    return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

def screen_check(screenshot, template_path, threshold=0.8):
    """
    Generalized function to check if a screen matches a given template.
    """
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"Template image not found at {template_path}")

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    if max_val < threshold:
        print(f"Template not matched. Confidence: {max_val:.2f}")
    return max_val >= threshold

def is_desktop_visible():
    """
    Check if the desktop is visible.
    """
    frame = capture_screen()
    return screen_check(frame, desktop_template_path)

def loading_game_check():
    """
    Check if the game is in the 'Starting game' phase.
    """
    frame = capture_screen()
    return screen_check(frame, loading_game_template_path)

def is_start_screen_visible():
    """
    Check if the game is on the start screen.
    """
    frame = capture_screen()
    return screen_check(frame, start_screen_template_path)

def click_button(template_path, threshold=0.8, duration=0.5):
    """
    Generalized function to find and click a button on the screen.
    :param template_path: Path to the button image template.
    :param threshold: Confidence threshold for template matching (default: 0.8).
    :param duration: Time in seconds for the mouse to move to the button (default: 0.5).
    :return: True if the button is clicked, False otherwise.
    """
    frame = capture_screen()
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"Button template image not found at {template_path}")

    screenshot_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        button_center = (max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2)
        pyautogui.moveTo(button_center[0], button_center[1], duration=duration)
        pyautogui.click()
        print(f"Clicked the button at {template_path}.")
        return True

    print(f"Button not found for template: {template_path}. Confidence: {max_val:.2f}")
    return False

def click_btd6_icon():
    """
    Find and double-click the BTD6 desktop icon.
    """
    return click_button(btd6_icon_path, duration=0.5)

def click_start_button():
    """
    Detect and click the 'Start' button on the start screen.
    """
    return click_button(start_button_template_path)

def start_btd6():
    """
    Main function to detect desktop, launch BTD6, and check for loading game and start screen.
    """
    print("Press 'q' to quit.")
    while True:
        try:
            # Check if the desktop is visible
            if is_desktop_visible():
                print("Desktop detected! Looking for BTD6 icon.")
                if click_btd6_icon():
                    print("Waiting for the game to launch.")

                    # Wait for loading screen
                    while not loading_game_check():
                        print("Waiting for 'Starting game' phase...")
                        time.sleep(1)

                    print("Game is in the 'Starting game' phase!")

                    # Wait for start screen
                    print("Waiting for the start screen...")
                    while not is_start_screen_visible():
                        print("Waiting for the start screen...")
                        time.sleep(1)

                    print("Game is on the start screen!")

                    # Click the 'Start' button
                    print("Looking for the 'Start' button...")
                    while not click_start_button():
                        print("Waiting for the 'Start' button to appear...")
                        time.sleep(1)

                    break

            time.sleep(1)  # Avoid unnecessary CPU usage
        except KeyboardInterrupt:
            print("\nQuitting...")
            break

if __name__ == "__main__":
    start_btd6()
    game_parameters = select_game()
    train_model = train
