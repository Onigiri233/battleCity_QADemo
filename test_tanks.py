# -*- encoding: utf-8 -*-
"""
@File    : test_tanks.py
@Time    : 2020/3/21 21:20
@Author  : Fantuan
@Software: PyCharm
"""
import math
import time

import pygame

import tanks
import Tkinter as tk
import os, threading, random

from a_star import AStar


def run(nr_of_players=1):
    tanks.game = tanks.Game()
    tanks.castle = tanks.Castle()
    tanks.play_sounds = False
    tanks.game.stage = 0
    tanks.game.nr_of_players = nr_of_players
    tanks.game.nextLevel()



def run_gui_single():
    th = threading.Thread(target=run, args=(1,))
    th.setDaemon(True)  # 守护线程
    th.start()
    time.sleep(1)
    route_info_gui()
    time.sleep(1)
    player_move_gui()


def run_gui_double():
    th = threading.Thread(target=run, args=(2,))
    th.setDaemon(True)  # 守护线程
    th.start()
    time.sleep(1)
    route_info_gui()
    time.sleep(1)
    player_move_gui()


dirction = ("向上", "向右", "向下", "向左")
tank_type = ("普通", "三倍移速", "超级子弹", "四倍血量")
bullet_owner = ("我方", "敌方")
bonus_type = ("手雷", "无敌", "保护", "星星", "生命", "冻结")
tile_type = ("空", "砖", "铁", "水", "草", "冰")


def get_info():
    strbuf = ""
    for player in tanks.players:
        strbuf += "玩家位置%s，移动方向：%s\n" % ((player.rect[0], player.rect[1]), dirction[player.direction],)

    for enemy in tanks.enemies:
        strbuf += "敌人位置%s，类型%s，移动方向：%s，移动速度：%s,移动路径%s\n" % (
            (enemy.rect[0], enemy.rect[1]), tank_type[enemy.type], dirction[enemy.direction], enemy.speed,
            (enemy.path[0], enemy.path[1]),)
    for bullet in tanks.bullets:
        strbuf += "子弹位置%s，归属%s，移动方向：%s，移动速度：%s\n" % (
            (bullet.rect[0], bullet.rect[1]), bullet_owner[bullet.owner], dirction[bullet.direction], bullet.speed,)
    for bonus in tanks.bonuses:
        strbuf += "BUFF类型%s\n" % (bonus_type[bonus.bonus],)
    strbuf += "当前关卡%s\n" % (tanks.game.stage)
    level = tanks.Level(tanks.game.stage)
    # print (level.obstacle_rects)
    # print (level.mapr)
    for tile in level.mapr:
        for player in tanks.players:
            # pygame.Rect(position[0] - 8 , position[1] + 11, 8, 6).colliderect(castle.rect)
            # print ("%s-%s")%(tile.topleft,(player.rect[0],player.rect[1]))
            if tile.x == player.rect[0] or tile.y == player.rect[1]:
                print("[%s,%s]") % (tile.topleft, tile_type[tile.type])

    print strbuf
    return strbuf


def get_output_doc():
    print (tanks.game.stage)
    for player in tanks.players:
        print ("消灭%s，得分%s" % (str(player.trophies), str(player.score)))


def player_fire():
    maze = [[0] * 26 for i in range(26)]

    while not tanks.game.game_over:
        for tile in tanks.game.level.obstacle_rects:
            maze[tile.y / 16][tile.x / 16] = 1

        for player in tanks.players:
            available_positions = player.available_pos
            available_fire = player.available_fire
            available_pos = []
            available_dire = []
            for i in range(len(available_positions)):
                if len(available_positions[i]):
                    available_dire.append(i)
                    available_pos.append(available_positions[i][0])

            for bullet in tanks.bullets:
                for i in range(len(available_fire)):
                    if bullet.owner == 1 and bullet.direction == (i + 3) % 3 and bullet.rect.collidelist(
                            available_fire[i]) != -1:
                        if player.state == player.STATE_ALIVE:
                            player.rotate(i)
                            player.fire()
                            # print ("向%s方向拦截") % (i)
                    elif bullet.owner == 1 and bullet.rect.colliderect(player.rect):
                        # print ("躲避")
                        player.move(available_pos[0])

            for enemy in tanks.enemies:

                for i in range(len(available_fire)):
                    if enemy.rect.collidelist(available_fire[i]) != -1:
                        if player.state == player.STATE_ALIVE:
                            player.rotate(i)
                            player.fire()
                        # print ("自由开火方向%s") % (i)


def player_move():
    maze = [[0] * 26 for i in range(26)]

    while not tanks.game.game_over:
        for tile in tanks.game.level.obstacle_rects:
            maze[tile.y / 16][tile.x / 16] = 1

        for player in tanks.players:
            # for i in range(len(tanks.players)):
            #     player = tanks.players[i]
            if player.state == player.STATE_ALIVE:
                available_positions = player.available_pos
                available_fire = player.available_fire
                available_pos = []
                available_dire = []
                player.move_path = []
                for i in range(len(available_positions)):
                    if len(available_positions[i]):
                        available_dire.append(i)
                        available_pos.append(available_positions[i][0])
                if available_dire and player.direction in available_dire:
                    # print available_dire
                    player.move(player.direction)
                else:
                    # print available_dire
                    player.move(player.direction)
                    player.move(random.randint(0,3))

                #
                for bullet in tanks.bullets:
                    for i in range(len(available_fire)):
                        if bullet.owner == 1 and bullet.rect.colliderect(player.rect):
                            player.move(available_dire[0])
                # if player.move_path:
                #     for enemy in tanks.enemies:
                #         if enemy.rect.y / 16 > 20:
                #             # print ("优先级更高的敌人(%s,%s)-->(%s,%s)") % (
                #             #     player.rect.x / 16, player.rect.y / 16, enemy.rect.x / 16, enemy.rect.y / 16,)
                #             player.move_path = AStar(maze, (player.rect.x / 16, player.rect.y / 16),
                #                                      (enemy.rect.x / 16, enemy.rect.y / 16))
                #
                # else:
                #     if tanks.enemies:
                #         # print ("随机找一个敌人(%s,%s)-->(%s,%s)") % (
                #         #     player.rect.left / 16, player.rect.y / 16, tanks.enemies[0].rect.x / 16,
                #         #     tanks.enemies[0].rect.y / 16,)
                #         player.move_path = AStar(maze, (player.rect.x / 16, player.rect.y / 16),
                #                                  (tanks.enemies[0].rect.x / 16, tanks.enemies[0].rect.y / 16))
                #
                # if player.move_path:
                #     surface_plan = pygame.Surface((16 * 2, 16 * 2)).convert_alpha()
                #     surface_plan.fill((0, 125, 0, 10))
                #     for x, y in player.move_path:
                #         tanks.screen.blit(surface_plan, pygame.Rect([x * 16, y * 16], [x + 16, y + 16]))
                #     # print player.move_path
                #     change_plan = False
                #     while (len(player.move_path)>0 and (x, y == player.rect.x / 16, player.rect.y / 16 or change_plan == False)):
                #         (x, y) = player.move_path[-1]
                #         player.move_path = player.move_path[:-1]
                #         # print x, y, player.move_path
                #         #     dirction = ("向上", "向右", "向下", "向左")
                #         dir = -1
                #         if y * 16 > player.rect.y:
                #             # print "DOWN"
                #             dir = 2
                #         elif y * 16 < player.rect.y:
                #             # print "UP"
                #             dir = 0
                #         elif x * 16 > player.rect.x:
                #             # print "right"
                #             dir = 1
                #         elif x * 16 < player.rect.x:
                #             # print "left"
                #             dir = 3
                #         player.pressed[dir] = True
                #         for enemy in tanks.enemies:
                #             if enemy.rect.y / 16 > 20:
                #                 # print ("优先级更高的敌人(%s,%s)-->(%s,%s)") % (
                #                 #     player.rect.x / 16, player.rect.y / 16, enemy.rect.x / 16, enemy.rect.y / 16,)
                #                 # player.move_path = AStar(maze, (player.rect.x / 16, player.rect.y / 16),
                #                 #                          (enemy.rect.x / 16, enemy.rect.y / 16))
                #                 change_plan = True
                #         player.pressed = [False] * 4




def player_move_gui():
    th = threading.Thread(target=player_move)
    th.setDaemon(True)  # 守护线程
    th.start()
    th2 = threading.Thread(target=player_fire)
    th2.setDaemon(True)  # 守护线程
    th2.start()


def route_info():
    while not tanks.game.game_over:
        surface_route = pygame.Surface((16 * 2, 16 * 2)).convert_alpha()
        surface_route.fill((255, 255, 0, 10))
        surface_fire = pygame.Surface((3 * 2, 3 * 2)).convert_alpha()
        surface_fire.fill((255, 255, 10, 10))

        for player in tanks.players:
            all_directions = [player.DIR_UP, player.DIR_RIGHT, player.DIR_DOWN, player.DIR_LEFT]
            x = int(round(player.rect.left / 16))
            y = int(round(player.rect.top / 16))
            player.available_pos = [[], [], [], []]
            player.available_fire = [[pygame.Rect(player.rect[0] + 11, player.rect[1] - 8, 6, 8)],
                                     [pygame.Rect(player.rect[0] + 26, player.rect[1] + 11, 8, 6)],
                                     [pygame.Rect(player.rect[0] + 11, player.rect[1] + 26, 6, 8)],
                                     [pygame.Rect(player.rect[0] - 8, player.rect[1] + 11, 8, 6)]]

            for direction in all_directions:
                pos_isOut = False
                fire_isHit = False
                new_pos_rect = player.rect
                if direction == player.DIR_UP and y > 1:
                    while (pos_isOut == False):
                        new_pos_rect = new_pos_rect.move(0, -8)
                        if new_pos_rect.top < 0:
                            pos_isOut = True
                        elif new_pos_rect.collidelist(player.level.obstacle_rects) == -1:
                            player.available_pos[0].append(new_pos_rect)
                        else:
                            pos_isOut = True
                    new_fire_rect = player.available_fire[0][0]
                    while (fire_isHit == False):
                        if new_fire_rect.top < 0:
                            fire_isHit = True
                        elif new_fire_rect.collidelist(player.level.obstacle_rects) == -1:
                            player.available_fire[0].append(new_fire_rect)
                            new_fire_rect = new_fire_rect.move(0, -8)
                        else:
                            fire_isHit = True
                elif direction == player.DIR_RIGHT and x < 24:

                    while (pos_isOut == False):
                        new_pos_rect = new_pos_rect.move(8, 0)
                        if new_pos_rect.left > (416 - 26):
                            pos_isOut = True
                        elif new_pos_rect.collidelist(player.level.obstacle_rects) == -1:
                            player.available_pos[1].append(new_pos_rect)
                        else:
                            pos_isOut = True
                    new_fire_rect = player.available_fire[1][0]
                    while (fire_isHit == False):
                        if new_fire_rect.left > (416 - 26):
                            fire_isHit = True
                        elif new_fire_rect.collidelist(player.level.obstacle_rects) == -1:
                            player.available_fire[1].append(new_fire_rect)
                            new_fire_rect = new_fire_rect.move(8, 0)

                        else:
                            fire_isHit = True
                elif direction == player.DIR_DOWN and y < 24:

                    while (pos_isOut == False):
                        new_pos_rect = new_pos_rect.move(0, 8)
                        if new_pos_rect.top > (416 - 26):
                            pos_isOut = True
                        elif new_pos_rect.collidelist(player.level.obstacle_rects) == -1:
                            player.available_pos[2].append(new_pos_rect)
                        else:
                            pos_isOut = True
                    new_fire_rect = player.available_fire[2][0]
                    while (fire_isHit == False):

                        if new_fire_rect.top > (416 - 26):
                            fire_isHit = True
                        elif new_fire_rect.collidelist(player.level.obstacle_rects) == -1:
                            player.available_fire[2].append(new_fire_rect)
                            new_fire_rect = new_fire_rect.move(0, 8)

                        else:
                            fire_isHit = True
                elif direction == player.DIR_LEFT and x > 1:
                    while (pos_isOut == False):
                        new_pos_rect = new_pos_rect.move(-8, 0)
                        if new_pos_rect.left < 0:
                            pos_isOut = True
                        elif new_pos_rect.collidelist(player.level.obstacle_rects) == -1:
                            player.available_pos[3].append(new_pos_rect)
                        else:
                            pos_isOut = True
                    new_fire_rect = player.available_fire[3][0]

                    while (fire_isHit == False):
                        if new_fire_rect.left < 0:
                            fire_isHit = True
                        elif new_fire_rect.collidelist(player.level.obstacle_rects) == -1:
                            player.available_fire[3].append(new_fire_rect)
                            new_fire_rect = new_fire_rect.move(-8, 0)
                        else:
                            fire_isHit = True
            for pos_list in player.available_pos:
                for pos in pos_list:
                    tanks.screen.blit(surface_route, pos.topleft)
            for fire_list in player.available_fire:
                for fire in fire_list:
                    tanks.screen.blit(surface_fire, fire.topleft)
            # 移动
            # x = player.rect.left
            # y = player.rect.top
            # pixels = player.nearest(random.randint(1, 12) * 32, 32)  + 3
            # if new_direction == player.DIR_UP:
            #     for px in range(0, pixels, player.speed):
            #         positions.append([x, y - px])
            # elif new_direction == player.DIR_RIGHT:
            #     for px in range(0, pixels, player.speed):
            #         positions.append([x + px, y])
            # elif new_direction == player.DIR_DOWN:
            #     for px in range(0, pixels, player.speed):
            #         positions.append([x, y + px])
            # elif new_direction == player.DIR_LEFT:
            #     for px in range(0, pixels, player.speed):
            #         positions.append([x - px, y])

            # pixels = player.nearest(random.randint(1, 12) * 32, 32) + 3
            # # new_position=[x - px, y]
            # for px in range(0, pixels, player.speed):
            #     new_rect = pygame.Rect(new_position, [26, 26])
            #
            #     if new_rect.collidelist(tanks.game.level.obstacle_rects) != -1:

        # if cmp(rects, tanks.game.level.obstacle_rects) == 0:
        #     # 无变化
        #     pass
        # else:
        #     # 改变
        #     print ("%s\n") % ("地图改变")
        #     rects = tanks.game.level.obstacle_rects
        #
        # for tile in rects:
        #     tanks.screen.blit(surface_route, tile.topleft)


def route_info_gui():
    th = threading.Thread(target=route_info)
    th.setDaemon(True)  # 守护线程
    th.start()


# 作弊能力-直接下一关
def cheatNextLevel():
    tanks.game.finishLevel()


# 作弊能力-无限火力（？）
def cheatSuperPowers():
    for player in tanks.players:
        player.superpowers = 3
        player.max_active_bullets = 2
        player.lives = 30


# 作弊能力-无敌防御
def cheatSuperDefense():
    tanks.game.level.buildFortress(tanks.game.level.TILE_STEEL)
    for player in tanks.players:
        tanks.game.shieldPlayer(player, True, 100000)


def gui():
    root = tk.Tk()
    root.geometry('640x320')
    root.title('自动化测试')

    lb1 = tk.Label(root, text='自动化测试')
    lb1.pack()

    btn_run1 = tk.Button(root, text='单人模式', command=run_gui_single)
    btn_run1.place(relx=0.05, rely=0.1, relwidth=0.3, relheight=0.15)
    btn_run2 = tk.Button(root, text='双人模式', command=run_gui_double)
    btn_run2.place(relx=0.05, rely=0.3, relwidth=0.3, relheight=0.15)

    btn_testrun = tk.Button(root, text='自动化开始', command=player_move_gui)
    btn_testrun.place(relx=0.05, rely=0.5, relwidth=0.3, relheight=0.15)

    btn3 = tk.Button(root, text='显示路径', command=route_info_gui)
    btn3.place(relx=0.5, rely=0.1, relwidth=0.2, relheight=0.1)

    def get_info_gui():
        strbuf = get_info()
        info.set(strbuf)

    btn4 = tk.Button(root, text='显示信息', command=get_info_gui)
    btn4.place(relx=0.5, rely=0.3, relwidth=0.2, relheight=0.1)

    btn5 = tk.Button(root, text='结果分析', command=get_output_doc)
    btn5.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.1)

    btn6 = tk.Button(root, text='下一关', command=cheatNextLevel)
    btn6.place(relx=0.75, rely=0.1, relwidth=0.2, relheight=0.1)
    btn7 = tk.Button(root, text='无限火力', command=cheatSuperPowers)
    btn7.place(relx=0.75, rely=0.3, relwidth=0.2, relheight=0.1)
    btn8 = tk.Button(root, text='超级防御', command=cheatSuperDefense)
    btn8.place(relx=0.75, rely=0.5, relwidth=0.2, relheight=0.1)
    info = tk.StringVar()
    txt = tk.Entry(root, textvariable=info, state='readonly')
    txt.place(rely=0.7, relwidth=1, relheight=0.3)
    root.mainloop()


def terminal():
    FLAG = True
    while (FLAG == True):
        message = raw_input("用户输入:")
        # run 单人游戏
        if message == "r1":
            threading.Thread(target=run, args=(1,)).start()
        elif message == "r2":
            threading.Thread(target=run, args=(2,)).start()
        # quit 退出
        elif message == "q":
            FLAG = False
        # get 获取信息
        elif message == "g":
            get_info()
        # move 自动化测试开始
        elif message == "m":
            threading.Thread(target=player_move).start()
        # move 自动化测试开始
        elif message == "l":
            cheatNextLevel()


if __name__ == "__main__":
    gui()
