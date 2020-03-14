import pygame

from Projectiles.BananaProjectile import BananaProjectile
from Towers.Tower import Tower


class BananaWarrior(Tower):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            tower_size=2,
            damage=1,
            range=8,
            price=100,
            speed=1 / 4,
            cooldown=150,
            tower_image=pygame.image.load("res/pictures/Bananawarrior.png"),
            projectile_angle=45,
            penetration=3,
            projectile_kind=BananaProjectile)
