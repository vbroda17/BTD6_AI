from enum import Enum

class UserInputMode(Enum):
    DEFAULT = "default"
    GUIDED = "guided"
    FREE = "free"
    DEBUG = "debug"

class HeroStatus(Enum):
    SELECTABLE = "selectable"
    SELECTED = "selected"
    LOCKED = "locked"