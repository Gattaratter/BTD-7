import pygame

from Projectiles.Projectile import Projectile


class BananaProjectile(Projectile):
    def __init__(self, x, y, speed, damage, towersize, target, angle, penetration):
        super().__init__(x, y, speed, damage, towersize, target, angle, penetration,
                         projectil_image=pygame.image.load("res/pictures/spear.png"))