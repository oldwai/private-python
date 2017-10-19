# -*- coding:utf-8 -*-
'''
@author:oldwai
'''
# email: frankandrew@163.com

import sys
import traceback
from random import *

import pygame
from pygame.locals import *

import enemy, supply
import bullet
import myplane

if getattr(sys, 'frozen', False):
    exec_path = sys._MEIPASS.replace('\\', '/') + '/'
else:
    exec_path = './'

pygame.init()

pygame.mixer.init()

bg_size = width, height = 480,800
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption(" Mega Plane")

background = pygame.image.load(exec_path + "picture/background.png").convert_alpha()
#飞机血槽变量定义
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

#载入游戏音乐
pygame.mixer.music.load(exec_path + "sound/game_music.wav")
pygame.mixer.music.set_volume(0.2)
bullet_sound = pygame.mixer.Sound(exec_path + "sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound(exec_path + "sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound(exec_path + "sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound(exec_path + "sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound(exec_path + "sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound(exec_path + "sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_flying_sound = pygame.mixer.Sound(exec_path + "sound/enemy3_flying.wav")
enemy3_flying_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound(exec_path + "sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound(exec_path + "sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound(exec_path + "sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.2)
me_down_sound = pygame.mixer.Sound(exec_path + "sound/me_down.wav")
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

def increase_speed(target, inc_num = 1):
    for each in target:
        each.speed += inc_num


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

    #每30秒增加补给包
    bullet_supply = supply.BulletSupply(bg_size)
    bomb_supply = supply.BombSupply(bg_size)
    SUPPLY_TIME = USEREVENT
    pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)

    #超级子弹定时器
    super_bullet_time = USEREVENT + 1

    #无敌计时器
    INVINCIBLE_TIME = USEREVENT + 2

    #游戏结束时不绘制

    #标记是否使用超级子弹
    is_super_bullet = False

    #生成普通子弹
    normal_bullet = []
    normal_bullet_index = 0
    normal_bullet_num = 5
    for i in range(normal_bullet_num):
        normal_bullet.append(bullet.NormalBullet(me.rect.midtop))
    #生成超级子弹
    super_bullet = []
    super_bullet_index = 0
    super_bullet_num = 8
    for i in range(super_bullet_num // 2):
        super_bullet.append(bullet.SuperBullet((me.rect.centerx - 33, me.rect.centery )))
        super_bullet.append(bullet.SuperBullet((me.rect.centerx + 30, me.rect.centery )))

    #中弹图片索引
    e1_destroy_index = 0
    e2_destroy_index = 0
    e3_destroy_index = 0
    me_destroy_index = 0

    #统计得分
    score = 0
    score_font = pygame.font.Font(exec_path + "font/font.ttf", 36)
    prompt_font = pygame.font.Font(exec_path + "font/prompt.TTF", 21)
    #标记是否暂停游戏
    paused = False
    paused_nor_image = pygame.image.load(exec_path + "picture/paused_nor_image.png").convert_alpha()
    paused_pressed_image = pygame.image.load(exec_path + "picture/paused_pressed_image.png").convert_alpha()
    resume_nor_image = pygame.image.load(exec_path + "picture/resume_nor_image.png").convert_alpha()
    resume_pressed_image = pygame.image.load(exec_path + "picture/resume_pressed_image.png").convert_alpha()
    paused_rect = paused_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_default_image = paused_nor_image


    #生命数量
    life_image = pygame.image.load(exec_path + "picture/life.png").convert_alpha()
    life_image_rect = life_image.get_rect()
    life_num = 1

    #设置全屏炸弹
    bomb_image = pygame.image.load(exec_path + "picture/bomb.png").convert_alpha()
    bomb_image_rect = bomb_image.get_rect()
    bomb_font = pygame.font.Font(exec_path + "font/font.ttf", 48)
    bomb_num = 3

    #游戏结束画面
    #gameover_font = pygame.font.Font(exec_path + "font/font.TFF", 48)
    again_image = pygame.image.load(exec_path + "picture/again_image.png").convert_alpha()
    again_image_rect = again_image.get_rect()
    gameover_image = pygame.image.load(exec_path + "picture/gameover_image.png").convert_alpha()
    gameover_image_rect = gameover_image.get_rect()

    #设置游戏难度级别
    level =1

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
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pygame.time.set_timer(SUPPLY_TIME, 30 * 1000)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_default_image = resume_pressed_image

                    else:
                        paused_default_image = paused_pressed_image
                else:
                    if paused:
                        paused_default_image = resume_nor_image
                    else:
                        paused_default_image = paused_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.active = False
            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if choice([True, False]):
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == super_bullet_time:
                is_super_bullet = False
                pygame.time.set_timer(super_bullet_time, 0)

            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)


        #根据用户的得分增加难度
        if level == 1 and score > 10000:
            level = 2
            upgrade_sound.play()
            #增加3个小飞机、2个中飞机、1个大型飞机
            add_small_enemies(small_enemies, enemies, 3)
            add_mid_enemies(mid_enemies, enemies, 2)
            add_big_enemies(big_enemies, enemies, 1)
            #提升小型敌机的速度
            increase_speed(small_enemies)

        if level == 2 and score > 30000:
            level = 3
            upgrade_sound.play()
            #增加5个小飞机、3个中飞机、2个大型飞机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小/中型敌机的速度
            increase_speed(small_enemies)
            increase_speed(mid_enemies)

        if level == 3 and score > 60000:
            level = 4
            upgrade_sound.play()
            #增加5个小飞机、3个中飞机、2个大型飞机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型敌机的速度
            increase_speed(small_enemies)
            increase_speed(mid_enemies)

        if level == 4 and score > 1000000:
            level = 5
            upgrade_sound.play()
            #增加5个小飞机、3个中飞机、2个大型飞机
            add_small_enemies(small_enemies, enemies, 5)
            add_mid_enemies(mid_enemies, enemies, 3)
            add_big_enemies(big_enemies, enemies, 2)
            #提升小型敌机的速度
            increase_speed(small_enemies)
            increase_speed(mid_enemies)

        screen.blit(background, (0,0))


        if life_num and not paused:
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

            #绘制全屏炸弹补给并检测是否获得
            if bomb_supply.active:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, me):
                    get_bomb_sound.play()
                    if bomb_num < 3:
                        bomb_num += 1
                    bomb_supply.active = False

            #绘制超级子弹补给并检测是否获得
            if bullet_supply.active:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, me):
                    get_bullet_sound.play()
                    #发射超级子弹
                    is_super_bullet = True
                    pygame.time.set_timer(super_bullet_time, 18 * 1000)
                    bullet_supply.active = False


            #发射子弹
            if not (delay % 10):
                #播放子弹声音
                #暂时缺少声音文件，部分音效未能加载。后续优化

                #判断是发射超级子弹还是普通子弹
                if is_super_bullet:
                    bullets = super_bullet
                    bullets[super_bullet_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[super_bullet_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    super_bullet_index = (super_bullet_index + 2) % super_bullet_num

                else:
                    bullets = normal_bullet
                    bullets[normal_bullet_index].reset(me.rect.midtop)
                    normal_bullet_index = (normal_bullet_index + 1) % normal_bullet_num

            #检测子弹是否击中
            for b in bullets:
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
                    #绘制血条
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

                    #大型敌机的出现。即将出现在画面中时播放音效
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
                            score += 10000
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
                            score += 6000
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
                            score += 1000
                            each.reset()

            #检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False,pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                     e.active = False


            #绘制我方飞机
            if me.active:
                if switch_image:
                    screen.blit(me.image1, me.rect)
                else:
                    screen.blit(me.image2, me.rect)
            else:
                #毁灭
                me_down_sound.play()
                if not(delay % 3):
                    screen.blit(me.destroy_images[me_destroy_index], each.rect)
                    me_destroy_index = (me_destroy_index + 1) % 4
                    if me_destroy_index == 0:
                        life_num -= 1
                        me.reset()
                        pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)
            #绘制炸弹
            bomb_text = bomb_font.render(" x %d" % bomb_num, True, RED)
            bomb_text_rect = bomb_text.get_rect()
            screen.blit(bomb_image, (10, height - 10 - bomb_image_rect.height))
            screen.blit(bomb_text, (20 + bomb_image_rect.width, height - 5 - bomb_text_rect.height))

            #绘制剩余生命数量：
            if life_num:
                for i in range(life_num):
                    screen.blit(life_image, \
                                (width-10-(i+1)*life_image_rect.width, \
                                 height-10-life_image_rect.height))
        elif paused and life_num:
            prompt = prompt_font.render("Continue pressing the pause button, exit please close" , True, BLACK)
            screen.blit(prompt, (10 , height//2))
        #绘制游戏结束画面
        elif life_num == 0:
            #音乐停止
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            pygame.time.set_timer(SUPPLY_TIME, 0)

            again_image_rect.left, again_image_rect.top =(width//2 - 40, height//2)
            screen.blit(again_image, again_image_rect )

            gameover_image_rect.left, gameover_image_rect.top =(width//2 - 40, height//2 + 50)
            screen.blit(gameover_image, gameover_image_rect)

            #检测用户的鼠标操作
            #如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                #获取鼠标坐标
                pos = pygame.mouse.get_pos()
                #如果用户点击“重新开始”
                if again_image_rect.left < pos[0] < again_image_rect.right and \
                    again_image_rect.top < pos[1] < again_image_rect.bottom:
                    #调用main()函数，重新开始游戏
                    main()
                #如果用户点击结束游戏
                elif gameover_image_rect.left < pos[0] < gameover_image_rect.right and \
                    gameover_image_rect.top < pos[1] < gameover_image_rect.bottom:
                    #退出游戏
                    pygame.quit()
                    sys.exit()




        #得分
        if life_num:
            score_text = score_font.render("Score : %s" % str(score), True, RED)
            screen.blit(score_text, (10,5))
        else:
            finally_score_text = score_font.render("Your Score : %s" % str(score), True, RED)
            screen.blit(finally_score_text, (80,again_image_rect.top -80))

        screen.blit(paused_default_image, paused_rect)

        #切换图片,使用户感觉飞机在动
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
