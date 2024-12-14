import pyautogui
import cv2
import numpy as np
import time

def is_desktop_visible(screenshot, template_path):
    """
    Check if the desktop is visible by finding a specific desktop feature.
    """
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"Template image not found at {template_path}")

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8
    return max_val >= threshold

def click_btd6_icon(screenshot, btd6_icon_path):
    """
    Find and double-click the BTD6 desktop icon.
    """
    template = cv2.imread(btd6_icon_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"BTD6 icon template image not found at {btd6_icon_path}")

    screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    threshold = 0.8
    if max_val >= threshold:
        icon_center = (max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2)
        pyautogui.moveTo(icon_center[0], icon_center[1], duration=0.5)
        pyautogui.doubleClick()
        return True
    return False

def wait_for_game_launch(starting_game_path):
    """
    Wait until the game shows the "Starting game" screen.
    """
    print("Waiting for the game to launch...")
    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Load the template for the "Starting game" screen
        template = cv2.imread(starting_game_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            raise ValueError(f"Starting game template image not found at {starting_game_path}")

        screenshot_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)

        # Check if the "Starting game" screen is visible
        threshold = 0.8
        if max_val >= threshold:
            print("Game is launching!")
            break

        time.sleep(1)  # Wait 1 second before checking again

def main(desktop_template_path, btd6_icon_path, starting_game_path):
    """
    Main function to check if on desktop, launch BTD6, and wait for game launch.
    """
    print("Press 'q' to quit.")
    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Check if the desktop is visible
        if is_desktop_visible(frame, desktop_template_path):
            print("Desktop detected! Looking for BTD6 icon.")
            if click_btd6_icon(frame, btd6_icon_path):
                print("BTD6 icon clicked. Waiting for the game to launch.")
                wait_for_game_launch(starting_game_path)
                break

        # Quit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Provide the paths to the template images
    desktop_template_path = "images/desktop/desktop.png"  # Replace with the desktop feature template path
    btd6_icon_path = "images/desktop/btd6_icon.png"       # Replace with the BTD6 icon template path
    starting_game_path = "images/desktop/btd6_start.png"  # Replace with the "Starting game" screen template path

    main(desktop_template_path, btd6_icon_path, starting_game_path)
