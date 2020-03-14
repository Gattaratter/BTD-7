import math

import pygame
from pygame.rect import Rect

from MapLoader import MapLoader
from Player import Player
from UIElements.Image import Image
from UIElements.Button import Button
from UIElements.Label import Label
from MapElements.WayCell import WayCell
from Towers.BananaWarrior import BananaWarrior

# user32 = ctypes.windll.user32
# print(user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

# Window + loop
from Level import Level


class Game:
    def __init__(self):
        self.window = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.title = "Bloons TD 7"
        pygame.display.set_caption(self.title)
        icon = pygame.image.load('res/pictures/bloon.png')
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()

    def run(self):
        running = True

        glogic = GameLogic()
        while running:
            glogic.handle_input()
            glogic.update()
            glogic.draw(self.window)
            pygame.display.set_caption("Bloons TD 7 - %s" % self.update_fps())
            self.window.blit(self.update_fps(), (10, 0))
            pygame.display.flip()
            self.clock.tick(500)
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
        self.level = Level.from_file("res/level/level_1.json")
        # ui liste
        self.ui_elements = [
            Button(1620, 950, 280, 50, (107, 142, 35), (34, 139, 34), "Start", self.set_spawn_true),
            Button(1620, 1020, 280, 50, (205, 92, 92), (178, 34, 34), "Exit", exit),
            Label(1620, 10, (255, 0, 0), "Lifepoints: ", self.player),
            Label(1620, 60, (255, 0, 0), "Money: ", self.player),
            Label(1620, 110, (255, 0, 0), "Wave: ", self.level.curr_wave),
            Image(1870, 20, "res\pictures\heart.png"),
            Image(1870, 70, "res\pictures\money.png"),
        ]

        # market
        self.shops = [Bananamarket(1615, 155)]
        # mouscoordinates
        self.mouse = pygame.mouse.get_pos()
        # später in menu class
        self.font = pygame.font.SysFont('monospace', 30)
        # grid
        self.grid = MapLoader.zwerg_101()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left = 1
                self.pressdown_left()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Right = 3
                self.pressdown_right()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                exit(-1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.set_spawn_true()

    def draw(self, window):
        self.draw_grid(window)
        self.draw_towers(window)
        self.draw_bloons(window)
        self.draw_projectiles(window)
        self.draw_menu(window)

    def draw_grid(self, window):
        for coordinate, cell in self.grid.items():
            x, y = coordinate
            #pygame.draw.rect(window, cell.colour, Rect(x * cell.width, y * cell.height, cell.width, cell.height))
            if isinstance(self.grid[x, y], WayCell):
                self.grid[x, y].drawway(window)
            else:
                self.grid[x, y].drawcell(window)

    def draw_menu(self, window):
        pygame.draw.rect(window, (176, 224, 230), Rect(1600, 0, 320, 1080))
        pygame.draw.rect(window, (238, 203, 173), Rect(1610, 150, 300, 925))
        for ui_element in self.ui_elements:
            ui_element.draw(window)
        for market in self.shops:
            market.draw(window)
            for market in self.shops:
                if market.stick:
                    window.blit(market.towerimage,
                                (math.floor(self.mouse[0] / 32) * 32, math.floor(self.mouse[1] / 32) * 32))

    def draw_towers(self, window):
        for tower in self.towers:
            tower.draw(window)

    def draw_bloons(self, window):
        for bloon in self.bloons:
            bloon.draw(window)

    def draw_projectiles(self, window):
        for projectile in self.projectiles:
            projectile.draw(window)

    def update(self):
        self.mouse = pygame.mouse.get_pos()
        to_remove_bloons = []
        to_remove_projectiles = []

        self.level.update(self.bloons)

        # bloon out of display
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

        for tower in self.towers:
            tower.update(self.bloons)
            tower.shoot(self.projectiles)

        for ui_element in self.ui_elements:
            if isinstance(ui_element, Label):
                ui_element.update(self.player, self.level)
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
                        break
                for coordinates, cell in self.grid.items():
                    if isinstance(cell, WayCell):
                        diffx = math.floor(pos[0] / 32) - cell.posx
                        diffy = math.floor(pos[1] / 32) - cell.posy
                        if math.floor(pos[0] / 32) >= cell.posx \
                                and math.floor(pos[1] / 32) >= cell.posy:
                            if -1 < diffx < 1 and -1 < diffy < 1:
                                break
                        if math.floor(pos[0] / 32) <= cell.posx \
                                and math.floor(pos[1] / 32) <= cell.posy:
                            if -2 < diffx < 2 and -2 < diffy < 2:
                                break
                self.towers.append(BananaWarrior(math.floor(pos[0] / 32), math.floor(pos[1] / 32)))
                shop.stick = False
                self.player.money -= shop.price
            if shop.collidepoint(pos) and not shop.stick:
                shop.buy(self.player)

    def is_button_clicked(self, pos):
        for button in filter(lambda ui_element: isinstance(ui_element, Button), self.ui_elements):
            if button.collidepoint(pos):
                button.execute()

    def set_spawn_true(self):
        self.level.spawn = True

    def pressdown_right(self):
        for market in self.shops:
            market.stick = False

class Bananamarket:
    def __init__(self, posx, posy):
        self.towersize = 2
        self.cellsize = 32
        self.towerimage = pygame.image.load('res/pictures/bananawarrior.png')
        self.stick = False
        self.marketimage = pygame.image.load('res/pictures/banana.png')
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

    def draw(self, window):
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


if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
