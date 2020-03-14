import pygame


class MapCell:
    def __init__(self, cellsize, pos, colour=(0, 0, 0)):
        self.posx, self.posy = pos
        self.width = cellsize
        self.height = cellsize
        self.colour = colour
        self.image_gras = pygame.image.load('res/pictures/gras.png').convert()

    def drawcell(self, window):
        window.blit(self.image_gras, (self.posx * 32, self.posy * 32))