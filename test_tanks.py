# -*- encoding: utf-8 -*-
"""
@File    : test_tanks.py
@Time    : 2020/3/21 21:20
@Author  : Fantuan
@Software: PyCharm
"""
import tanks
import Tkinter as tk
import os, threading


def run_single():
	tanks.game = tanks.Game()
	tanks.castle = tanks.Castle()
	tanks.game.stage = 1
	tanks.game.nr_of_players = 1
	tanks.game.nextLevel()

def run_double():
	game = tanks.Game()
	tanks.castle = tanks.Castle()
	game.stage = 1
	game.nr_of_players = 2
	game.nextLevel()

def get_info():
	for player in tanks.players:
		# 玩家 位置 生命数 状态
		print("玩家"+str((player.rect[0],player.rect[1]))+str(player.state))
	for enemy in tanks.enemies:
		# 敌人 位置 形态 路径
		print("敌人"+str((enemy.rect[0],enemy.rect[1]))+str(enemy.type)+str(enemy.path))
	for bullet in tanks.bullets:
		# 子弹 位置 归属 生命数 状态
		print("子弹"+str((bullet.rect[0],bullet.rect[1]))+str(bullet.owner))
	print("BUFF"+str(tanks.bonuses))
	print("LABELS"+str(tanks.labels))

def player_move():
	for player in tanks.players:
		player.move(player.DIR_UP)

# 作弊能力
def cheatNextLevel():
	tanks.game.finishLevel()

def gui():
	root = tk.Tk()
	root.geometry('460x240')
	root.title('自动化测试')

	lb1 = tk.Label(root, text='自动化测试')
	lb1.pack()

	btn1 = tk.Button(root, text='单人模式', command=threading.Thread(target=run_single).start())
	btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)
	btn2 = tk.Button(root, text='双人模式', command=run_double())
	btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)

	btn2 = tk.Button(root, text='自动化开始', command=get_info)
	btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)
	btn2 = tk.Button(root, text='显示信息', command=get_info)
	btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)
	btn2 = tk.Button(root, text='结果分析', command=get_info)
	btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)


	txt = tk.Text(root)
	txt.place(rely=0.6, relheight=0.4)
	root.mainloop()


def terminal():
	FLAG = True
	while (FLAG == True):
		message = raw_input("用户输入:")
		# run 单人游戏
		if message == "r":
			threading.Thread(target=run_single).start()
		# quit 退出
		elif message == "q":
			FLAG=False
		# get 获取信息
		elif message == "get":
			get_info()
		# move 自动化测试开始
		elif message == "m":
			threading.Thread(target=player_move()).start()
		# move 自动化测试开始
		elif message == "l":
			cheatNextLevel()



if __name__ == "__main__":
	terminal()
	# gui()