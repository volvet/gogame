
from __future__ import absolute_import

import os
import sys
import tarfile
import gzip
import glob
import shutil
import numpy as np
from tensorflow.keras.utils import to_categorical

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/..')
from dlgo.gosgf import Sgf_game
from dlgo.goboard import Board, GameState, Move
from dlgo.gotypes import Player, Point
from dlgo.encoders.base import get_encoder_by_name
from dlgo.data.index_processor import KGSIndex

class GoDataProcessor:
  def __init__(self, encoder='oneplane', data_directory='data'):
    self.encoder= get_encoder_by_name(encoder, 19)
    self.data_dir = data_directory


if __name__ == '__main__':
  print('dlgo.data.processor')


