import pygame

from MapElements.MapCell import MapCell


class WayCell(MapCell):
    def __init__(self, size, pos, previous, next):
        super().__init__(size, pos, (205, 133, 63))
        self.previouscell = previous
        self.next = next
        self.image_grade_vertikal = pygame.image.load('res/pictures/grade.png').convert()
        self.image_grade_horizontal = pygame.transform.rotate(self.image_grade_vertikal, 90)
        self.image_hoch_rechts = pygame.image.load('res/pictures/rechts.png').convert()
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