# -*- coding:utf-8 -*-
'''
@author:oldwai
'''
# email: frankandrew@163.com

import pygame
from random import *
import sys

if getattr(sys, 'frozen', False):
    exec_path = sys._MEIPASS.replace('\\', '/') + '/'
else:
    exec_path = './'

class SmallEnemy(pygame.sprite.Sprite):
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(exec_path + "picture/enemy_small.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load(exec_path + "picture/e1_destroy1.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e1_destroy2.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e1_destroy3.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e1_destroy4.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 2
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-5 * self.height, 0)

class MidEnemy(pygame.sprite.Sprite):
    energy = 8
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(exec_path + "picture/enemy_mid.png").convert_alpha()
        self.image_hit = pygame.image.load(exec_path + "picture/enemy_mid_hit.png").convert_alpha()
        self.destroy_images = []
        #e表示enemy
        self.destroy_images.extend([\
            pygame.image.load(exec_path + "picture/e2_destroy1.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e2_destroy2.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e2_destroy3.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e2_destroy4.png").convert_alpha() \
            ])
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.energy = MidEnemy.energy
        self.hit = False
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -self.height)

class BigEnemy(pygame.sprite.Sprite):
    energy = 20
    def __init__(self,bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(exec_path + "picture/enemy_big_1.png").convert_alpha()
        self.image2 = pygame.image.load(exec_path + "picture/enemy_big_2.png").convert_alpha()
        self.image_hit = pygame.image.load(exec_path + "picture/enemy_big_hit.png").convert_alpha()
        self.destroy_images = []
        #e表示enemy
        self.destroy_images.extend([ \
            pygame.image.load(exec_path + "picture/e3_destroy1.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e3_destroy2.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e3_destroy3.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e3_destroy4.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e3_destroy5.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/e3_destroy6.png").convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.hit = False
        self.energy = MidEnemy.energy
        self.mask = pygame.mask.from_surface(self.image1)
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-15 * self.height, -5 * self.height)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def reset(self):
        self.active = True
        self.energy = MidEnemy.energy
        self.rect.left, self.rect.top = \
            randint(0, self.width - self.rect.width), \
            randint(-10 * self.height, -5 * self.height)