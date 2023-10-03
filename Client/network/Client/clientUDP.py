
import json
import socket
import threading
import time

from ping import FPSCounter
from settings import *



class UDPClient(threading.Thread):
    def __init__(self, ):
        super().__init__()

        self.is_running = True

        self.server_data = {}
        self.client_data = {}


        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(1.0)

        self.receive_thread = threading.Thread(target=self.receive, daemon=True)
        self.receive_thread.start()


        self.network_fps_counter = FPSCounter('CLIENT UDP')



    def run(self):
        while self.is_running:
            try:
                self.client_socket.sendto(json.dumps(self.client_data).encode(ENCODING), (SERVER_IP, UDP_PORT))
                time.sleep(0.001)

                self.network_fps_counter.ping()

            except TimeoutError:
                print('Timeout UDP client send')

            except OSError:
                print('Connexion lost UDP client')
        print('Thread UDP client send terminated')


    def receive(self):
        while self.is_running:
            try:
                response, addr = self.client_socket.recvfrom(BUFFER_SIZE)
                self.server_data = json.loads(response.decode(ENCODING))
                time.sleep(0.001)

            except TimeoutError:
                print('Back to the menu')
                self.close()

            except Exception as e:
                print(f'Error UDP client receive: {e}')
        
        print('Thread UDP client receive terminated')
    

    def close(self):
        self.is_running = False
        self.server_data = {}
        if self.client_socket:
            self.client_socket.close()

