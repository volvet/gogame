# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 17:02:00 2020

@author: Administrator
"""

import os
import random
import re
import sys
import time
import tqdm
import argparse
import argh
import gtp as gtp_lib
from load_data_sets import parse_data_sets, DataSet


def gtp(strategy, read_file=None):
  pass

def preprocess(*data_sets, processed_dir='processed_data'):
  processed_dir = os.path.join(os.getcwd(), processed_dir)
  if not os.path.isdir(processed_dir):
    os.mkdir(processed_dir)

  print(processed_dir)
  test_chunk, training_chunks = parse_data_sets(*data_sets)
  print('Allocating %s positions as test, reminder as training' % len(test_chunk), file=sys.stderr)
  
  print('Writing test chunk')
  test_dataset = DataSet.from_positions_w_context(test_chunk, is_test=True)
  test_filename = os.path.join(processed_dir, 'test.chunk.gz')
  test_dataset.write(test_filename)
  
  print('Write training chunks')
  training_dataset = map(DataSet.from_positions_w_context, training_chunks)
  for i, dataset in tqdm.tqdm(enumerate(training_dataset)):
    pass
  

def train(processed_dir, read_file=None, save_file=None, epochs=10, logdir=None, checkpoint_freq=10000):
  pass

if __name__== '__main__':
  parser = argparse.ArgumentParser()
  argh.add_commands(parser, [gtp, preprocess, train])
  argh.dispatch(parser)