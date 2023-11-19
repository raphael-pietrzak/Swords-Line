class Carousel:
    def __init__(self):
        self.screens = ["shop", "collection", "battle", "clan", "events"]
        self.current_screen_index = 0

    def display_current_screen(self):
        """
        Affiche le contenu de l'écran actuel.
        """
        current_screen = self.screens[self.current_screen_index]
        print(f"Affichage de l'écran : {current_screen}")

    def next_screen(self):
        """
        Passe à l'écran suivant dans le carrousel.
        """
        self.current_screen_index = (self.current_screen_index + 1) % len(self.screens)

    def previous_screen(self):
        """
        Passe à l'écran précédent dans le carrousel.
        """
        self.current_screen_index = (self.current_screen_index - 1) % len(self.screens)

    def display_pagination(self):
        """
        Affiche les indicateurs de position (bulles) pour chaque écran dans le carrousel.
        """
        pagination = " ".join(["●" if i == self.current_screen_index else "○" for i in range(len(self.screens))])
        print(f"Pagination : {pagination}")

# Exemple d'utilisation
carousel = Carousel()

# Affiche l'écran actuel
carousel.display_current_screen()

# Affiche la pagination initiale
carousel.display_pagination()

# Passe à l'écran suivant
carousel.next_screen()
carousel.display_current_screen()
carousel.display_pagination()

# Passe à l'écran précédent
carousel.previous_screen()
carousel.display_current_screen()
carousel.display_pagination()


# Passe à l'écran suivant
carousel.next_screen()
carousel.display_current_screen()
carousel.display_pagination()

# Passe à l'écran suivant
carousel.next_screen()
carousel.display_current_screen()
carousel.display_pagination()

# Passe à l'écran suivant
carousel.next_screen()
carousel.display_current_screen()
carousel.display_pagination()