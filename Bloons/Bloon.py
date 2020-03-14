import math


class Bloon:
    def __init__(self, x, y, health, speed, image):
        self.progressx = 0
        self.progressy = 0
        self.posx = x
        self.posy = y
        self.speed = speed
        self.value = 1
        self.health = int(health)
        self.image = image

    def update(self, grid):
        if (self.posx, self.posy) not in grid:
            return
        nposx, nposy = grid[math.floor(self.posx), math.floor(self.posy)].next

        # oben
        if self.posx == nposx and self.posy - self.progressy >= nposy:
            if (self.progressy - self.speed) > (-1):
                self.progressy -= self.speed
            else:
                self.posy -= 1
                self.progressy = 0
        # rechts
        elif self.posx + self.progressx <= nposx and self.posy == nposy:
            if (self.progressx + self.speed) < 1:
                self.progressx += self.speed
            else:
                self.posx += 1
                self.progressx = 0
        # unten
        elif self.posx == nposx and self.posy + self.progressy <= nposy:
            if (self.progressy + self.speed) < 1:
                self.progressy += self.speed
            else:
                self.posy += 1
                self.progressy = 0
        # links
        elif self.posx - self.progressx >= nposx and self.posy == nposy:
            if (self.progressx - self.speed) > -1:
                self.progressx -= self.speed
            else:
                self.posx -= 1
                self.progressx = 0
        else:
            assert "Fehler no direction"
            print("posx %s, posy %s, progx %s progy %s" % (self.posx, self.posy, self.progressx, self.progressy))

    def draw(self, window):
        window.blit(self.image, ((self.posx + self.progressx) * 32, (self.posy + self.progressy) * 32))
