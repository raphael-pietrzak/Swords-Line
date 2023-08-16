
# Configuration du client

SERVER_IP = '127.0.0.1'  # Localhost


# SERVER_IP = '127.0.0.1'  # Mettez l'adresse IP publique du serveur
# Configurez votre box en ouvrant une redirection de port
# 12345 vers l'adresse ip privée de votre ordi qui sert de serveur

SERVER_PORT = 12345     # Port d'écoute du serveur
BUFFER_SIZE = 2048

ANIMATION_SPEED = 10
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
PLAYER_SPEED = 1




EDITOR_DATA = {
    1 : {'type' : 'decoration', 'name' : 'dead', 'cols' : 7, 'rows' : 2, 'path' : 'graphics/Dead_and_Fire/Dead/Dead.png'},
    2 : {'type' : 'decoration', 'name' : 'fire', 'cols' : 7, 'rows' : 1, 'path' : 'graphics/Dead_and_Fire/Fire/Fire.png'},
    3 : {'type' : 'player', 'name' : 'goblins', 'cols' : 7, 'rows' : 3, 'path' : 'graphics/Factions/Goblins/Torch.png'},
    4 : {'type' : 'player', 'name' : 'knights', 'cols' : 6, 'rows' : 3, 'path' : 'graphics/Factions/Knights/Warrior.png'},
    5 : {'type' : 'terrain', 'name' : 'tree', 'cols' : 4, 'rows' : 1, 'path' : 'graphics/Terrain/Trees/Tree.png'},
}



# colors
RED_PLAYER = '#E01515'
RED_CONTOUR = '#950000'
BLUE_PLAYER = '#5ABEFF'
BLUE_CONTOUR = '#0047A4'


BUTTON_BG_COLOR = '#1C6225'
MENU_BG_COLOR = '#0F332C'
