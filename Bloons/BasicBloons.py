import pygame

from Bloons.Bloon import Bloon


class RedBloon(Bloon):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=1,
            speed=1/30,
            image=pygame.image.load('res/pictures/redbloon.png')
        )


class BlueBloon(Bloon):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=1,
            speed=1/15,
            image=pygame.image.load('res/pictures/bluebloon.png')
        )


class GreenBloon(Bloon):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=3,
            speed=1/10,
            image=pygame.image.load('res/pictures/green_bloon.png')
        )


class YellowBloon(Bloon):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            health=4,
            speed=1/5,
            image=pygame.image.load('res/pictures/yellow_bloon.png')
        )