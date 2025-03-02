from network.network import NetworkServer
from config import ServerConfig
import signal
import sys

class Main:
    def __init__(self):
        self.server = None

    def signal_handler(self, sig, frame):
        print("\nArrêt du serveur...")
        if self.server:
            self.server.stop()
        sys.exit(0)

    def run(self):
        # Configuration du gestionnaire de signal pour Ctrl+C
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # Création et démarrage du serveur
        self.server = NetworkServer(ServerConfig)
        if self.server.start():
            print("Serveur prêt. Appuyez sur Ctrl+C pour arrêter.")
            # Maintenir le thread principal en vie
            signal.pause()

if __name__ == "__main__":
    main = Main()
    main.run()
