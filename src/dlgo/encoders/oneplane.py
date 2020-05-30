import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/..')
from dlgo.encoders.base import Encoder
from dlgo.gotypes import Point
#from dlgo.goboard import GameState

class OnePlaneEncoder(Encoder):
  def __init__(self, board_size):
    self.board_width, self.board_height = board_size
    self.num_planes = 1
    
  def name(self):
    return 'oneplane'
  
  def encode(self, game_state):
    board_matrix = np.zero(self.shape())
    next_player = game_state.next_player
    for r in range(self.board_height):
      for c in range(self.board_width):
        p = Point(row=r+1, col=c+1)
        go_string = game_state.board.get_go_string(p)
        if go_string is None:
          continue
        if go_string.color == next_player:
          board_matrix[0, r, c] = 1
        else:
          board_matrix[0, r, c] = -1
    return board_matrix

  
  def encode_point(self, point):
    return self.board_width * (point.row - 1) + point.col - 1
  
  def encode_point_index(self, index):
    row = index // self.board_width
    col = index % self.board_width
    return Point(row=row+1, col=col+1)
  
  def num_point(self):
    return self.board_width * self.board_height
  
  def shape(self):
    return self.num_planes, self.board_width, self.board_height
  
def create(board_size):
  return OnePlaneEncoder(board_size)
    

if __name__ == '__main__':
  print('dlgo.encoders.oneplane')