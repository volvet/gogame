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
from contextlib import contextmanager
from load_data_sets import parse_data_sets, DataSet
from policy import PolicyNetwork
from strategies import MCTS

TRAINING_CHUNK_RE = re.compile(r'train\d+\.chunk.gz')

@contextmanager
def timer(message):
  tick = time.time()
  yield
  tock = time.time()
  #print('%s, %0.3f' % (message, (tock-tick)))


def gtp(strategy, read_file=None):
  network = PolicyNetwork()
  instance = MCTS(network, read_file)
  gtp_engine = gtp_lib.Engine(instance)
  print('gtp engine ready')
  while not gtp_engine.disconnect:
    inpt = input()
    try:
      cmd_list = inpt.split('\n')
    except:
      cmd_list = [inpt]
    for cmd in cmd_list:
      print('sending cmd %s' % cmd)
      engine_reply = gtp_engine.send(cmd)
      print(engine_reply)

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
  
  print('\nWrite training chunks')
  training_datasets = map(DataSet.from_positions_w_context, training_chunks)
  for i, dataset in tqdm.tqdm(enumerate(training_datasets)):
    train_filename = os.path.join(processed_dir, 'train%s.chunk.gz' % i)
    dataset.write(train_filename)
  

def train(processed_dir, read_file=None, save_file=None, epochs=10, logdir=None, checkpoint_freq=10000):
  test_dataset = DataSet.read(os.path.join(processed_dir, 'test.chunk.gz'))
  #print(test_dataset)
  train_chunk_files = [os.path.join(processed_dir, fname)
                       for fname in os.listdir(processed_dir) if TRAINING_CHUNK_RE.match(fname)]
  print(train_chunk_files)
  if read_file is not None:
    read_file = os.path.join(os.getcwd(), save_file)
  n = PolicyNetwork()
  n.initialize_variables()
  if logdir is not None:
    n.initialize_logging(logdir)
    
  last_save_checkpoint = 0
  for i in range(epochs):
    random.shuffle(train_chunk_files)
    for file in tqdm.tqdm(train_chunk_files, desc='epochs ' + str(i)):
      #print('Using %s' % file)
      with timer('load dataset'):
        train_dataset = DataSet.read(file)
      with timer('training'):
        n.train(train_dataset)
      if n.get_global_step() > last_save_checkpoint + checkpoint_freq:
        with timer('save model'):
          n.save_variables(save_file)
        with timer('test set evaluation'):
          n.check_accuracy(test_dataset)
        last_save_checkpoint = n.get_global_step()
    with timer('test set evaluation'):
      n.check_accuracy(test_dataset)


if __name__== '__main__':
  parser = argparse.ArgumentParser()
  argh.add_commands(parser, [gtp, preprocess, train])
  argh.dispatch(parser)