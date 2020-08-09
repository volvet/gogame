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
from load_data_sets import parse_data_sets


def gtp(strategy, read_file=None):
  pass

def preprocess(*data_sets, processed_dir='processed_data'):
  processed_dir = os.path.join(os.getcwd(), processed_dir)
  if not os.path.isdir(processed_dir):
    os.mkdir(processed_dir)

  print(processed_dir)
  parse_data_sets(*data_sets)
  pass

def train(processed_dir, read_file=None, save_file=None, epochs=10, logdir=None, checkpoint_freq=10000):
  pass

if __name__== '__main__':
  parser = argparse.ArgumentParser()
  argh.add_commands(parser, [gtp, preprocess, train])
  argh.dispatch(parser)