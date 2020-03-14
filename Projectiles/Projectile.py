import math

import pygame


class Projectile:
    def __init__(self, posx, posy, speed, damage, towersize, target, angle, penetration, projectil_image):
        self.tposx, self.tposy = target
        self.angle = angle
        self.towersize = towersize
        self.speed = speed
        self.penetration = penetration
        self.posx = posx
        self.posy = posy
        self.damage = damage
        self.projectile_image = projectil_image
        self.startposx = posx
        self.startposy = posy
        self.dposy = self.tposy - (self.startposy + self.towersize / 2)
        self.dposx = self.tposx - (self.startposx + self.towersize / 2)
        self.progressfactor = self.speed / (math.sqrt((self.dposx * self.dposx) + (self.dposy * self.dposy)))
        self.hitted_bloon = []
        self.rot_image = pygame.transform.rotate(self.projectile_image, self.angle + 180)

        if self.dposy > 0:
            self.rot_image = pygame.transform.rotate(self.projectile_image, self.angle + (
                    180 + (math.atan(self.dposx / self.dposy) * 180 / math.pi)))

        elif self.dposy == 0 and self.dposx > 0:
            self.rot_image = pygame.transform.rotate(self.projectile_image, self.angle + 180 + 0.01)

        elif self.dposy == 0 and self.dposx < 0:
            self.rot_image = pygame.transform.rotate(self.projectile_image, self.angle + 0.01)

        elif self.dposy < 0:
            self.rot_image = pygame.transform.rotate(self.projectile_image,
                                                     self.angle + (math.atan(self.dposx / self.dposy) * 180 / math.pi))

    def draw(self, window):
        window.blit(self.rot_image, (
            (self.posx + self.towersize / 2) * 32, (self.posy + self.towersize / 2) * 32))

    def update(self):
        self.posx += self.progressfactor * self.dposx
        self.posy += self.progressfactor * self.dposy
