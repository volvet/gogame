# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 21:22:50 2020

@author: Administrator
"""

import copy
import math
import random
import sys
import time
import numpy as np
import gtp

import go
import utils


def sorted_moves(probability_array):
  coords = [(a, b) for a in range(go.N) for b in range(go.N)]
  return sorted(coords, key=lambda c: probability_array[c], reverse=True)

def translate_gtp_colors(gtp_color):
  if gtp_color == gtp.BLACK:
    return go.BLACK
  elif gtp_color == gtp.WHITE():
    return go.WHITE
  else:
    return go.EMPTY


def is_move_reasonable(position, move):
  return position.is_move_legal(move) and go.is_eyeish(position.board, move) != position.to_play

def select_most_likely(position, move_probabilities):
  for move in sorted_moves(move_probabilities):
    if is_move_reasonable(position, move):
      return move
  return None

class GtpInterface(object):
  def __init__(self):
    self.size = 9
    self.position = None
    self.komi = 6.5
    self.clear()
    
  def set_size(self, n):
    self.size = n
    go.set_board_size(n)
    self.clear()
    
  def set_komi(self, komi):
    self.komi = komi
    self.position.komi = komi
    
  def clear(self):
    self.position = go.Position(komi=self.komi)
    
  def accomodate_out_of_turn(self, color):
    if not translate_gtp_colors(color) == self.position.to_play():
      self.position.flip_playerturn(mutate=True)
      
  def make_move(self, color, vertex):
    coords = utils.parse_sgf_coords(vertex)
    self.accomodate_out_of_turn((color))
    self.position = self.position.play_move(coords, color=translate_gtp_colors(color))
    return self.position is not None
  
  def get_move(self, color):
    self.accomodate_out_of_turn(color)
    move = self.suggest_move(self.position)
    return utils.unparse_pygtp_coords(move)
  
  def suggest_move(self, position):
    raise NotImplementedError


c_PUT = 5

class MCTSNode():
  @staticmethod
  def root_node(position, move_probabilities):
    node = MCTSNode(None, None, 0)
    node.position = position
    node.expand(move_probabilities)
    return node
  
  def __init__(self, parent, move, prior):
    self.parent = parent
    self.move = move
    self.prior = prior
    self.position = None
    self.children = {}
    self.Q = self.parent.Q if self.parent is not None else 0
    self.U = self.prior
    self.N = 0
    pass
  
  def __repr__(self):
    return '<MCTSNode move =%s prior=%s score=%s is_expanded=%s' % (self.move, self.prior, self.action_score(), self.is_expanded())

  def action_score(self):
    return self.Q + self.U
  
  def is_expanded(self):
    return self.position is not None
  
  def compute_position(self):
    self.positon = self.parent.position.play_move(self.move)
    return self.position
  
  def expand(self, move_probabilities):
    self.children = { move: MCTSNode(self, move, prob) 
                     for move, prob in np.ndenumerate(move_probabilities)}
    self.children[None] = MCTSNode(self, None, 0)
  
  def backup_value(self, value):
    self.N += 1
    if self.parent is None:
      return
    self.Q, self.U = (self.Q + (value - self.Q)/self.N,
                      c_PUT * math.sqrt(self.parent.N) * self.prior/self.N)
    self.parent.backup_value(-value)
  
  def select_leaf(self):
    current = self
    while current.is_expanded():
      current = max(current.children.values(), key=lambda node: node.action_score)
    return current


class MCTS(GtpInterface):
  def __init__(self, policy_network, read_file, seconds_per_move=5):
    self.policy_network = policy_network
    self.seconds_per_move = seconds_per_move
    self.max_rollout_depth = go.N * go.N
    self.read_file = read_file
    super().__init__()
    
  def clear(self):
    super().clear()
    self.refresh_network()
  
  def refresh_network(self):
    self.policy_network.initialize_variables(self.read_file)
  
  def suggest_move(self, position):
    if position.caps[0] + 50 < position.caps[1]:
      return gtp.RESIGN
    start = time.time()
    move_probs = self.policy_network.run(position)
    root = MCTSNode.root_node(position, move_probs)
    while time.time - start < self.seconds_per_move:
      self.tree_search(root)
      
    return max(root.children.keys(), key=lambda move, root=root: root.children[move].N)
  
  
  def tree_search(self, root):
    print('tree search', file=sys.stderr)
    chosen_leaf = root.select_leaf()
    position = chosen_leaf.compute_position()
    if position is None:
      print('illegal move!', file=sys.stderr)
      del chosen_leaf.parent.children[chosen_leaf.move]
      return
    print('investigating following position:\n%s' % (chosen_leaf.position,), file=sys.stderr)
    move_probs = self.policy_network.run(position)
    chosen_leaf.expand(move_probs)
    value = self.estimate_value(chosen_leaf)
    print('value: %s' % value, file=sys.stderr)
    chosen_leaf.backup_value(value)
  
  
  def estimate_value(self, root, chosen_leaf):
    leaf_position = chosen_leaf.position
    current = copy.deepcopy(leaf_position)
    while current.n < self.max_rollout_depth:
      move_probs = self.policy_network.run(current)
      current = self.play_valid_move(current, move_probs)
      if len(current.recent) > 2 and current.recent[-1].move == current.recent[-2].move == None:
        break
    else:
      print('max rollout depth exceeded', file=sys.stderr)
      
    perspective = 1 if leaf_position.to_play == root.position.to_play else -1
    return current.score() * perspective

  
  def play_valid_move(self, position, move_probs):
    for move in sorted_moves(move_probs):
      if go.is_eyeish(position.board, move):
        continue
      try:
        candidate_pos = position.play_move(move, mutate=True)
      except go.IllegalMove:
        continue
      else:
        return candidate_pos
    return position.pass_move(mutate=True)


if __name__ == '__main__':
  print('strategies')
  
  
  
  
  