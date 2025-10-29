
from src.menu.slider import MenuSlider

class Main:
    def __init__(self):
        self.menu = MenuSlider(800, 600)

    def run(self):
        self.menu.run()

if __name__ == "__main__":
    main = Main()
    main.run()