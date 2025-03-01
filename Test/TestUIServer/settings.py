import pygame
from enum import Enum

# Configuration de base
WIDTH, HEIGHT = 1024, 768
FPS = 60

# Couleurs
BACKGROUND_COLOR = (30, 30, 40)
TEXT_COLOR = (220, 220, 220)
BUTTON_COLOR = (70, 70, 100)
BUTTON_HOVER_COLOR = (90, 90, 120)
BUTTON_TEXT_COLOR = (240, 240, 240)
TAB_INACTIVE_COLOR = (50, 50, 70)
TAB_ACTIVE_COLOR = (70, 70, 100)
SUCCESS_COLOR = (0, 200, 0)
WARNING_COLOR = (200, 200, 0)
ERROR_COLOR = (200, 0, 0)

# Énumération des onglets
class Tab(Enum):
    DASHBOARD = 0
    ROOMS = 1
    LOGS = 2
    CONFIG = 3
