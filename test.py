import pyautogui
import cv2
import numpy as np
import time
import pytesseract  # For OCR, optional for advanced detection

# Tesseract configuration
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Paths for templates
TEMPLATES = {
    "desktop": "images/desktop/desktop.png",
    "btd6_icon": "images/desktop/btd6_icon.png",
    "loading_game": "images/desktop/btd6_launch.png",
    "start_screen": "images/screens/startScreen.png",
    "start_button": "images/buttons/buttonStart.png",
}

def capture_screen():
    """
    Capture the current screen as a NumPy array.
    """
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def match_template(frame, template_path, threshold=0.8):
    """
    Match a template on the screen and return the confidence and location.
    """
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    if template is None:
        raise ValueError(f"Template image not found at {template_path}")

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    return max_val, max_loc

def click_at(location, duration=0.5):
    """
    Click at a specific screen location.
    """
    pyautogui.moveTo(location[0], location[1], duration=duration)
    pyautogui.click()

def detect_and_click(template_path, threshold=0.8):
    """
    Detect a button using template matching and click it.
    """
    frame = capture_screen()
    confidence, location = match_template(frame, template_path, threshold)
    if confidence >= threshold:
        button_center = (location[0] + templ                ate.shape[1] // 2, location[1] + template.shape[0] // 2)
        click_at(button_center)
        print(f"Clicked button: {template_path}")
        return True
    print(f"Button not found: {template_path} (Confidence: {confidence:.2f})")
    return False

def detect_text(frame, region=None):
    """
    Detect text in a specified region of the screen using OCR.
    """
    if region:
        frame = frame[region[1]:region[3], region[0]:region[2]]
    return pytesseract.image_to_string(frame)

# Game state functions
def is_desktop_visible():
    """
    Check if the desktop is visible.
    """
    frame = capture_screen()
    return match_template(frame, TEMPLATES["desktop"])[0] >= 0.8

def click_btd6_icon():
    """
    Click the BTD6 desktop icon.
    """
    return detect_and_click(TEMPLATES["btd6_icon"])

def is_start_screen_visible():
    """
    Check if the game's start screen is visible.
    """
    frame = capture_screen()
    return match_template(frame, TEMPLATES["start_screen"])[0] >= 0.8

def game_loop():
    """
    Main game loop to control BTD6.
    """
    print("Starting BTD6...")
    if is_desktop_visible():
        if click_btd6_icon():
            print("Game launched, waiting for the start screen...")
            time.sleep(10)  # Wait for the game to load
            while not is_start_screen_visible():
                print("Waiting for the start screen...")
                time.sleep(1)
            print("Start screen detected. Ready to begin.")
            detect_and_click(TEMPLATES["start_button"])

# Placeholder for RL training and strategy
def analyze_game_state():
    """
    Analyze the game state and return relevant metrics.
    """
    frame = capture_screen()
    # Example: Extract round number, money, lives using OCR or visual markers
    money = detect_text(frame, region=(100, 100, 200, 150))
    round_number = detect_text(frame, region=(300, 300, 400, 350))
    return {"money": money, "round": round_number}

def place_tower(location, tower_type):
    """
    Place a tower at the specified location.
    """
    print(f"Placing {tower_type} at {location}")
    pyautogui.moveTo(location[0], location[1], duration=0.5)
    pyautogui.click()

if __name__ == "__main__":
    game_loop()
