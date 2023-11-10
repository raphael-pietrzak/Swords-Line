
import json, socket, threading
from classes.ping import FPSCounter
from classes.settings import *


class TCPClient:
    def __init__(self):
        self.server_data = {}
        self.is_running = True

        self.network_fps_counter = FPSCounter('CLIENT TCP')

    
    def start(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((SERVER_IP, TCP_PORT))
            self.client_socket.settimeout(1.0)

            self.receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receive_thread.start()

        except ConnectionRefusedError:
            print('Connexion refused TCP client')
            self.close()


    def receive_messages(self):
        while self.is_running:
            try:
                
                data = self.client_socket.recv(BUFFER_SIZE)
                if not data:
                    break
                print('Reçu du server :', data.decode(ENCODING))
                self.server_data = json.loads(data.decode(ENCODING))

                self.network_fps_counter.ping()

            except TimeoutError:
                continue

            except OSError:
                break

        self.close()
        print('Thread TCP client receive terminated')
    

    def send(self, message):
        data = json.dumps(message)
        self.client_socket.send(data.encode(ENCODING))
    

    def close(self):
        self.is_running = False
        if self.client_socket:
            self.client_socket.close()
        print('TCP client properly closed')