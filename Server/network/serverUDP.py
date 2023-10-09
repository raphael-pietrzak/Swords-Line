import json, socket, threading
from classes.ping import FPSCounter
from classes.settings import *



class UDPServer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.is_running = True

        self.client_data = {}
        self.server_data = {}

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.bind()

  

    def bind(self):
        try:
            self.server_socket.bind((HOST, UDP_PORT))
        except OSError:
            print(f"Serveur UDP failed to connect")
            self.is_running = False

    def run(self):
        print(f"Serveur UDP en écoute sur {HOST}:{UDP_PORT} ...")

        self.network_fps_counter = FPSCounter('SERVER UDP')
        while self.is_running:
            try:
                data, addr = self.server_socket.recvfrom(BUFFER_SIZE)
                data = json.loads(data.decode(ENCODING)) 
                if not data: continue

                uuid = data['uuid']
                message = data['message']
                self.client_data[uuid] = message


                self.server_socket.sendto(json.dumps(self.server_data).encode(ENCODING), addr)

                self.network_fps_counter.ping()

            
            except TimeoutError:
                continue

            except Exception as e:
                # print(f'########   Error UDP server : {e}   ########')
                continue
        
        print('Thread UDP server terminated')

    

    def close(self):
        self.is_running = False
        self.server_socket.close()
