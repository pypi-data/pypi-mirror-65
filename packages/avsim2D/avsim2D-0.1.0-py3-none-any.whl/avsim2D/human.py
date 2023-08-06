
import pygame
import os

class HumanSprite(pygame.sprite.Sprite):
    """Human sprite object

        Definition of the human sprite

        Attributs
        ----------
        rect : pygame.Rect
        image : pygame.Surface
    """

    def __init__(self, x, y):
        """__init__ of Human sprite object

            initialisation of the human sprite

            Parameters
            ----------
            x : int
                x-axis position of the sprite rectangle
            y : int
                y-axis position of the sprite rectangle
        """
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 23, 43)
        self.image = pygame.Surface([32, 17])


class Human():
    """Human class

        This class manage the simulation of showing an human on the screen depending on the car sensors

        Attributs
        ----------
        self.human_sprite : Human_sprite
        self.human_image : pygame.image
        self.human_image_back : pygame.image
        self.vitesse : int
    """

    def __init__(self, x = 40, y = 40):
        """Initialisation of the Human object

        """

        self.human_sprite = HumanSprite(x, y)

        current_dir = os.path.dirname(os.path.abspath(__file__))
        human_path = os.path.join(current_dir, "Images/human.png")  
        human_back_path = os.path.join(current_dir, "Images/human_back.png")  

        self.human_image = pygame.image.load(human_path).convert_alpha()
        self.human_image_back = pygame.image.load(human_back_path).convert_alpha()
        self.speed = 1

    def update(self, screen):

        screen.blit(self.human_image, (self.human_sprite.rect.x * 8, self.human_sprite.rect.y * 8))




