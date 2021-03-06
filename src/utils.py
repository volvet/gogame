# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 10:46:36 2020

@author: Administrator
"""


import functools
import operator
import gtp
import go


KGS_COLUMNS = 'ABCDEFGHJKLMNOPQRST'
SGF_COLUMNS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def parse_sgf_to_flat(sgf):
  return flatten_coords(parse_sgf_coords(sgf))

def flatten_coords(c):
  return go.N * c[0] + c[1]

def unflatten_coords(f):
  return divmod(f, go.N)

def parse_kgs_coords(s):
  'Interprets coords. A1 is bottom left; A9 is top left.'
  if s == 'pass':
    return None
  s = s.upper()
  col = KGS_COLUMNS.index(s[0])
  row_from_bottom = int(s[1:]) - 1
  return go.N - row_from_bottom - 1, col

def parse_pygtp_coords(vertex):
  'Interprets coords. (1, 1) is bottom left; (1, 9) is top left.'
  if vertex in (gtp.PASS, gtp.RESIGN):
    return None
  return go.N - vertex[1], vertex[0] - 1

def unparse_pygtp_coords(c):
  if c == gtp.RESIGN:
    return gtp.RESIGN
  if c is None:
    return gtp.PASS
  return c[1] + 1, go.N - c[0]

def parse_sgf_coords(s):
  'Interprets coords. aa is top left corner; sa is top right corner'
  if s is None or s == '':
    return None
  return SGF_COLUMNS.index(s[1]), SGF_COLUMNS.index(s[0])

def product(numbers):
  return functools.reduce(operator.mul, numbers)

if __name__ == '__main__':
  print('utils')