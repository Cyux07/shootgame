import pygame
import os, time, math

from src import param
from src.bonus import Bonus
from src.enemy import Enemy
from src.player import Player
from multiprocessing.dummy import Process


class Gate(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (param.SCREEN_WIDTH, param.SCREEN_HEIGHT))
        pygame.display.set_caption('death shooter!')

        self.background = pygame.image.load('../res/background/stg6bg.png').convert() #convert???
        self.gameover_back = pygame.image.load('../res/background/cdbg05a.png')

        self.player = Player('../res/player/pl00.png',(param.SCREEN_WIDTH / 2,param.SCREEN_HEIGHT - 200))
        self.enemys = []
        self.enemys.append(Enemy('../res/enemy/enemy.png', [200, 100]))
        #self.enemy_entrance(0, [200, 100])

        self.bonus = []

        etama2 = pygame.image.load('../res/bullet/etama2.png')
        self.field_img = etama2.subsurface(
                (0, param.field_offset),
                (param.field_len, param.field_len))
        self.field_angle = 0

    def observe(self):
        army_entri_p = Process(target=self.enemy_entrance, args=(0, [200, 200]))
        army_entri_p.start()
        i = 1
        while True:
            self.draw_background()
            #pygame.time.delay(40)
            time.sleep(0.1)
            #playerstatus = self.player

            key_pressed = pygame.key.get_pressed()
            pygame.key.get_repeat()
            if key_pressed[pygame.K_UP]:
                self.player.moveUp()
            if key_pressed[pygame.K_DOWN]:
                self.player.moveDown()
            if key_pressed[pygame.K_LEFT]:
                self.player.moveLeft()
            if key_pressed[pygame.K_RIGHT]:
                self.player.moveRight()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.changeBody(Player.Body.Left)
                    elif event.key == pygame.K_RIGHT:
                        self.player.changeBody(Player.Body.Right)
                    elif event.key == pygame.K_z:
                        self.player.is_attack = True
                    elif event.key == pygame.K_LSHIFT:
                        self.player.speed = param.slow_speed
                        Process(target=self.open_field, args=()).start()
                        print('A.T. Filed 全開！')
                        #self.open_field()
                elif event.type == pygame.KEYUP:
                    if (event.key == pygame.K_LEFT and not key_pressed[pygame.K_RIGHT])\
                            or (event.key == pygame.K_RIGHT and not key_pressed[pygame.K_LEFT]):
                        self.player.changeBody(Player.Body.Center)
                    elif event.key == pygame.K_z:
                        self.player.is_attack = False
                    elif event.key == pygame.K_LSHIFT:
                        #self.close_field()
                        self.player.speed = param.speed
                        Process(target=self.close_field, args=()).start()
                        print('A.T. Filed 關閉！')

            self.attack_check()
            # self.safe_check()

            self.show_player()
            self.show_enemys()
            # print('onDraw()')
            pygame.display.update()

# ||||||||||||||||||||||||一时の事件||||||||||||||||||||||||||||||||||||||||||||||||
    # 入场
    def enemy_entrance(self, index, pos):
        pw = 0
        ph = 0
        self.enemys[index].body_mode = Enemy.Body.Move
        self.enemys[index].img_index = 0
        len = math.sqrt(pos[0] * pos[0] + pos[1] * pos[1])
        speedw = pos[1] / len * param.speed
        speedh = pos[0] / len * param.speed
        while abs(pos[0] - ph) > param.speed or abs(pos[1] - pw) > param.speed:
            time.sleep(0.01)
            #pygame.display.update()
            #self.draw_background()
            #self.show_player()

            if self.enemys[index].img_index < param.emove_frame-1:
                self.enemys[index].img_index += 1
            pw += speedw
            ph += speedh
            self.enemys[index].rect.topleft = [ph, pw]
            #self.screen.blit(self.enemys[index].img, self.enemys[index].rect.topleft)
        # init
        self.enemys[index].rect.topleft = pos
        self.enemys[index].body_mode = Enemy.Body.Center
        self.enemys[index].img_index = 0
        self.enemys[index].shoot()

    def enemy_down(self, enemy):
        enemy.body_mode = Enemy.Body.Down
        enemy.img_index = 0
        for i in range(0, param.edown_frame):
            enemy.img_index = i
            time.sleep(0.02)
            #self.screen.blit(enemy.img, enemy.rect.topleft)
        self.enemys.remove(enemy)
        self.enemy_bonus(enemy.rect.topleft)
        enemy.remove()

    #敌人死后的奖励，多个分数片，一个能量片
    def enemy_bonus(self, pos):
        self.bonus.append(Bonus(Bonus.POWER_M, [pos[0]-20, pos[1]+10]))
        self.bonus.append(Bonus(Bonus.POWER_M, [pos[0]+20, pos[1]+10]))
        self.bonus.append(Bonus(Bonus.POWER_L, [pos[0], pos[1]+12]))

    # TODO 透明渐显渐隐
    def open_field(self):
        self.player.is_shift = True
        print('alpha %d:' %self.field_img.get_alpha())
        copy = self.field_img.copy()
        self.field_img = pygame.transform.scale(self.field_img, (param.field_len + 10, param.field_len + 10))
        self.field_img.set_alpha(0)
        fade_alpha = 0
        for i in range(15, 0, -1):
            time.sleep(0.01)
            pygame.transform.scale(self.field_img, (param.field_len + i, param.field_len + i))
            self.field_img.set_alpha(self.field_img.get_alpha() + 25)
            cup = pygame.Surface(self.field_img.get_rect().size, pygame.SRCALPHA)
            cup.fill((255, 255, 255, fade_alpha))
            fade_alpha += 17
            self.field_img.unlock()
            self.field_img.blit(cup, (0, 0), special_flags=pygame.BLEND_RGB_MULT)
            #self.field_img = cup.copy()
        #pygame.transform.scale(self.field_img, (param.field_len, param.field_len))
        #self.field_img.set_alpha(255)
        self.field_img = copy.copy()

    def close_field(self):
        copy = self.field_img.copy()
        self.field_img = pygame.transform.scale(self.field_img, (param.field_len + 10, param.field_len + 10))
        self.field_img.set_alpha(255)
        for i in range(0, 15):
            time.sleep(0.01)
            pygame.transform.scale(self.field_img, (param.field_len + i, param.field_len + i))
            self.field_img.set_alpha(self.field_img.get_alpha() - 25)
        #pygame.transform.scale(self.field_img, (param.field_len, param.field_len))
        #self.field_img.set_alpha(255)
        self.field_img = copy
        self.player.is_shift = False

# ||||||||||||||||||||||||||||||||||||||||display||||||||||||||||||||||||||||||||||||||
    def draw_background(self):
        self.screen.fill(0)  # rgb?
        self.screen.blit(self.background, (0, 0))

    def show_player(self):
        self.screen.blit(self.player.img, self.player.rect.topleft)

        # bullet ----------------------------------------
        if self.player.is_attack:
            if self.player.frequen % param.FREQUEN == 0:
                self.player.shoot()
                self.player.frequen = 1
            else:
                self.player.frequen += 1

        if len(self.player.bullets) > 0:
            for bullet in self.player.bullets:
                bullet.move()
                if bullet.rect.bottom < 0:
                    self.player.bullets.remove(bullet)
            self.player.bullets.draw(self.screen)

        # shift field------------------------------------
        if self.player.is_shift:
            img = pygame.transform.rotate(self.field_img, self.field_angle)
            img_r = pygame.transform.flip(img, True, False)
            # =pygame.transform.rotate(self.field_img, -self.field_angle)
            self.field_angle = (self.field_angle + 0.2) % 360
            self.screen.blit(img, (self.player.rect.left + (- img.get_width() + param.WIDTH)/2,
                                   self.player.rect.top + (- img.get_height() + param.HEIGHT)/2))
            self.screen.blit(img_r, (self.player.rect.left + (- img.get_width() + param.WIDTH) / 2,
                                   self.player.rect.top + (- img.get_height() + param.HEIGHT)/2))

        # wing plane(ball) ------------------------------
        if self.player.power == 200:
            pass
        elif self.player.power >= 150:
            pass
        elif self.player.power >= 100:
            pass
        elif self.player.power >= 50:
            pass

    def show_enemys(self):
        for enemy in self.enemys:
            self.screen.blit(enemy.img, enemy.rect.topleft)

        # enemy bullet-----------------------------
        for enemy in self.enemys:
            if enemy.is_frequen_over:
                for bullet in enemy.bullets:
                    if bullet.rect.top < 0 or bullet.rect.bottom > param.SCREEN_HEIGHT or bullet.rect.left > param.SCREEN_WIDTH or bullet.rect.right < 0:
                        enemy.bullets.remove(bullet)
                    bullet.move()
            enemy.bullets.draw(self.screen)

    def show_bonus(self):
        for bo in self.bonus:
            if bo.rect.top > param.SCREEN_HEIGHT + 5:
                bo.remove()
            else:
                bo.move()
                self.screen.blit(bo.image, bo.rect.topleft)

# ||||||||||||||||||||||||||||||||||检测|||||||||||||||||||||||||||||||||||||||||||||
    def attack_check(self):
        bullseye = None
        for enemy in self.enemys:
            bullseye = pygame.sprite.spritecollideany(enemy, self.player.bullets)
            if not bullseye == None:
                if pygame.sprite.collide_circle_ratio(0.6)(enemy, bullseye):
                    #self.enemy_down(enemy)
                    #self.enemys.remove(enemy)
                    p = Process(target=self.enemy_down, args=(enemy,), )
                    p.start()
            self.player.bullets.remove(bullseye)
            bullseye = None

    def bonus_check(self):
        catcha = None
        catcha = pygame.sprite.spritecollideany(self.player, self.bonus)
        if not catcha == None:
            if pygame.sprite.collide_circle_ratio(1.5)(self.player, catcha):
                if catcha.type == Bonus.POWER_M:
                    self.player.power += 10
                elif catcha.type == Bonus.POWER_L:
                    self.player.power += 50
                #TODO etc...
                p = Process(target=catcha.suck, args=(self.player.topleft,))
                p.start()

if __name__ == '__main__':
    newgame = Gate()
    newgame.observe()
