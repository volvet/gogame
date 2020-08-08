
from __future__ import print_function

from dlgo.agent.native import RandomBot
from dlgo import goboard_slow
from dlgo import goboard
from dlgo import gotypes
from dlgo.utils import print_board, print_move
import time
#import os


def main():
  board_size = 9
  game = goboard.GameState.new_game(board_size)
  bots = {
    gotypes.Player.black: RandomBot(),
    gotypes.Player.white: RandomBot(),
  }
  while not game.is_over():
    time.sleep(0.3)
    print(chr(27) + "[2J")
    print_board(game.board)
    bot_move = bots[game.next_player].select_move(game)
    #print(bot_move.point, game.next_player)
    #print_move(game.next_player, bot_move)
    game = game.apply_move(bot_move)

if __name__ == '__main__':
  main()