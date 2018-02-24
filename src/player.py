import pygame

from src import param
from src.bullet import Bullet
from enum import Enum


class Player(pygame.sprite.Sprite):
    Body = Enum('Body', ('Center', 'Left', 'Right')) #正常飞行，左侧身，右侧身

    #pos=position
    def __init__(self, img, bound):
        pygame.sprite.Sprite.__init__(self)
        player_img = pygame.image.load(img) #'../res/player/pl00.png'
        self.__player = []
        self.__playerL = []
        self.__playerR = []
        for i in range(0, 8): #玩家形象(img list)
            self.__player.append(player_img.subsurface(
                (param.WIDTH * i, 0), (param.WIDTH, param.HEIGHT)))
            self.__playerL.append(player_img.subsurface(
                (param.WIDTH * i, param.HEIGHT), (param.WIDTH, param.HEIGHT)))
            self.__playerR.append(player_img.subsurface(
                (param.WIDTH * i, param.HEIGHT*2), (param.WIDTH, param.HEIGHT)))
        self.img_index = 0 #list序号共8帧
        self.img_mode = Player.Body.Center

        self.bullet = []
        for i in range(0, 3):
            self.bullet.append(pygame.transform.rotate(player_img.subsurface(
                (param.BULLET_WIDTH * i, param.BULLET_OFFSET),
                (param.BULLET_WIDTH, param.BULLET_HEIGHT)), 90))
        self.bullets = pygame.sprite.Group()
        self.frequen = 0 #射击频率
        self.speed = param.speed

        self.rect = self.__player[0].get_rect()
        self.rect.topleft = bound
        self.is_hit = False #是否被攻击
        self.is_attack = False #是否射击

        # 能量共200，每50一个僚机，最多4个
        self.power = 0
        self.wing_img = player_img.subsurface(
            (param.wing_offw, param.wing_offh),
            (param.wing_len, param.wing_len))

        self.__is_shift = False #是否shift

    @property
    def img(self):
        try:
            if self.img_mode == Player.Body.Center:
                return self.__player[self.img_index]
            elif self.img_mode == Player.Body.Left:
                return self.__playerL[self.img_index]
            elif self.img_mode == Player.Body.Right:
                return self.__playerR[self.img_index]
        finally:
            self.img_index = (self.img_index + 1) % param.frame

    @property
    def is_shift(self):
        return self.__is_shift

    @is_shift.setter
    def is_shift(self, shi):
        self.__is_shift = shi
        if self.__is_shift:
            self.speed = param.slow_speed
        else:
            self.speed = param.speed

    def shoot(self):
        bulletL = Bullet(self.bullet[0], [self.rect.left, self.rect.top])
        bulletR = Bullet(self.bullet[0], [self.rect.right, self.rect.top])
        self.bullets.add(bulletL)
        self.bullets.add(bulletR)

        # TODO wing ball bullet---------------------------------
        if self.power == 200:
            pass
        elif self.power >= 150:
            pass
        elif self.power >= 100:
            pass
        elif self.power >= 50:
            pass

    def moveUp(self):
        if self.rect.top <= 0:
            self.rect.top =0
        else:
            self.rect.top -= self.speed

    def moveDown(self):
        if self.rect.top >= param.SCREEN_HEIGHT - param.HEIGHT:
            self.rect.top = param.SCREEN_HEIGHT - param.HEIGHT
        else:
            self.rect.top += self.speed

    def moveLeft(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def moveRight(self):
        if self.rect.left >= param.SCREEN_WIDTH - param.WIDTH:
            self.rect.left = param.SCREEN_WIDTH - param.WIDTH
        else:
            self.rect.left += self.speed

    def changeBody(self, mode):
        if isinstance(mode, Player.Body):
            self.img_mode = mode
