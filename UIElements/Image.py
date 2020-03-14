import pygame

from UIElements.UIElement import UIElement


class Image(UIElement):
    def __init__(self, posx, posy, file_name):
        super().__init__(posx, posy)
        self.image = pygame.image.load(file_name)

    def draw(self, window):
        window.blit(self.image, (self.posx, self.posy))

    def update(self):
        pass