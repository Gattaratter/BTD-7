import math



class Tower:
    def __init__(self, x, y, tower_size, damage, range, price, speed, cooldown, tower_image, projectile_angle,
                 penetration, projectile_kind):
        self.posx = x
        self.posy = y
        self.tower_size = tower_size
        self.damage = damage
        self.range = range
        self.price = price
        self.speed = speed
        self.active = True
        self.cooldown = cooldown
        self.towerimage = tower_image
        self.inrange = []
        self.frames_since_last_shoot = self.cooldown
        self.projectile_angle = projectile_angle
        self.penetration = penetration
        self.projectile_kind = projectile_kind

    def update(self, bloons):
        if self.frames_since_last_shoot < self.cooldown and not self.active:
            self.frames_since_last_shoot += 1
        if self.frames_since_last_shoot == self.cooldown:
            self.frames_since_last_shoot -= self.cooldown
            self.active = True

        # bloons in radius finden
        for bloon in bloons:
            if math.sqrt((((self.posy + self.tower_size / 2) - bloon.posy) ** 2) + (
                    ((self.posx + self.tower_size / 2) - bloon.posx) ** 2)) <= self.range:
                self.inrange.append(bloon)
        for bloon in self.inrange:
            if math.sqrt((((self.posy + self.tower_size / 2) - bloon.posy) ** 2) + (
                    ((self.posx + self.tower_size / 2) - bloon.posx) ** 2)) > self.range:
                self.inrange.remove(bloon)

    def shoot(self, projectiles):
        if self.active and len(self.inrange) > 0:
            self.active = False
            projectiles.append(
                self.projectile_kind(self.posx, self.posy, self.speed, self.damage, self.tower_size, (
                    self.inrange[0].posx + self.inrange[0].progressx + 1 / 2,
                    self.inrange[0].posy + self.inrange[0].progressy + 1 / 2), self.projectile_angle, self.penetration))
        self.inrange = []

    def draw(self, window):
        window.blit(self.towerimage, (self.posx * 32, self.posy * 32))
