from Network.Server.serverTCP import TCPServer
from Network.Server.serverUDP import UDPServer


class Server:
    def __init__(self):

        self.clients = {}

        self.udp_server = UDPServer(self.clients)
        self.udp_server.start()

        self.tcp_server = TCPServer(self.clients)
        self.tcp_server.start()

        
    
    def send(self, message, protocol):
        match protocol:
            case 'TCP': self.tcp_server.send(message)
            case 'UDP': self.udp_server.server_data = message
            case _: return None
                

    def receive(self, protocol):
        match protocol:
            case 'TCP': return self.tcp_server.data_received
            case 'UDP': return self.udp_server.clients
            case _: return None
    

    def close(self):
        self.udp_server.close()
        self.tcp_server.close()
