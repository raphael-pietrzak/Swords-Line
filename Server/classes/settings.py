
ANIMATION_SPEED = 10

HOST = "192.168.1.20"
SERVER_IP = "86.210.13.172"
UDP_PORT = 12345
TCP_PORT = 54321

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 700

BUFFER_SIZE = 1024
ENCODING = 'utf-8'

EDITOR_DATA = {
    1 : {'type' : 'decoration', 'name' : 'dead', 'grid' : (7, 2), 'path' : 'graphics/Dead_and_Fire/Dead/Dead.png'},
    2 : {'type' : 'decoration', 'name' : 'fire', 'grid' : (7, 1), 'path' : 'graphics/Dead_and_Fire/Fire/Fire.png'},
    3 : {'type' : 'player', 'name' : 'goblin', 'grid' : (7,  3), 'path' : 'graphics/Factions/Goblins/Torch.png'},
    4 : {'type' : 'player', 'name' : 'knight', 'grid' : (6,  3), 'path' : 'graphics/Factions/Knights/Warrior.png'},
    5 : {'type' : 'terrain', 'name' : 'tree', 'grid' : (4, 1), 'path' : 'graphics/Terrain/Trees/Tree.png'},
    6 : {'type' : 'terrain', 'name' : 'tree_fire', 'grid' : (4,  1), 'path' : 'graphics/Terrain/Trees/Tree_on_Fire.png'},
    7 : {'type' : 'ressources', 'name' : 'pinecone', 'grid' : None, 'path' : 'graphics/Ressources/Pinecone.png'},
    8 : {'type' : 'ressources', 'name' : 'twigs', 'grid' : None, 'path' : 'graphics/Ressources/Twigs.png'},
    9 : {'type' : 'ressources', 'name' : 'log', 'grid' : None, 'path' : 'graphics/Ressources/Log.png'},
    10 : {'type' : 'ressources', 'name' : 'gold', 'grid' : None, 'path' : 'graphics/Ressources/Gold.png'},
    11 : {'type' : 'building', 'name' : 'goblin_house', 'grid' : None, 'path' : 'graphics/Factions/Goblins/Goblin_House.png'},
    12 : {'type' : 'building', 'name' : 'knight_house', 'grid' : None, 'path' : 'graphics/Factions/Knights/Knight_House.png'},
}




# colors
RED_PLAYER = '#E01515'
RED_CONTOUR = '#950000'
BLUE_PLAYER = '#5ABEFF'
BLUE_CONTOUR = '#0047A4'


BUTTON_BG_COLOR = '#1C6225'
MENU_BG_COLOR = '#0F332C'
