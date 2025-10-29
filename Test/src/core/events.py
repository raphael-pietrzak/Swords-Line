from enum import Enum, auto
from typing import Dict, List
from dataclasses import dataclass

class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    SETTINGS = auto()

class EventType(Enum):
    QUIT = auto()
    STATE_CHANGE = auto()
    MENU_BUTTON_CLICK = auto()
    MENU_SELECTION = auto()
    PLAYER_MOVE = auto()
    PLAYER_ATTACK = auto()
    COLLISION = auto()

@dataclass
class Event:
    type: EventType
    data: dict = None
    
    def __post_init__(self):
        if self.data is None:
            self.data = {}


class EventManager:
    def __init__(self):
        self._listeners: Dict[EventType, List[callable]] = {}
        
    def subscribe(self, event_type: EventType, callback: callable):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
        
    def post(self, event: Event):
        if event.type in self._listeners:
            for callback in self._listeners[event.type]:
                callback(event)