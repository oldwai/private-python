# -*- coding:utf-8 -*-
'''
@author:oldwai
'''
# email: frankandrew@163.com

import pygame
import sys

if getattr(sys, 'frozen', False):
    exec_path = sys._MEIPASS.replace('\\', '/') + '/'
else:
    exec_path = './'

class NormalBullet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(exec_path + "picture/normal_bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = position
        self.speed = 12
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

class SuperBullet(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(exec_path + "picture/super_bullet.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left , self.rect.top = position
        self.speed = 14
        self.active = True
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True