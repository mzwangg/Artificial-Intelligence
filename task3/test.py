


# 导入黑白棋文件
from game import Game
from player import RandomPlayer,AIPlayer,HumanPlayer

# 人类玩家黑棋初始化
black_player = AIPlayer("X")

# AI 玩家 白棋初始化
white_player = RandomPlayer("O")

# 游戏初始化，第一个玩家是黑棋，第二个玩家是白棋
game = Game(white_player,black_player)

# 开始下棋
game.run()