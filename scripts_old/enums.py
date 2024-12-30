from enum import Enum, auto

class GameState(Enum):
    DESKTOP = auto()
    LAUNCHING = auto()
    START = auto()
    MAIN_MENU = auto()

# You can add more enums here if needed, such as for tower types or game modes.
