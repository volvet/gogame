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
    self.position = go.Position(komo=self.komi)


if __name__ == '__main__':
  print('strategies')