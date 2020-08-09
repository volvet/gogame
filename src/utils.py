# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 10:46:36 2020

@author: Administrator
"""


import gtp
import go


KGS_COLUMNS = 'ABCDEFGHJKLMNOPQRST'
SGF_COLUMNS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def parse_sgf_coords(s):
  'Interprets coords. aa is top left corner; sa is top right corner'
  if s is None or s == '':
    return None
  return SGF_COLUMNS.index(s[1]), SGF_COLUMNS.index(s[0])