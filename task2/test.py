import numpy as np  # 提供维度数组与矩阵运算
import copy  # 从copy模块导入深度拷贝方法
import math
from board import Chessboard


# 基于棋盘类，设计搜索策略
class Game:
    def __init__(self, show=True):
        """
        初始化游戏状态.
        """

        self.chessBoard = Chessboard(show)
        self.solves = []
        self.gameInit()

    # 重置游戏
    def gameInit(self, show=True):
        """
        重置棋盘.
        """

        self.Queen_setRow = [-1] * 8
        self.chessBoard.boardInit(False)

    ##############################################################################
    ####                请在以下区域中作答(可自由添加自定义函数)                 ####
    ####              输出：self.solves = 八皇后所有序列解的list                ####
    ####             如:[[0,6,4,7,1,3,5,2],]代表八皇后的一个解为                ####
    ####           (0,0),(1,6),(2,4),(3,7),(4,1),(5,3),(6,5),(7,2)            ####
    ##############################################################################
    #                                                                            #

    def updateCheck(self,row,column,flag):
        self.check[0][column]=flag
        self.check[1][row+column]=flag
        self.check[2][row-column+8]=flag

    #下列函数，从第row行开始搜索搜索答案
    def findSolution(self,row=0):
        if row==8:
            self.solves.append(copy.deepcopy(self.ans))
            return
        for column in range(8):
            if not (self.check[0][column] or self.check[1][row+column] or self.check[2][row-column+8]):
                self.ans[row]=column
                self.updateCheck(row,column,True)
                self.findSolution(row+1)
                self.updateCheck(row,column,False)

    def run(self, row=0):

        #ans用于存储答案,check用于判断是否能放置皇后,0用于判断列上旗子的分布情况，1、2储存了旗子在对角线的分布情况
        self.ans=[False for i in range(8)]
        self.check=[[False for i in range(16)] for j in range(3)]

        self.findSolution()

    #                                                                            #
    ##############################################################################
    #################             完成后请记得提交作业             #################
    ##############################################################################

    def showResults(self, result):
        """
        结果展示.
        """

        self.chessBoard.boardInit(False)
        for i, item in enumerate(result):
            if item >= 0:
                self.chessBoard.setQueen(i, item, False)

        self.chessBoard.printChessboard(False)

    def get_results(self):
        """
        输出结果(请勿修改此函数).
        return: 八皇后的序列解的list.
        """

        self.run()
        return self.solves

a=Game()
b=a.get_results()
for i in range(5):
    print(b[i])