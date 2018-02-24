import pygame
import math
from src import param


class Bonus(pygame.sprite.Sprite):
    SCORE_S = 1
    SCORE_M = 2
    SCORE_L = 3
    POWER_S = 11
    POWER_M = 12
    POWER_L = 13
    LIFE = 21

    def __init__(self, type, pos):
        pygame.sprite.Sprite.__init__(self)
        raw_img = pygame.image.load('../res/bullet/etama2.png')
        self.image = None
        if type == Bonus.POWER_M:
            self.image = raw_img.subsurface(
                (0, param.bonus_offset), (param.bonus_len, param.bonus_len))
        elif type == Bonus.POWER_L:
            self.image = raw_img.subsurface(
                (param.bonus_len * 3, param.bonus_offset), (param.bonus_len, param.bonus_len))

        if self.image == None:
            raise AttributeError

        self.rect = self.image.get_rect()
        self.rect.topleft = pos



    def move(self):
        self.rect.bottom += param.speed / 2

    def suck(self, pos):
        y, x = self.rect.topleft
        len = math.sqrt(pos[0] * pos[0] + pos[1] * pos[1])
        speedx = pos[1] / len * param.speed
        speedy = pos[0] / len * param.speed

        while abs(pos[1]-x) > param.speed or abs(pos[0] - y) > param.speed:
            if pos[1] > x:
                self.rect.left += speedx
            else:
                self.rect.left -= speedx
            if pos[0] > y:
                self.rect.top += speedy
            else:
                self.rect.top -= speedy