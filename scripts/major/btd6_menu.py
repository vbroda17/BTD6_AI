import logging
import sys
import os

# Add the project root to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# Import modules after adjusting the path
from scripts.minor.utils import *
from scripts.minor.paths import *
from scripts.major.btd6_heroes import *
from scripts.major.btd6_play import *

logging.basicConfig(level=logging.INFO)

def display_menu():
    """
    Display the main menu options for navigation.
    """
    print("\n=== BTD6 Menu ===")
    print("1. Hero Selection")
    print("2. Play Game")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")
    return choice

def navigate_menu(mode="default"):
    """
    Navigate between different game sections based on user input.
    """
    
    while True:
        choice = display_menu()

        if choice == "1":
            logging.info("Navigating to Hero Selection.")
            hero_selection_menu()
        elif choice == "2":
            logging.info("Navigating to Play Game.")
            play_game_menu()
        elif choice == "3":
            logging.info("Exiting BTD6 Menu.")
            break
        else:
            logging.warning("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
  navigate_menu()

