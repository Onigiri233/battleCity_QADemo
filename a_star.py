# -*- encoding: utf-8 -*-
"""
@File    : a_star.py
@Time    : 2020/4/8 8:56
@Author  : Fantuan
@Software: PyCharm
"""

#!/bin/python
# -*- coding:utf-8 -*-

# def dijkstra(graph, startIndex, path, cost, max):
#     """
#     求解各节点最短路径，获取path，和cost数组，
#     path[i] 表示vi节点的前继节点索引，一直追溯到起点。
#     cost[i] 表示vi节点的花费
#     """
#     lenth = len(graph)
#     v = [0] * lenth
#     # 初始化 path，cost，V
#     for i in range(lenth):
#         if i == startIndex:
#             v[startIndex] = 1
#         else:
#             cost[i] = graph[startIndex][i]
#             path[i] = (startIndex if (cost[i] < max) else -1)
#     # print v, cost, path
#     for i in range(1, lenth):
#         minCost = max
#         curNode = -1
#         for w in range(lenth):
#             if v[w] == 0 and cost[w] < minCost:
#                 minCost = cost[w]
#                 curNode = w
#         # for 获取最小权值的节点
#         if curNode == -1: break
#         # 剩下都是不可通行的节点，跳出循环
#         v[curNode] = 1
#         for w in range(lenth):
#             if v[w] == 0 and (graph[curNode][w] + cost[curNode] < cost[w]):
#                 cost[w] = graph[curNode][w] + cost[curNode] # 更新权值
#                 path[w] = curNode # 更新路径
#         # for 更新其他节点的权值（距离）和路径
#     return path
# def AStar(maze, start_pos, end_pos):
#     TILE_SIZE = 16
#     openPointList = []
#     PointSet = set()
#     # closePointList = []
#     openPointList.append(start_pos)
#     while len(openPointList) > 0:
#         x, y = openPointList.pop(0)
#         if x > 0:
#             if maze[x - 1][y] == 0 and (x - 1, y) not in PointSet:
#                 openPointList.append((x - 1, y))
#                 PointSet.add((x - 1, y))
#         elif y > 0:
#             if maze[x][y-1] == 0 and (x, y - 1) not in PointSet:
#                 openPointList.append((x, y - 1))
#                 PointSet.add((x, y - 1))
#         elif x < TILE_SIZE-1:
#             if maze[x+1][y] == 0 and (x + 1, y) not in PointSet:
#                 openPointList.append((x + 1, y))
#                 PointSet.add((x + 1, y))
#         elif y < TILE_SIZE-1:
#             if maze[x][y + 1] == 0 and (x, y + 1) not in PointSet:
#                 openPointList.append((x , y + 1))
#                 PointSet.add((x, y + 1))
#         if openPointList[-1]==end_pos:
#             break
#     print openPointList
#     return

import os, sys, random, math

# 地图设置
import tanks

gameMapWidth = 26
gameMapHeight = 26
gameMap = []

# 地图障碍物
# obstacleCount = 5

# 块状态
ITEM_STAT_NORMAL = 0  # 空点
ITEM_STAT_OBSTACLE = 1  # 障碍物
ITEM_STAT_START = 2  # 起点
ITEM_STAT_END = 3  # 终点

# 起点和终点
spNum = -1
epNum = -1


# 每块的属性
class Item:
    def __init__(self, x, y, status):
        self.x = x
        self.y = y
        self.status = status
        self.mf = -1
        self.mg = -1
        self.mh = -1
        self.mParent = None
        self.isPath = 0


# 初始化地图
def initMap(maze, start_pos, end_pos):
    for wc in xrange(gameMapWidth):
        for hc in xrange(gameMapHeight):
            gameMap.append(Item(wc, hc, ITEM_STAT_NORMAL))

    # 插入障碍物
    for i in xrange(gameMapWidth):
        for j in xrange(gameMapHeight):
            if maze[i][j]==1:
                gameMap[i*gameMapHeight+j].status = ITEM_STAT_OBSTACLE

    global spNum
    global epNum
    # 选取起点和终点
    while (spNum == -1):
        x,y=start_pos
        choose = y*gameMapHeight+x
        if gameMap[choose].status == 0:
            spNum = choose
            gameMap[spNum].status = ITEM_STAT_START

    while (epNum == -1):
        x, y = end_pos
        choose = y*gameMapHeight+x
        if gameMap[choose].status == 0:
            epNum = choose
            gameMap[epNum].status = ITEM_STAT_END


# 输出地图信息
def printMap():
    for itemc in xrange(len(gameMap)):
        if gameMap[itemc].status == ITEM_STAT_START:
            print "START",
        elif gameMap[itemc].status == ITEM_STAT_END:
            print "END  ",
        elif gameMap[itemc].isPath == 1:
            print "path ",
        else:
            print "%d   " % (gameMap[itemc].status),

        if (itemc + 1) % gameMapHeight == 0:
            print "\n"


# 寻路
def findPath():
    path=[]
    global spNum
    global epNum

    # 开启列表
    openPointList = []
    # 关闭列表
    closePointList = []

    # 开启列表插入起始点
    openPointList.append(gameMap[spNum])
    while (len(openPointList) > 0):
        # 寻找开启列表中最小预算值的点
        minFPoint = findPointWithMinF(openPointList)
        # 从开启列表移除,添加到关闭列表
        openPointList.remove(minFPoint)
        closePointList.append(minFPoint)
        # 找到当前点周围点
        surroundList = findSurroundPoint(minFPoint, closePointList)

        # 开始寻路
        for sp in surroundList:
            # 存在在开启列表，说明上一块查找时并不是最优路径，考虑此次移动是否是最优路径
            if sp in openPointList:
                newPathG = CalcG(sp, minFPoint)  # 计算新路径下的G值
                if newPathG < sp.mg:
                    sp.mg = newPathG
                    sp.mf = sp.mg + sp.mh
                    sp.mParent = minFPoint
            else:
                sp.mParent = minFPoint  # 当前查找到点指向上一个节点
                CalcF(sp, gameMap[epNum])
                openPointList.append(sp)
        if gameMap[epNum] in openPointList:
            gameMap[epNum].mParent = minFPoint

            break
    curp = gameMap[epNum]
    while True:
        curp.isPath = 1
        # print((curp.y, curp.x))
        path.append((curp.y, curp.x))
        curp = curp.mParent
        if curp == None:
            break
    # print "\n"
    # printMap()
    # path.reverse()
    return path[1:-1]


def CalcG(point, minp):
    return math.sqrt((point.x - point.mParent.x) ** 2 + (point.y - point.mParent.y) ** 2) + minp.mg


# 计算每个点的F值
def CalcF(point, endp):
    h = abs(endp.x - point.x) + abs(endp.y - point.y)
    g = 0
    if point.mParent == None:
        g = 0
    else:
        g = point.mParent.mg + math.sqrt((point.x - point.mParent.x) ** 2 + (point.y - point.mParent.y) ** 2)
    point.mg = g
    point.mh = h
    point.mf = g + h
    return


# 不能是障碍块，不包含在关闭列表中
def notObstacleAndClose(point, closePointList):
    if point not in closePointList and point.status != ITEM_STAT_OBSTACLE:
        return True
    return False


# 查找周围块
def findSurroundPoint(point, closePointList):
    surroundList = []
    up = None
    down = None
    left = None
    right = None


    # 上面的点存在
    if point.x > 0:
        up = gameMap[gameMapHeight * (point.x - 1) + point.y]
        if notObstacleAndClose(up, closePointList):
            surroundList.append(up)
    # 下面的点存在
    if point.x < gameMapWidth - 1:
        down = gameMap[gameMapHeight * (point.x + 1) + point.y]
        if notObstacleAndClose(down, closePointList):
            surroundList.append(down)
    # 左边的点存在
    if point.y > 0:
        left = gameMap[gameMapHeight * (point.x) + point.y - 1]
        if notObstacleAndClose(left, closePointList):
            surroundList.append(left)
    # 右边的点存在
    if point.y < gameMapHeight - 1:
        right = gameMap[gameMapHeight * (point.x) + point.y + 1]
        if notObstacleAndClose(right, closePointList):
            surroundList.append(right)
    return surroundList


# 查找list中最小的f值
def findPointWithMinF(openPointList):
    f = 0xffffff
    temp = None
    for pc in openPointList:
        if pc.mf < f:
            temp = pc
            f = pc.mf
    return temp


def AStar(maze, start_pos, end_pos):
    initMap(maze, start_pos, end_pos)  ##初始化地图
    # printMap()  ##输出初始化地图信息
    path=findPath()
    # print(path)
    return path  ##查找最优路径
if __name__ == '__main__':
    maze = [[0] * 26 for i in range(26)]
    # for tile in tanks.game.level.obstacle_rects:
    #     maze[tile.y / 16][tile.x / 16] = 1
    initMap(maze, (8,24), (12,0))  ##初始化地图
    # printMap()  ##输出初始化地图信息
    findPath()  ##查找最优路径


