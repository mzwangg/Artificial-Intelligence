# 导入随机包
import random
import copy
import datetime
import math

class RandomPlayer:
    def __init__(self, color):
        self.color = color

    def random_choice(self, board):
        action_list = list(board.get_legal_actions(self.color))

        # 如果 action_list 为空，则返回 None,否则从中选取一个随机元素，即合法的落子坐标
        if len(action_list) == 0:
            return None
        else:
            return random.choice(action_list)

    def get_move(self, board):
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        action = self.random_choice(board)
        return action


class HumanPlayer:
    def __init__(self, color):
        self.color = color

    def get_move(self, board):
        # 如果 self.color 是黑棋 "X",则 player 是 "黑棋"，否则是 "白棋"
        if self.color == "X":
            player = "黑棋"
        else:
            player = "白棋"

        # 人类玩家输入落子位置，如果输入 'Q', 则返回 'Q'并结束比赛。
        # 如果人类玩家输入棋盘位置，e.g. 'A1'，
        # 首先判断输入是否正确，然后再判断是否符合黑白棋规则的落子位置
        while True:
            action = input(
                "请'{}-{}'方输入一个合法的坐标(e.g. 'D3'，若不想进行，请务必输入'Q'结束游戏。): ".format(player,
                                                                                                      self.color))

            # 如果人类玩家输入 Q 则表示想结束比赛
            if action == "Q" or action == 'q':
                return "Q"
            else:
                row, col = action[1].upper(), action[0].upper()

                # 检查人类输入是否正确
                if row in '12345678' and col in 'ABCDEFGH':
                    # 检查人类输入是否为符合规则的可落子位置
                    if action in board.get_legal_actions(self.color):
                        return action
                else:
                    print("你的输入不合法，请重新输入!")


def change_color(color):
    if color == "O":
        return "X"
    elif color == "X":
        return "O"
    else:
        return copy.deepcopy(color)


class UCTNode:
    #表示父节点将color色的棋放置到action位置得到该节点
    def __init__(self, color, action, parent):
        self.times = 0
        self.scores = 0
        self.color = color
        self.action = action
        self.parent = parent
        self.visited_child_nodes = []
        self.unvisited_nodes = []

    def UCB1_score(self, c):
        if self.times == 0:
            return math.inf
        return self.scores/self.times + c*(math.sqrt(2*math.log(self.parent.times)/self.times).real)

    def cal_unvisited_nodes(self,board):
        self.unvisited_nodes = list(board.get_legal_actions(change_color(self.color)))

class AIPlayer:
    def __init__(self, color, stop_condition=(1,2000), c=1):
        self.color = color
        self.c = c # c为UCB1算法中的常数
        self.stop_condition=stop_condition # 停止搜索条件数组，0号位为截止时间，1号位为截止次数

    # 当两棋手都没有棋可走时游戏结束
    def game_over(self, board):
        b_list = list(board.get_legal_actions('X'))
        w_list = list(board.get_legal_actions('O'))
        return (len(b_list) == 0 and len(w_list) == 0)


    #根据当前的棋盘和当前棋手决定下一个拓展节点
    #返回拓展节点和下一棋手的颜色
    def select(self, board):
        cur_node = self.root

        while(True):
            # 如果游戏结束了，则直接返回当前这个节点
            if(self.game_over(board)):
                return cur_node

            # 如果还有未扩展过的节点
            if(len(cur_node.unvisited_nodes)>0):
                # 随机扩展一个未扩展的节点
                action = cur_node.unvisited_nodes.pop(random.randint(0, len(cur_node.unvisited_nodes)-1))
                new_node=UCTNode(change_color(cur_node.color), action, cur_node)
                cur_node.visited_child_nodes.append(new_node)
                board._move(action, new_node.color)
                new_node.cal_unvisited_nodes(board) # 计算新节点的子节点
                return new_node

            else:
                # 如果所有的节点都扩展过了，则根据UCB1选择节点
                child_node = None
                max_child_score = -math.inf
                for cur_child_node in cur_node.visited_child_nodes:
                    cur_child_score = cur_child_node.UCB1_score(self.c)
                    if(cur_child_score>max_child_score):
                        max_child_score = cur_child_score
                        child_node = cur_child_node

                # 若无棋可走，则添加一个占位节点，保证MAX节点和MIN节点交替出现
                if (child_node == None):
                    child_node=UCTNode(change_color(cur_node.color), (-1, -1), cur_node)
                    child_node.cal_unvisited_nodes(board)
                    cur_node.visited_child_nodes.append(child_node)
                # 如果选择的不是一个占位节点，则说明有棋可下
                elif (child_node.action != (-1, -1)):
                    board._move(child_node.action, child_node.color)

                # 此时已经找到下一步需要拓展的节点，交换棋手继续探索
                cur_node = child_node

    # 表明当前color玩家已经下棋，需要模拟之后的情况
    def simulate(self, board, color):
        color = copy.deepcopy(color)
        while (not self.game_over(board)):
            color = change_color(color)
            action_list = list(board.get_legal_actions(color))
            # 如果有棋可下，则下棋
            if (len(action_list) != 0):
                action = random.choice(action_list)
                board._move(action, color)

        # 获取获胜方和获胜子数
        winner, win_score = board.get_winner()
        if ["X","O","-"][winner] != self.color: # winner为白棋时将得分取相反数，因为此时得分为white_count - black_count
            win_score = -win_score
        return win_score

    def back_propagate(self, node, win_score):
        if (node == None):  # 递归终点
            return

        # 当模拟节点颜色等于AI颜色时，该模拟节点并不是直观上以为的MAX节点
        # 因为在我的设计中，节点的颜色为达到该节点的颜色，即该颜色已经使用过了
        # 所以选择子节点的颜色其实是模拟节点颜色的相反颜色
        # 所以当模拟节点颜色等于AI颜色时，该节点为MIN节点，会加上终局得分
        if (node.color == self.color):
            node.scores += win_score
        else:
            node.scores -= win_score # 当平局时，score减去0，没有影响

        #当平局时，只增加次数，不更新得分
        node.times += 1
        self.back_propagate(node.parent, win_score)

    def UCTSearch(self, board):
        startTime = datetime.datetime.now()
        iterate_num = 0
        self.root = UCTNode(change_color(self.color), (-1, -1), None)
        self.root.cal_unvisited_nodes(board)

        while (datetime.datetime.now() - startTime).seconds < self.stop_condition[0] and \
                iterate_num< self.stop_condition[1]:
            new_board = copy.deepcopy(board)
            cur_node = self.select(new_board) #选择+扩展, select中会更新棋盘
            win_score = self.simulate(new_board, cur_node.color) #模拟
            self.back_propagate(cur_node, win_score) # 反向传播
            iterate_num += 1

        #选择置信上限区间最大的节点
        score_array=[node.UCB1_score(self.c) for node in self.root.visited_child_nodes]
        select_index=score_array.index(max(score_array))
        select_node = self.root.visited_child_nodes[select_index]
        return select_node.action

    def get_move(self, board):
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))
        # -----------------请实现你的算法代码--------------------------------------

        action = self.UCTSearch(board)
        # ------------------------------------------------------------------------
        return action