import pygame

from UIElements.UIElement import UIElement


class Label(UIElement):
    def __init__(self, posx, posy, colour, text, player):
        super().__init__(posx, posy)
        self.colour = colour
        self.text = text
        self.player = player
        self.font = pygame.font.SysFont('Comic Sans MS', 30)

    def draw(self, window):
        window.blit(self.label, (self.posx, self.posy))

    def update(self, player, wave):
        if self.text == "Lifepoints: ":
            self.label = self.font.render(self.text + str(player.lifepoints), False, self.colour)
        elif self.text == "Money: ":
            self.label = self.font.render(self.text + str(player.money) + "$", False, self.colour)
        elif self.text == "Wave: ":
            self.label = self.font.render(self.text + str(wave.wave), False, self.colour)
