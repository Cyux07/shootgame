import pygame
import math
from enum import Enum

from src import param
from src.bullet import AlgoBullet


class Enemy(pygame.sprite.Sprite):
    Body = Enum('Body', ('Center', 'Move', 'Down'))

    def __init__(self, img, pos):
        pygame.sprite.Sprite.__init__(self)
        self.__image = []
        self.__move_img = []
        self.__down_img = []
        enemy_img = pygame.image.load(img)
        for i in range(0, param.enemy_frame):
            self.__image.append(enemy_img.subsurface(
                (param.ENEMY_WIDTH * i, param.ENEMY_OFFSET),
                (param.ENEMY_WIDTH, param.ENEMY_HEIGHT)))
        for i in range(param.enemy_frame, param.enemy_frame + param.emove_frame):
            self.__move_img.append(enemy_img.subsurface(
                (param.ENEMY_WIDTH * i, param.ENEMY_OFFSET),
                (param.ENEMY_WIDTH, param.ENEMY_HEIGHT)))
        for i in range(0, param.edown_frame):
            self.__down_img.append(enemy_img.subsurface(
                (param.EDOWN_OFFSETW+param.ENEMY_WIDTH * i, param.EDOWN_OFFSETH),
                (param.ENEMY_WIDTH, param.ENEMY_HEIGHT)))

        self.rect = self.__image[0].get_rect()
        self.rect.topleft = pos
        self.speed = param.speed
        self.img_index = 0
        self.body_mode = Enemy.Body.Center
        # TODO 自定义的获取这两个参数
        self.bullets = pygame.sprite.Group()
        rawimg = pygame.image.load('../res/bullet/etama.png')
        self.bullet_img = rawimg.subsurface((param.enemy_bullet, param.enemy_bullet), (param.enemy_bullet, param.enemy_bullet))
        self.period = 4000 #ms 发射子弹周期
        self.frequen = 5
        self.var = 1 # 控制子弹轨道函数的变量
        self.is_frequen_over = False

    @property
    def img(self):
        try:
            if self.body_mode == Enemy.Body.Center:
                return self.__image[self.img_index]
            elif self.body_mode == Enemy.Body.Move:
                return self.__move_img[self.img_index]
            elif self.body_mode == Enemy.Body.Down:
                return self.__down_img[self.img_index]
        finally:
            if self.body_mode == Enemy.Body.Center:
                self.img_index = (self.img_index + 1) % param.enemy_frame

    def shoot(self):
        if True:
            a = 1.68
            a2 = 5.0
            b = 7.0
            c = 2.2
            while True:
                if not len(self.bullets) == 0:
                    pass #wait for 一轮子弹在屏幕上过完
                else:
                    self.is_frequen_over = False
                    try:

                        for i in range(0, 400):
                            if True:
                                theta = 360 * i * 10
                                x = (a2 - b) * math.cos(theta) + c * math.cos((a2 / b - 1) * theta)*100
                                y = (a2 - b) * math.sin(theta) - c * math.sin((a2 / b - 1) * theta)*100
                                # -----------
                                radian = math.atan(y / x)
                                ro_angle = math.degrees(radian)
                                bullet = AlgoBullet(pygame.transform.rotate(self.bullet_img, -ro_angle),
                                                    [self.rect.centerx + x, self.rect.centery - y],
                                                    AlgoBullet.ARTCHIMEDES)
                                bullet.speedx = param.speed * math.cos(radian) * 10
                                bullet.speedy = -param.speed * math.sin(radian) * 10
                                self.bullets.add(bullet)
                                # -----------这一坨重构
                            else:
                                seta = i / 10.0
                                r = math.pow(a, seta)
                                x = r * math.cos(seta)
                                y = r * math.sin(seta)
                                radian = math.atan(y/x)
                                ro_angle = math.degrees(radian)
                                bullet = AlgoBullet(pygame.transform.rotate(self.bullet_img, -ro_angle),
                                                    [self.rect.centerx + x, self.rect.centery - y],
                                                    AlgoBullet.ARTCHIMEDES)
                                bullet.speedx = param.speed * math.cos(radian) * 10
                                bullet.speedy = -param.speed * math.sin(radian) * 10
                                self.bullets.add(bullet)
                            pygame.time.delay(10)
                        self.is_frequen_over = True
                    except TypeError:
                        print('rect out range') # 子弹设定已越界
                    pygame.time.delay(self.period)
        else:
            while True:
                for i in range(0, 100):
                    pygame.time.delay(self.frequen)
                    bullet = AlgoBullet(self.bullet_img, [self.rect.centerx, self.rect.centery], AlgoBullet.INVOLUTE_HELICOID)
                    self.bullets.add(bullet)
                pygame.time.delay(self.period)



