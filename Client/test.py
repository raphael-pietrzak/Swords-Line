import threading, time

class Main:
    def __init__(self):
        self.count = 0
        self.running = True
        self.thread = threading.Thread(target=self.print_count)
        self.thread.start()


    def print_count(self):
        while self.running:
            self.count += 1
            print(self.count)
            time.sleep(1)

    def run(self):
        while self.running:
            print("Boucle de test")
            time.sleep(1)
            if self.count == 10:
                self.running = False
        


if __name__ == "__main__":
    main = Main()
    main.run()