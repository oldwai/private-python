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

class MyPlane(pygame.sprite.Sprite):
    def __init__(self, bg_size):
        pygame.sprite.Sprite.__init__(self)

        self.image1 = pygame.image.load(exec_path + "picture/myplane1.png").convert_alpha()
        self.image2 = pygame.image.load(exec_path + "picture/myplane2.png").convert_alpha()
        self.destroy_images = []
        self.destroy_images.extend([\
            pygame.image.load(exec_path + "picture/myplane_destroy1.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/myplane_destroy2.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/myplane_destroy3.png").convert_alpha(), \
            pygame.image.load(exec_path + "picture/myplane_destroy4.png").convert_alpha() \
            ])
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2,\
            self.height - self.rect.height - 60
        #移动的速度为10像素
        self.speed = 10
        self.active = True
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image1)

    def move_up(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def move_down(self):
        if self.rect.bottom < self.height - 60:
            self.rect.bottom += self.speed
        else:
            self.rect.bottom = self.height - 60

    def move_left(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def move_right(self):
        if self.rect.right < self.width:
            self.rect.right += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = \
            (self.width - self.rect.width) // 2,\
            self.height - self.rect.height - 60
        self.active = True
        self.invincible = True

