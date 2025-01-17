import logging
from scripts.minor.utils import *
from scripts.minor.paths import *

logging.basicConfig(level=logging.INFO)

# Hero options as constants
HEROES = {
    "Quincy": HEROES_QUINCY,
    "Gwendolin": HEROES_GWENDOLIN,
    "Striker Jones": HEROES_STRIKER_JONES,
    "Obyn Greenfoot": HEROES_OBYN_GREENFOOT,
    "Benjamin": HEROES_BENJAMIN,
}

def display_heroes():
    """
    Display the list of available heroes.
    """
    print("\n=== Available Heroes ===")
    for i, hero in enumerate(HEROES.keys(), start=1):
        print(f"{i}. {hero}")

def select_hero(hero_name=None):
    """
    Select a hero interactively or programmatically.
    
    Args:
        hero_name (str): Name of the hero to select. If None, prompt the user.
    """
    if hero_name is None:
        display_heroes()
        choice = input("Enter the number of the hero you want to select: ")
        try:
            hero_name = list(HEROES.keys())[int(choice) - 1]
        except (ValueError, IndexError):
            logging.error("Invalid choice. Please try again.")
            return select_hero()

    logging.info(f"Attempting to select hero: {hero_name}")
    hero_path = HEROES.get(hero_name)
    if not hero_path:
        logging.error(f"Hero '{hero_name}' not found.")
        return

    # Simulate hero selection on the screen
    if check_segment(hero_path, threshold=0.8):
        click(hero_path)
        logging.info(f"Selected hero: {hero_name}")
    else:
        logging.error(f"Unable to locate hero '{hero_name}' on the screen.")

def confirm_hero_selection():
    """
    Confirm the currently selected hero by checking the screen.
    """
    for hero_name, hero_path in HEROES.items():
        if check_segment(hero_path, threshold=0.8):
            logging.info(f"Currently selected hero: {hero_name}")
            return hero_name
    logging.warning("No hero is currently selected.")
    return None

def hero_selection_menu():
    """
    Menu for hero selection.
    """
    while True:
        print("\n=== Hero Selection Menu ===")
        print("1. Display Heroes")
        print("2. Select Hero")
        print("3. Confirm Selected Hero")
        print("4. Return to Main Menu")
        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            display_heroes()
        elif choice == "2":
            select_hero()
        elif choice == "3":
            confirm_hero_selection()
        elif choice == "4":
            logging.info("Returning to main menu.")
            break
        else:
            logging.warning("Invalid choice. Please enter a valid option.")
