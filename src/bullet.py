import pygame
import math
from src import param


# rect image 是继承的属性
class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.speed = param.speed * 8

    def move(self):
        self.rect.bottom -= self.speed


class AlgoBullet(pygame.sprite.Sprite):
    INVOLUTE_HELICOID = 1
    ARTCHIMEDES = 2

    def __init__(self, bullet_img, pos, fun):
        #super(Bullet, self).__init__(self, bullet_img, pos)
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.speed = param.speed

        #self.pos = pos # 发射者原位置

        self.fun = fun
        self.var = 1

    def move(self):
        if self.fun == AlgoBullet.INVOLUTE_HELICOID:
            self.var += 0.0001
            r = 1
            ang = 360 * self.var
            s = 2 * math.pi * r * self.var
            x0 = s * math.cos(ang)
            y0 = s * math.sin(ang)
            x = x0 + s * math.sin(ang)
            y = y0 - s * math.cos(ang)
            #print('%d, %d' %(x, y))
            self.rect.left += x
            self.rect.top += y
        elif self.fun == AlgoBullet.ARTCHIMEDES:
            self.rect.left += self.speedx # 动态属性！！！
            self.rect.top -= self.speedy

