

import time


class FPSCounter:
    def __init__(self, name):
        self.name = name
        self.message_count = 0
        self.start_time = time.time()

    def ping(self):
        self.message_count += 1
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= 1.0:
            messages_per_second = self.message_count / elapsed_time
            print(f"[ MONITORING {self.name} ]: {messages_per_second:.2f}")
            self.message_count = 0
            self.start_time = time.time()