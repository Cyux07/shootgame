import threading

import pygame
import math
'''

from src.Gate import Gate
#from src.test2 import t2


class t1():
    t1s = 233
    def t1f(self):
        print(t1.t1s + t2.t2s)

s = pygame.sprite.Group()
print(len(s))
threading'''

a = 5
b = 7
c = 2.2
for t in range(0, 20):
    theta = 360*t*10
    x = (a-b)*math.cos(theta) + c*math.cos((a/b - 1)*theta)
    y = (a - b)*math.sin(theta)-c*math.sin((a/b-1)*theta)
    print('(%f, %f)' %(x, y))
