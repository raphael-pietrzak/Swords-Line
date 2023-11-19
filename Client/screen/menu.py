class Carrousel:
    def __init__(self):
        self.screens = ["shop", "collection", "battle", "clan", "events"]
        self.current_screen = 0

    
    def event_loop(self):


    def next_screen(self):
        self.current_screen_index = (self.current_screen_index + 1) % len(self.screens)

    def previous_screen(self):
        self.current_screen_index = (self.current_screen_index - 1) % len(self.screens)

    def display_pagination(self):
        pagination = " ".join(["●" if i == self.current_screen_index else "○" for i in range(len(self.screens))])
        print(f"Pagination : {pagination}")

        





class Shop:
    def __init__(self):
        self.cards = []
        self.gold = 0
        self.gems = 0
        self.chests = []

class Collection:
    def __init__(self):
        self.cards = []


class Battle:
    def __init__(self):
        self.battle_button = Button("Battle")
        self.chest_slots = [ChestSlot() for _ in range(4)]

class Clan:
    def __init__(self):
        self.clan_button = Button("Clan")

class Events:
    def __init__(self):
        self.events_button = Button("Events")


class Button:
    def __init__(self, text):
        self.text = text

class ChestSlot:
    def __init__(self):
        self.is_empty = True
