# config.py

class ServerConfig:
    HOST = ''  # Vide pour accepter les connexions de toutes les interfaces
    PORT = 5555
    MAX_CONNECTIONS = 10
    BUFFER_SIZE = 4096
    ROOM_CLEANUP_DELAY = 300  # 5 minutes
    UPDATE_INTERVAL = 0.1

