import time

class LogManager:
    def __init__(self):
        self.logs = []
        self.max_logs = 100

    
    def add_log(self, message, log_type="INFO"):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.logs.append({"time": timestamp, "type": log_type, "message": message})
        if len(self.logs) > self.max_logs:
            self.logs.pop(0)

    def get_logs(self):
        return self.logs

    def clear_logs(self):
        self.logs = []
        print("Logs cleared")