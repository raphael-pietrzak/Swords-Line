class Player:
    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name
        self.character = None
        self.room_id = None

    def set_character(self, character_id):
        self.character = character_id

    def set_room(self, room_id):
        self.room_id = room_id
