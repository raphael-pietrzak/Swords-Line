import time
from network.serverTCP import TCPServer
from network.serverUDP import UDPServer
from menu.online_indicator import ConnectionState, OnlineIndicator

class Server:
    def __init__(self):
        self.online = True
        self.online_indicator = OnlineIndicator(self.online)
        self.start()
        

    def start(self):
        self.udp_server = UDPServer()
        self.udp_server.start()

        self.tcp_server = TCPServer(self.del_udp_client)
        self.tcp_server.start()

        self.online = True






    def toggle(self):
        self.start() if not self.online else self.close()

        
    
    def send(self, message, protocol):
        match protocol:
            case 'TCP': self.tcp_server.send(message)
            case 'UDP': self.udp_server.server_data = message
            case _: return None
                

    def receive(self, protocol):
        match protocol:
            case 'TCP': return self.tcp_server.get_clients_data()           
            case 'UDP': return self.udp_server.client_data          
            case _: return None
    


    def get_new_clients(self):
        new_clients = self.tcp_server.new_clients
        self.tcp_server.new_clients = []
        return new_clients

    def get_del_clients(self):
        del_clients = self.tcp_server.del_clients
        self.tcp_server.del_clients = []
        return del_clients
    


    def del_udp_client(self, uuid):
        if uuid in self.udp_server.client_data:
            del self.udp_server.client_data[uuid]

    
    def update_indicator(self):
        if not self.online:
            self.online_indicator.change_state(ConnectionState.OFFLINE)
            return
        if self.udp_server.is_running or self.tcp_server.is_running:
            self.online_indicator.change_state(ConnectionState.ONLINE)
        else:
            self.online_indicator.change_state(ConnectionState.WAITING)
    

    def close(self):
        self.udp_server.close()
        self.tcp_server.close()
        self.online = False
        self.online_indicator.change_state(ConnectionState.OFFLINE)
    
