import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from scripts.minor.exceptions import *
from scripts.minor.enums import *
from scripts.minor.utils import *
from scripts.minor.paths import *

import json
import logging

class HeroInformation:
    def __init__(self, name, status=HeroStatus.LOCKED):
        """
        Initialize the HeroInformation object.

        Args:
            name (str): The hero's name.
            status (HeroStatus): The hero's current status.
        """
        self.name = name
        self.status = status

    def to_dict(self):
        """Convert the hero's information to a dictionary."""
        return {
            "name": self.name,
            "status": self.status.value,
        }

    @staticmethod
    def from_dict(data):
        """Create a HeroInformation object from a dictionary."""
        return HeroInformation(
            name=data["name"],
            status=HeroStatus(data["status"])
        )

    def __repr__(self):
        return f"HeroInformation(name='{self.name}', status={self.status})"


class HeroManager:
    def __init__(self):
        """
        Initialize the HeroManager object.
        """
        self.heroes = []  # List of HeroInformation objects
        self.selected_hero = None  # Currently selected hero

    def add_hero(self, hero):
        """
        Add a hero to the manager.

        Args:
            hero (HeroInformation): The hero to add.
        """
        self.heroes.append(hero)

    def get_playable_heroes(self):
        """
        Get a list of all playable (selectable) heroes.

        Returns:
            list[HeroInformation]: List of selectable heroes.
        """
        return [hero for hero in self.heroes if hero.status != HeroStatus.LOCKED]

    def get_hero_by_name(self, name):
        """
        Get a hero by their name.

        Args:
            name (str): The name of the hero.

        Returns:
            HeroInformation or None: The hero object, or None if not found.
        """
        for hero in self.heroes:
            if hero.name == name:
                return hero
        return None

    def set_selected_hero(self, name):
        """
        Set the currently selected hero.

        Args:
            name (str): The name of the hero to select.
        """
        hero = self.get_hero_by_name(name)
        if hero and hero.status != HeroStatus.LOCKED:
            self.selected_hero = hero
            hero.status = HeroStatus.SELECTED
            logging.info(f"Selected hero: {name}")
        else:
            logging.warning(f"Cannot select hero: {name}. Either locked or not found.")

    def save_to_file(self, file_path):
        """
        Save hero information to a JSON file.

        Args:
            file_path (str): Path to the file.
        """
        data = {
            "heroes": [hero.to_dict() for hero in self.heroes],
        }
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        logging.info(f"Saved hero information to {file_path}.")

    def load_from_file(self, file_path):
        """
        Load hero information from a JSON file.

        Args:
            file_path (str): Path to the file.
        """
        if not os.path.exists(file_path):
            logging.warning(f"File {file_path} does not exist. No data loaded.")
            return

        with open(file_path, "r") as f:
            data = json.load(f)
        self.heroes = [HeroInformation.from_dict(hero) for hero in data["heroes"]]
        logging.info(f"Loaded hero information from {file_path}.")

    def __repr__(self):
        return f"HeroManager(heroes={self.heroes}, selected_hero={self.selected_hero})"
