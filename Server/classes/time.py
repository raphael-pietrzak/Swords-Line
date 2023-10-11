


class Cooldown:
    def __init__(self, cooldown):
        self.cooldown = cooldown
        self.timer = 0
        self.active = False


    def activate(self):
        self.active = True
    
    def update(self):
        if self.active:
            self.timer += 1
            if self.timer >= self.cooldown:
                self.active = False
                self.timer = 0