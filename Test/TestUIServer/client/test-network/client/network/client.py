import socket
import threading
import pickle
from config import SERVER_HOST, SERVER_PORT, BUFFER_SIZE

class NetworkClient:
    def __init__(self):
        self.socket = None
        self.receive_thread = None
        self.message_handler = None
        self.connected = False

    def connect(self, player_name, host=SERVER_HOST, port=SERVER_PORT):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, port))
            self.connected = True
            
            self.send_message({
                "type": "JOIN",
                "name": player_name
            })
            
            self.receive_thread = threading.Thread(target=self._receive_loop)
            self.receive_thread.daemon = True
            self.receive_thread.start()
            
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def _receive_loop(self):
        while self.connected:
            try:
                data = self.socket.recv(BUFFER_SIZE)
                if not data:
                    break
                message = pickle.loads(data)
                if self.message_handler:
                    self.message_handler(message)
            except:
                break
        self.connected = False

    def send_message(self, message):
        if self.connected:
            try:
                self.socket.sendall(pickle.dumps(message))
                return True
            except:
                return False
        return False

    def set_message_handler(self, handler):
        self.message_handler = handler

    def disconnect(self):
        self.connected = False
        if self.socket:
            self.socket.close()
