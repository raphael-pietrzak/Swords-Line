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

class ServerConfig:
    HOST = ''  # Vide pour accepter les connexions de toutes les interfaces
    PORT = 5555
    MAX_CONNECTIONS = 10
    BUFFER_SIZE = 4096
    ROOM_CLEANUP_DELAY = 300  # 5 minutes
    UPDATE_INTERVAL = 0.1

# Énumération des états de jeu
class GameState(Enum):
    WAITING = 0
    STARTING = 1
    PLAYING = 2
    FINISHED = 3