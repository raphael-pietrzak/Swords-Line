import uuid
from Network.Client.clientTCP import TCPClient
from Network.Client.clientUDP import UDPClient


class Client:
    def __init__(self):
        self.uuid = str(uuid.uuid4()).split('-')[0]
        self.start()
    
    def start(self):
        self.udp_client = UDPClient()
        self.tcp_client = TCPClient()
        self.tcp_client.start()
        self.udp_client.start()
        self.send('Hello', 'TCP')


    def send(self, message, protocol):
        if protocol == 'TCP' and not self.tcp_client.is_running:
            print('TCP client not running')
            return

        
        match protocol:
            case 'TCP': self.tcp_client.send({self.uuid: message})
            case 'UDP': self.udp_client.client_data = {self.uuid: message}
            case _: return None
    
    
    def receive(self, protocol):
        match protocol:
            case 'TCP': return self.tcp_client.server_data
            case 'UDP': return self.udp_client.server_data
            case _: return None


    def is_online(self):
        return self.tcp_client.is_running and self.udp_client.is_running

    def menu_return(self):
        print('Back to menu')


    def close(self):
        self.udp_client.close()
        self.tcp_client.close()
    