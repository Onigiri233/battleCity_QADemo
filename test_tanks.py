# -*- encoding: utf-8 -*-
"""
@File    : test_tanks.py
@Time    : 2020/3/21 21:20
@Author  : Fantuan
@Software: PyCharm
"""
import pygame

import tanks
import Tkinter as tk
import os, threading


def run(nr_of_players=1):
    tanks.game = tanks.Game()
    tanks.castle = tanks.Castle()
    tanks.play_sounds=False
    tanks.game.stage = 0
    tanks.game.nr_of_players = nr_of_players
    tanks.game.nextLevel()
    player_move_gui()


def run_gui_single():
    th = threading.Thread(target=run, args=(1,))
    th.setDaemon(True)  # 守护线程
    th.start()


def run_gui_double():
    th = threading.Thread(target=run, args=(2,))
    th.setDaemon(True)  # 守护线程
    th.start()

dirction = ("向上", "向右", "向下", "向左")
tank_type = ("普通", "三倍移速", "超级子弹", "四倍血量")
bullet_owner = ("我方", "敌方")
bonus_type=("手雷", "无敌", "保护", "星星", "生命", "冻结")
tile_type=("空", "砖", "铁", "水", "草", "冰")
def get_info():

    strbuf = ""
    for player in tanks.players:
        strbuf += "玩家位置%s，移动方向：%s\n" % ((player.rect[0], player.rect[1]), dirction[player.direction],)

    for enemy in tanks.enemies:
        strbuf += "敌人位置%s，类型%s，移动方向：%s，移动速度：%s,移动路径%s\n" % (
        (enemy.rect[0], enemy.rect[1]), tank_type[enemy.type], dirction[enemy.direction], enemy.speed,
        (enemy.path[0], enemy.path[-1]),)
    for bullet in tanks.bullets:
        strbuf += "子弹位置%s，归属%s，移动方向：%s，移动速度：%s\n" % (
        (bullet.rect[0], bullet.rect[1]), bullet_owner[bullet.owner], dirction[bullet.direction], bullet.speed,)
    for bonus in tanks.bonuses:
        strbuf += "BUFF类型%s\n"%(bonus_type[bonus.bonus],)
    strbuf += "当前关卡%s\n"%(tanks.game.stage)
    level = tanks.Level(tanks.game.stage)
    # print (level.obstacle_rects)
    # print (level.mapr)
    for tile in level.mapr:
        for player in tanks.players:
            # pygame.Rect(position[0] - 8 , position[1] + 11, 8, 6).colliderect(castle.rect)
            # print ("%s-%s")%(tile.topleft,(player.rect[0],player.rect[1]))
            if tile.x ==player.rect[0] or tile.y==player.rect[1]:
                print("[%s,%s]")%(tile.topleft,tile_type[tile.type])


    print strbuf
    return strbuf


def get_output_doc():
    print (tanks.game.stage)
    for player in tanks.players:
        print ("消灭%s，得分%s" %(str(player.trophies) ,str(player.score)))



def player_move():
    while not tanks.game.game_over:
        for player in tanks.players:
            for enemy in tanks.enemies:
                # dirction = ("向上", "向右", "向下", "向左")
                for pos in enemy.path[8:]:
                    x,y=pos[0],pos[1]
                    is_fire=False

                    if x==player.rect[0] and y<=player.rect[1]:
                        #             在上面
                        bullet_speed=5
                        if player.superpowers > 0:
                            bullet_speed = 8

                        time_enemy=enemy.path.index(pos)/enemy.speed
                        time_player=(player.rect[1]-y)/bullet_speed
                        if(time_enemy==time_player):
                            player.rotate(tanks.Tank.DIR_UP)
                            is_fire=True

                    elif x==player.rect[0] and y>=player.rect[1]:
                        #             在下面
                        player.rotate(tanks.Tank.DIR_DOWN)
                        is_fire=True

                    elif x>=player.rect[0] and y==player.rect[1]:
                        #             在右边
                        player.rotate(tanks.Tank.DIR_RIGHT)
                        is_fire=True

                    elif x <= player.rect[0] and y == player.rect[1]:
                        #             在左边
                        player.rotate(tanks.Tank.DIR_LEFT)
                        is_fire=True
                    if is_fire:
                        print ("开火，目标是%s"%((x,y),))
                        if player.state == player.STATE_ALIVE:
                            player.fire()

            # 获取上下左右能达到的坐标范围
            available_positions=[]


def player_move_gui():
    th = threading.Thread(target=player_move)
    th.setDaemon(True)  # 守护线程
    th.start()
def route_info():
    rects = []

    while not tanks.game.game_over:
        print ("%s!!!%s\n|||||||||||||||||%s")%(cmp(rects,tanks.game.level.obstacle_rects),rects,tanks.game.level.obstacle_rects,)
        if cmp(rects,tanks.game.level.obstacle_rects)==0:
            pass
        else:
            rects = tanks.game.level.obstacle_rects
            surface_route = pygame.Surface((8 * 2, 8 * 2)).convert_alpha()
            surface_route.fill((255, 0, 255, 50))
            for tile in rects:
                tanks.screen.blit(surface_route, tile.topleft)


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
        strbuf=get_info()
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
    info=tk.StringVar()
    txt = tk.Entry(root,textvariable=info,state='readonly')
    txt.place(rely=0.7,relwidth=1, relheight=0.3)
    root.mainloop()

def terminal():
    FLAG = True
    while (FLAG == True):
        message = raw_input("用户输入:")
        # run 单人游戏
        if message == "r1":
            threading.Thread(target=run,args=(1,)).start()
        elif message == "r2":
            threading.Thread(target=run,args=(2,)).start()
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
    # terminal()
    gui()

