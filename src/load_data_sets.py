# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 19:04:56 2020

@author: Administrator
"""

import sys
import os
import itertools
import struct

from sgf_wrapper import replay_sgf

CHUNK_SIZE = 4096
CHUNK_HEADER_FORMAT = 'iii?'
CHUNK_HEADER_SIZE = struct.calcsize(CHUNK_HEADER_FORMAT)

def find_sgf_files(*dataset_dirs):
  for dataset_dir in dataset_dirs:
    full_dir = os.path.join(os.getcwd(), dataset_dir)
    dataset_files = [os.path.join(full_dir, name) for name in os.listdir(full_dir)]
    for f in dataset_files:
      if os.path.isfile(f) and f.endswith('.sgf'):
        yield f
        
def get_positions_from_sgf(file):
  with open(file) as f:
    for position_w_content in replay_sgf(f.read()):
      if position_w_content.is_usable():
        yield position_w_content
        
def split_test_training(position_w_context, est_num_positions):
  desired_test_size = 10**5
  if est_num_positions < 2 * desired_test_size:
    print('Not enough data to have a full test set, splitting 67:33')
  else:
    print('Estimated number of chunk: %s' % (
      (est_num_positions - desired_test_size) // CHUNK_SIZE), file=sys.stderr)

def parse_data_sets(*data_sets):
  print('Searching the following directories {} for SGFS'.format('\n'.join(data_sets)))
  sgf_files = list(find_sgf_files(*data_sets))
  print('%s sgf files found' % len(sgf_files), file=sys.stderr)
  est_num_positions = len(sgf_files) * 200
  positions_w_context = itertools.chain(*map(get_positions_from_sgf, sgf_files))
  split_test_training(positions_w_context, est_num_positions)
  

if __name__ == '__main__':
  print('load_data_sets')