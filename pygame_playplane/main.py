# -*- coding:utf-8 -*-
'''
@author:oldwai
'''
# email: frankandrew@163.com

import pygame
import sys
import traceback
from pygame.locals import *
sys.path.append(r'E:\test-project\pygame_playplane')
import myplane
import enemy
import bullet

pygame.init()

pygame.mixer.init()

bg_size = width, height = 480,800
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("play !!!!")

background = pygame.image.load("picture/background.png").convert_alpha()
#飞机血槽变量定义
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

#载入游戏音乐
pygame.mixer.music.load("sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_flying_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_flying_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

def add_small_enemies(group1, group2, plane_num):
    for i in range(plane_num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)

def add_mid_enemies(group1, group2, plane_num):
    for i in range(plane_num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)

def add_big_enemies(group1, group2, plane_num):
    for i in range(plane_num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)



def main():
    pygame.mixer.music.play(-1)

    #生成我方飞机
    me = myplane.MyPlane(bg_size)

    #生成敌方飞机
    enemies = pygame.sprite.Group()

    #生成敌方小型飞机
    small_enemies = pygame.sprite.Group()
    add_small_enemies(small_enemies, enemies, 15)

    #生成敌方中型飞机
    mid_enemies = pygame.sprite.Group()
    add_mid_enemies(mid_enemies, enemies, 4)

    #生成敌方小型飞机
    big_enemies = pygame.sprite.Group()
    add_big_enemies(big_enemies, enemies, 2)

    #生成普通子弹
    normal_bullet = []
    normal_bullet_index = 0
    normal_bullet_num = 5
    for i in range(normal_bullet_num):
        normal_bullet.append(bullet.NormalBullet(me.rect.midtop))


    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #生命数量
    #life_image = pygame.image.load("picture/")
    life_num = 1

    #游戏结束画面
    #gameover_font = pygame.font.Font("font/font.TFF", 48)
    again_image = pygame.image.load("picture/again_image.png").convert_alpha()
    again_image_rect = again_image.get_rect()
    gameover_image = pygame.image.load("picture/gameover_image.png").convert_alpha()
    gameover_image_rect = gameover_image.get_rect()

    #用户切换图片
    switch_image = True
    #用于延时
    delay = 100
    clock = pygame.time.Clock()


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        #检测用户的键盘操作,get_pressed()检测频繁操作的
        key_pressed = pygame.key.get_pressed()

        if key_pressed[K_w] or key_pressed[K_UP]:
            me.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.move_right()


        screen.blit(background, (0,0))

        #发射子弹
        if not (delay % 10):
            normal_bullet[normal_bullet_index].reset(me.rect.midtop)
            normal_bullet_index = (normal_bullet_index + 1) % normal_bullet_num

        #检测子弹是否击中
        for b in normal_bullet:
            if b.active:
                b.move()
                screen.blit(b.image, b.rect)
                enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    b.active = False
                    for e in enemy_hit:
                        if e in mid_enemies or e in big_enemies:
                            e.hit = True
                            e.energy -= 1
                            if e.energy == 0:
                                e.active = False
                        else:
                            e.active = False


        #绘制敌方大型飞机
        for each in big_enemies:
            if each.active:
                each.move()
                if each.hit:
                    #绘制飞机被打中的特效
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False
                else:
                    if switch_image:
                        screen.blit(each.image1, each.rect)
                    else:
                        screen.blit(each.image2, each.rect)
                #绘制血槽
                pygame.draw.line(screen, BLACK,\
                                 (each.rect.left, each.rect.top -5), \
                                 (each.rect.right, each.rect.top -5), \
                                 2)
                #当生命大于20%显示绿色，否则为红色
                energy_remain = each.energy / enemy.BigEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen, energy_color,\
                                 (each.rect.left, each.rect.top -5), \
                                 (each.rect.left + each.rect.width * energy_remain, each.rect.top -5), \
                                 2)

                #即将出现在画面中，播放音效
                if each.rect.bottom == -50:
                    #-1表示循环播放
                    enemy3_flying_sound.play(-1)
            else:
                 #毁灭
                if not(delay % 3):
                    screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                    e3_destroy_index = (e3_destroy_index + 1) % 6
                    if e3_destroy_index == 0:
                        enemy3_flying_sound.stop()
                        each.reset()

        #绘制中型敌机
        for each in mid_enemies:
            if each.active:
                each.move()
                if each.hit:
                    #绘制飞机被打中的特效
                    screen.blit(each.image_hit, each.rect)
                    each.hit = False
                else:
                    screen.blit(each.image, each.rect)
                #绘制血槽
                pygame.draw.line(screen, BLACK,\
                                 (each.rect.left, each.rect.top -5), \
                                 (each.rect.right, each.rect.top -5), \
                                 2)
                #当生命大于20%显示绿色，否则为红色
                energy_remain = each.energy / enemy.MidEnemy.energy
                if energy_remain > 0.2:
                    energy_color = GREEN
                else:
                    energy_color = RED
                pygame.draw.line(screen, energy_color,\
                                 (each.rect.left, each.rect.top -5), \
                                 (each.rect.left + each.rect.width * energy_remain, each.rect.top -5), \
                                 2)
            else:
                #毁灭
                if not(delay % 3):
                    screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                    e2_destroy_index = (e2_destroy_index + 1) % 4
                    if e3_destroy_index == 0:
                        each.reset()

        #绘制小型敌机
        for each in small_enemies:
            if each.active:
                each.move()
                screen.blit(each.image, each.rect)
            else:
                 #毁灭
                if not(delay % 3):
                    screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 4
                    if e1_destroy_index == 0:
                        each.reset()

        #检测我方飞机是否被撞
        enemies_down = pygame.sprite.spritecollide(me, enemies, False,pygame.sprite.collide_mask)
        if enemies_down:
            me.active = False
            for e in enemies_down:
                e.active = False
                life_num -= 1

        #绘制我方飞机

        if me.active:
            if switch_image:
                screen.blit(me.image1, me.rect)
            else:
                screen.blit(me.image2, me.rect)
        else:
             #毁灭
            if not(delay % 3):
                screen.blit(me.destroy_images[me_destroy_index], each.rect)
                me_destroy_index = (me_destroy_index + 1) % 4
                if me_destroy_index == 0:
                    #running = False
                    screen.blit(gameover_image, gameover_image_rect)
                    #背景音乐停止
                    pygame.mixer.music.stop()
                    #停止全部音效
                    pygame.mixer.stop()
                    #
                    #gameover_image_rect.left, gameover_image_rect.top = \
                    #    (width - gameover_image_rect.width) // 2, \
                    screen.blit(gameover_image, gameover_image_rect)
                    if pygame.mouse.get_pressed()[0]:
                        #获取鼠标坐标
                        pos = pygame.mouse.get_pos()
                        #如果用户点击 重新开始
                        if gameover_image_rect < pos[0] < gameover_image_rect.right and \
                            gameover_image_rect.top < pos[1] < gameover_image_rect.bottom:
                            #退出游戏
                            pygame.quit()
                            sys.exit()
                    #each.reset()



        #切换图片
        if not(delay % 5):
            switch_image = not switch_image

        delay -= 1
        if not delay:
            delay = 100

        pygame.display.flip()

        clock.tick(60)


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()
