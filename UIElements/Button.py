import pygame
from pygame.rect import Rect

from UIElements.UIElement import UIElement


class Button(UIElement):
    def __init__(self, posx, posy, width, height, colour, hovercolour, text):
        super().__init__(posx, posy)
        self.width = width
        self.height = height
        self.colour = colour
        self.hovercolour = hovercolour
        self.originally_colour = colour
        self.text = text
        self.font = pygame.font.SysFont('monospace', 50)
        self.button = self.font.render(self.text, True, (0, 0, 0))
        self.rect = Rect(self.posx, self.posy, self.width, self.height)

    def update(self, mousecoordinates):
        mousex, mousey = mousecoordinates
        if (self.posx < mousex < (self.posx + self.width)) and (self.posy < mousey < (self.posy + self.height)):
            self.colour = self.hovercolour
        else:
            self.colour = self.originally_colour

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)
        window.blit(self.button, self.rect.topleft)

    def collidepoint(self, mouse):
        mousex, mousey = mouse
        if (self.posx < mousex < (self.posx + self.width)) and (self.posy < mousey < (self.posy + self.height)):
            return True
        else:
            return False
