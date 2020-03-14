import math

import pygame
from pygame.rect import Rect
from pygame.tests.ftfont_test import obj

from UIElements.Image import Image
from UIElements.Button import Button
from UIElements.Label import Label

pygame.init()


# user32 = ctypes.windll.user32
# print(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

# Window + loop
class Game:
    def __init__(self):
        self.window = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        pygame.display.set_caption("Bloons TD 7")
        icon = pygame.image.load('pictures/bloon.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        glogic = GameLogic()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left = 1
                    glogic.pressdown_left()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right = 3
                    glogic.pressdown_right()

            glogic.update()
            glogic.draw(self.window)
            self.window.blit(self.update_fps(), (10, 0))
            pygame.display.flip()
            self.clock.tick(100)
        pygame.quit()

    def update_fps(self):
        self.fps = str(int(self.clock.get_fps()))
        font = pygame.font.SysFont('monospace', 30)
        self.fps_text = font.render(self.fps, 1, pygame.Color("coral"))
        return self.fps_text


# updaten + Zeichnen
class GameLogic:
    def __init__(self):
        # player erstellen
        self.player = Player(1000, 3000)
        # towerliste
        self.towers = []
        # bloonliste
        self.bloons = []
        # projectileliste
        self.projectiles = []
        # wellen
        self.wave = Wave(0)
        # ui liste
        self.ui_elements = [
            Button(1620, 950, 280, 50, (107, 142, 35), (34, 139, 34), "Start"),
            Button(1620, 1020, 280, 50, (205, 92, 92), (178, 34, 34), "Exit"),
            Label(1620, 10, (255, 0, 0), "Lifepoints: ", self.player),
            Label(1620, 60, (255, 0, 0), "Money: ", self.player),
            Label(1620, 110, (255, 0, 0), "Wave: ", self.wave.wave),
            Image(1870, 20, "pictures\heart.png"),
            Image(1870, 70, "pictures\money.png"),
        ]

        # market
        self.shops = [Bananamarket(1615, 155)]
        # mouscoordinates
        self.mouse = pygame.mouse.get_pos()
        # später in menu class
        self.font = pygame.font.SysFont('monospace', 30)
        # grid
        self.grid = dict()
        for x in range(0, int(50)):  # 1600 pixel
            for y in range(0, int(34)):
                if y == 10 and x == 30:
                    self.grid[(x, y)] = Way(32, (x, y), (x - 1, y), (x, y + 1))
                elif 10 < y < 20 and x == 30:
                    self.grid[(x, y)] = Way(32, (x, y), (x, y - 1), (x, y + 1))
                elif y == 20 and x == 30:
                    self.grid[(x, y)] = Way(32, (x, y), (x, y - 1), (x + 1, y))
                elif y == 20 and 30 < x < 40:
                    self.grid[(x, y)] = Way(32, (x, y), (x - 1, y), (x + 1, y))
                elif y == 20 and x == 40:
                    self.grid[(x, y)] = Way(32, (x, y), (x - 1, y), (x, y - 1))
                elif 10 < y < 20 and x == 40:
                    self.grid[(x, y)] = Way(32, (x, y), (x, y + 1), (x, y - 1))
                elif y == 10 and x == 40:
                    self.grid[(x, y)] = Way(32, (x, y), (x, y + 1), (x + 1, y))
                elif y == 10 and (x > 40 or x < 30):
                    if x < 0:
                        self.grid[(x, y)] = Way(32, (x, y), (None, y), (x + 1, y))
                    elif x >= 60:
                        self.grid[(x, y)] = Way(32, (x, y), (x - 1, y), (None, y))
                    else:
                        self.grid[(x, y)] = Way(32, (x, y), (x - 1, y), (x + 1, y))
                else:
                    self.grid[(x, y)] = Cell(32, (x, y), (x * 2, y * 2, x + y))

    def draw(self, window):
        self.drawgrid(window)
        self.drawtowers(window)
        self.drawbloon(window)
        self.drawprojectile(window)
        self.drawmenu(window)

    def drawgrid(self, window):
        for coordinate, cell in self.grid.items():
            x, y = coordinate
            pygame.draw.rect(window, cell.colour, Rect(x * cell.width, y * cell.height, cell.width, cell.height))
            if self.grid[x, y].type == "way":
                self.grid[x, y].drawway(window)
            # else:
            #    self.grid[x, y].drawcell(window)

    def drawmenu(self, window):
        pygame.draw.rect(window, (176, 224, 230), Rect(1600, 0, 320, 1080))
        pygame.draw.rect(window, (238, 203, 173), Rect(1610, 150, 300, 925))
        for ui_element in self.ui_elements:
            ui_element.draw(window)
        for market in self.shops:
            market.drawmarket(window)
            for market in self.shops:
                if market.stick == True:
                    window.blit(market.towerimage,
                                (math.floor(self.mouse[0] / 32) * 32, math.floor(self.mouse[1] / 32) * 32))

    def drawtowers(self, window):
        for tower in self.towers:
            tower.drawtower(window)

    def drawbloon(self, window):
        for bloon in self.bloons:
            bloon.drawbloon(window)

    def drawprojectile(self, window):
        for projectile in self.projectiles:
            projectile.drawprojectile(window)

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        to_remove_bloons = []
        to_remove_projectiles = []

        self.wave.update(self.bloons)

        # bloon out of disolay
        for bloon in self.bloons:
            bloon.update(self.grid)
            if (bloon.posx, bloon.posy) not in self.grid:
                self.player.give_damage(bloon.health)
                to_remove_bloons.append(bloon)
        for bloon in to_remove_bloons:
            self.bloons.remove(bloon)

        # projectile out of display
        for projectile in self.projectiles:
            projectile.update()
            if (math.floor(projectile.posx), math.floor(projectile.posy)) not in self.grid:
                to_remove_projectiles.append(projectile)
        for projectile in to_remove_projectiles:
            self.projectiles.remove(projectile)

        # kabumm !!!
        for projectile in self.projectiles:
            for bloon in self.bloons:
                if math.sqrt(((projectile.posx + projectile.towersize / 2) - (bloon.posx + 1 / 2)) ** 2 + (
                        (projectile.posy + projectile.towersize / 2) - (bloon.posy + 1 / 2)) ** 2) <= 1:
                    if bloon in projectile.hitted_bloon:
                        break
                    else:
                        projectile.hitted_bloon.append(bloon)
                        if projectile.penetration > 1:
                            projectile.penetration -= 1
                            if bloon.health > projectile.damage:
                                bloon.health -= projectile.damage
                                self.player.money += projectile.damage
                            else:
                                self.player.money += bloon.health
                                self.bloons.remove(bloon)
                        else:
                            if bloon.health > projectile.damage:
                                bloon.health -= projectile.damage
                                self.player.money += projectile.damage
                                self.projectiles.remove(projectile)
                                break
                            else:
                                self.player.money += bloon.health
                                self.bloons.remove(bloon)
                                self.projectiles.remove(projectile)
                                break
        for i in range(len(self.bloons)):
            print(self.bloons[i].health)

        for tower in self.towers:
            tower.update(self.bloons, self.projectiles)

        for ui_element in self.ui_elements:
            if isinstance(ui_element, Label):
                ui_element.update(self.player, self.wave)
            elif isinstance(ui_element, Button):
                ui_element.update(pygame.mouse.get_pos())

        for market in self.shops:
            market.update(pygame.mouse.get_pos())

    def pressdown_left(self):
        self.is_button_clicked(pygame.mouse.get_pos())
        self.is_tower_possible_to_place(pygame.mouse.get_pos())

    def is_tower_possible_to_place(self, pos):
        for shop in self.shops:
            if shop.stick and pos[0] < 1568 and pos[1] < 1056:
                for tower in self.towers:
                    diffx = math.floor(pos[0] / 32) - tower.posx
                    diffy = math.floor(pos[1] / 32) - tower.posy
                    if -shop.towersize < diffx < shop.towersize and -shop.towersize < diffy < shop.towersize:
                        return
                for coordinates, cell in self.grid.items():
                    if isinstance(cell, Way):
                        diffx = math.floor(pos[0] / 32) - cell.posx
                        diffy = math.floor(pos[1] / 32) - cell.posy
                        if math.floor(pos[0] / 32) >= cell.posx \
                                and math.floor(pos[1] / 32) >= cell.posy:
                            if -1 < diffx < 1 and -1 < diffy < 1:
                                return
                        if math.floor(pos[0] / 32) <= cell.posx \
                                and math.floor(pos[1] / 32) <= cell.posy:
                            if -2 < diffx < 2 and -2 < diffy < 2:
                                return
                self.towers.append(BananaTower(32, math.floor(pos[0] / 32), math.floor(pos[1] / 32)))
                shop.stick = False
                self.player.money -= shop.price
            if shop.collidepoint(pos) and not shop.stick:
                shop.buy(self.player)

    def is_button_clicked(self, pos):
        for button in filter(lambda ui_element: isinstance(ui_element, Button), self.ui_elements):
            if button.collidepoint(pos):
                if button.text == "Exit":
                    pygame.quit()
                if button.text == "Start":
                    self.wave.spawn = True

    def pressdown_right(self):
        for market in self.shops:
            market.stick = False


# spezielle Zellen
class Cell:
    def __init__(self, cellsize, pos, colour=(0, 0, 0)):
        self.type = "normal"
        self.posx, self.posy = pos
        self.width = cellsize
        self.height = cellsize
        self.colour = colour
        self.image_gras = pygame.image.load('pictures/gras.png')

    def drawcell(self, window):
        window.blit(self.image_gras, (self.posx * 32, self.posy * 32))


class Way(Cell):
    def __init__(self, size, pos, previous, next):
        super().__init__(size, pos, (205, 133, 63))
        self.type = "way"
        self.previouscell = previous
        self.next = next
        self.image_grade_vertikal = pygame.image.load('pictures/grade.png')
        self.image_grade_horizontal = pygame.transform.rotate(self.image_grade_vertikal, 90)
        self.image_hoch_rechts = pygame.image.load('pictures/rechts.png')
        self.image_rechts_runter = pygame.transform.rotate(self.image_hoch_rechts, -90)
        self.image_runter_links = pygame.transform.rotate(self.image_hoch_rechts, -180)  # rechts-hoch
        self.image_links_hoch = pygame.transform.rotate(self.image_hoch_rechts, -270)  # runter-rechts

    def drawway(self, window):
        # grade-horizontal
        if (self.previouscell[0] != self.posx != self.next[0]) and (self.previouscell[1] == self.posy == self.next[1]):
            window.blit(self.image_grade_horizontal, (self.posx * 32, self.posy * 32))
        # grade-vertikal
        if (self.previouscell[0] == self.posx == self.next[0]) and (self.previouscell[1] != self.posy != self.next[1]):
            window.blit(self.image_grade_vertikal, (self.posx * 32, self.posy * 32))
        # hoch-rechts
        if (self.previouscell[0] == self.posx < self.next[0]) and (self.previouscell[1] > self.posy == self.next[1]):
            window.blit(self.image_hoch_rechts, (self.posx * 32, self.posy * 32))
        # rechts-runter
        if (self.previouscell[0] < self.posx == self.next[0]) and (self.previouscell[1] == self.posy < self.next[1]):
            window.blit(self.image_rechts_runter, (self.posx * 32, self.posy * 32))
        # runter-links
        # links-hoch
        # runter-rechts
        if (self.previouscell[0] == self.posx < self.next[0]) and (self.previouscell[1] < self.posy == self.next[1]):
            window.blit(self.image_links_hoch, (self.posx * 32, self.posy * 32))
        # rechts-hoch
        if (self.previouscell[0] < self.posx == self.next[0]) and (self.previouscell[1] == self.posy > self.next[1]):
            window.blit(self.image_runter_links, (self.posx * 32, self.posy * 32))


# Towerklassen
class BananaTower:
    def __init__(self, cellsize, x, y):
        self.cellsize = cellsize  # cellsize = 32 pixel (Zellgröße)
        self.posx = x
        self.posy = y
        self.towersize = 2
        self.damage = 1
        self.range = 20
        self.price = 100
        self.speed = 1 / 5
        self.activ = True
        self.cooldown = 100
        self.towerimage = pygame.image.load('pictures/bananawarrior.png')
        self.inrange = []
        self.now = self.cooldown
        self.angle = 45
        self.penetration = 3

    def update(self, bloons, projectiles):
        if self.now < self.cooldown and self.activ == False:
            self.now += 1
        if self.now == self.cooldown:
            self.now -= self.cooldown
            self.activ = True

        # bloons in radius finden
        for bloon in bloons:
            if math.sqrt((((self.posy + self.towersize / 2) - bloon.posy) ** 2) + (
                    ((self.posx + self.towersize / 2) - bloon.posx) ** 2)) <= self.range:
                self.inrange.append(bloon)
        for bloon in self.inrange:
            if math.sqrt((((self.posy + self.towersize / 2) - bloon.posy) ** 2) + (
                    ((self.posx + self.towersize / 2) - bloon.posx) ** 2)) > self.range:
                self.inrange.remove(bloon)

        # shoot
        if self.activ == True and len(self.inrange) > 0:
            self.activ = False
            self.last = pygame.time.get_ticks()
            projectiles.append(Bananaprojectile(32, self.posx, self.posy, self.speed, self.damage, self.towersize, (
                self.inrange[0].posx + self.inrange[0].progressx + 1 / 2,
                self.inrange[0].posy + self.inrange[0].progressy + 1 / 2), self.angle, self.penetration))

        self.inrange = []

    def drawtower(self, window):
        window.blit(self.towerimage, (self.posx * self.cellsize, self.posy * self.cellsize))


# Projektile
class Bananaprojectile:
    def __init__(self, cellsize, posx, posy, speed, damage, towersize, target, angle, penetration):
        self.tposx, self.tposy = target
        self.angle = angle
        self.towersize = towersize
        self.cellsize = cellsize
        self.speed = speed
        self.penetration = penetration
        self.posx = posx
        self.posy = posy
        self.damage = damage
        self.projectileimage = pygame.image.load('pictures/spear.png')
        self.startposx = posx
        self.startposy = posy
        self.dposy = self.tposy - (self.startposy + self.towersize / 2)
        self.dposx = self.tposx - (self.startposx + self.towersize / 2)
        self.progressfactor = self.speed / (math.sqrt((self.dposx * self.dposx) + (self.dposy * self.dposy)))
        self.hitted_bloon = []
        # für schuss nach update vor draw
        self.rot_image = pygame.transform.rotate(self.projectileimage, self.angle + 180)

        if self.dposy > 0:
            self.rot_image = pygame.transform.rotate(self.projectileimage, self.angle + (
                    180 + (math.atan(self.dposx / self.dposy) * 180 / math.pi)))

        elif self.dposy == 0 and self.dposx > 0:
            self.rot_image = pygame.transform.rotate(self.projectileimage, self.angle + 180 + 0.01)

        elif self.dposy == 0 and self.dposx < 0:
            self.rot_image = pygame.transform.rotate(self.projectileimage, self.angle + 0.01)

        elif self.dposy < 0:
            self.rot_image = pygame.transform.rotate(self.projectileimage,
                                                     self.angle + (math.atan(self.dposx / self.dposy) * 180 / math.pi))

    def drawprojectile(self, window):
        window.blit(self.rot_image, (
            (self.posx + self.towersize / 2) * self.cellsize, (self.posy + self.towersize / 2) * self.cellsize))

    def update(self):
        # fliegen
        self.posx += self.progressfactor * self.dposx
        self.posy += self.progressfactor * self.dposy


# Gegnerklasse
class Redbloon:
    def __init__(self, cellsize, x, y, health):
        self.progressx = 0
        self.progressy = 0
        self.cellsize = cellsize
        self.posx = x
        self.posy = y
        self.speed = [1 / 30, 1 / 15]
        self.value = 1
        self.health = int(health)
        self.bloonimages = [pygame.image.load('pictures/redbloon.png'), pygame.image.load('pictures/bluebloon.png')]

    def update(self, grid):
        if (self.posx, self.posy) not in grid:
            return
        nposx, nposy = grid[math.floor(self.posx), math.floor(self.posy)].next

        # oben
        if self.posx == nposx and self.posy - self.progressy >= nposy:
            if (self.progressy - self.speed[self.health - 1]) > (-1):
                self.progressy -= self.speed[self.health - 1]
            else:
                self.posy -= 1
                self.progressy = 0
        # rechts
        elif self.posx + self.progressx <= nposx and self.posy == nposy:
            if (self.progressx + self.speed[self.health - 1]) < 1:
                self.progressx += self.speed[self.health - 1]
            else:
                self.posx += 1
                self.progressx = 0
        # unten
        elif self.posx == nposx and self.posy + self.progressy <= nposy:
            if (self.progressy + self.speed[self.health - 1]) < 1:
                self.progressy += self.speed[self.health - 1]
            else:
                self.posy += 1
                self.progressy = 0
        # links
        elif self.posx - self.progressx >= nposx and self.posy == nposy:
            if (self.progressx - self.speed[self.health - 1]) > -1:
                self.progressx -= self.speed[self.health - 1]
            else:
                self.posx -= 1
                self.progressx = 0
        else:
            assert "Fehler no direction"
            print("posx %s, posy %s, progx %s progy %s" % (self.posx, self.posy, self.progressx, self.progressy))

    def drawbloon(self, window):
        window.blit(self.bloonimages[self.health - 1],
                    ((self.posx + self.progressx) * self.cellsize, (self.posy + self.progressy) * self.cellsize))


# wellen
class Wave:
    def __init__(self, start_wave):
        self.spawn = False
        self.now = 0
        self.wave = start_wave
        self.waves = dict()
        for wave in range(3):
            to_appand = []
            self.file = open("waves/wave" + str(wave), "r")
            for line in self.file:
                to_appand.append(line.split())
            self.waves[wave] = to_appand

    def update(self, bloons):
        if self.now == int(self.waves[self.wave][0][1]) and self.spawn:
            bloon_kind = self.waves[self.wave][0][0]
            if bloon_kind == "Redbloon":
                bloons.append(Redbloon(32, 0, 10, self.waves[self.wave][0][2]))
                self.waves[self.wave].pop(0)
            elif bloon_kind == "End":
                self.spawn = False
        if self.spawn == False and self.now > 0:
            self.wave += 1
            self.now = 0
        if self.spawn == True:
            self.now += 1


# Spieler
class Player:
    def __init__(self, lifepoints, money):
        self.lifepoints = lifepoints
        self.money = money

    def give_damage(self, damage):
        self.lifepoints -= damage


class Bananamarket:
    def __init__(self, posx, posy):
        self.towersize = 2
        self.cellsize = 32
        self.towerimage = pygame.image.load('pictures/bananawarrior.png')
        self.stick = False
        self.marketimage = pygame.image.load('pictures/banana.png')
        self.posx = posx
        self.posy = posy
        self.width = 64
        self.height = 64
        self.rect = Rect(self.posx, self.posy, self.width, self.height)
        self.originally_colour = (238, 232, 170)
        self.colour = (218, 165, 32)
        self.price = 100

    def update(self, mousecoordinates):
        mousex, mousey = mousecoordinates
        if (self.posx < mousex < (self.posx + self.width)) and (self.posy < mousey < (self.posy + self.height)):
            self.colour = (218, 165, 32)
        else:
            self.colour = self.originally_colour

    def drawmarket(self, window):
        pygame.draw.rect(window, self.colour, self.rect)
        window.blit(self.marketimage, (self.posx, self.posy))

    def collidepoint(self, mouse):
        mousex, mousey = mouse
        if (self.posx < mousex < (self.posx + self.width)) and (self.posy < mousey < (self.posy + self.height)):
            return True
        else:
            return False

    def buy(self, player):
        if player.money >= self.price:
            self.stick = True


# if __name__ == '__main__':
game = Game()
game.run()
