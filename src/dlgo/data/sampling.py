
from __future__ import print_function
from __future__ import absolute_import
import os
import sys
import random
from six.moves import range

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/..')
from dlgo.data.index_processor import KGSIndex


class Sampler:
  def __init__(self, data_dir='data', num_test_games=100, cap_year=2020, seed=1337):
    self.data_dir = data_dir
    self.num_test_games = num_test_games
    self.test_games = []
    self.train_games = []
    self.test_sample_filename = 'test_samples.txt'
    self.cap_year = cap_year
    random.seed(seed)
    self.compute_test_samples()
    
  def draw_data(self, data_type, num_samples):
    if data_type == 'test':
      return self.test_games
    elif data_type == 'train' and num_samples is not None:
      return self.draw_training_samples(num_samples)
    elif data_type == 'train' and num_samples is None:
      return self.draw_all_training()
  
  def draw_samples(self, num_sample_games):
    available_games = []
    index = KGSIndex(data_directory=self.data_dir)
    
    for fileinfo in index.file_info:
      filename = fileinfo['filename']
      #year = int(filename.split('-')[1].split('-')[0])
      #if year > self.cap_year:
      #  continue
      num_games = fileinfo['num_games']
      for i in range(num_games):
        available_games.append((filename, i))
    print('>>> Total number of games used: ' + str(len(available_games)))
    sample_set = set()
    while(len(sample_set) < num_sample_games):
      sample = random.choice(available_games)
      if sample not in sample_set:
        sample_set.add(sample)
    print('Drawn ' + str(num_sample_games) + ' samples:')
    return list(sample_set)
  
  def draw_training_games(self):
    index = KGSIndex(data_directory=self.data_dir)

    for fileinfo in index.file_info:
      filename = fileinfo['filename']
      #year = int(filename.split('-')[1].split('-')[0])
      #if year > self.cap_year:
      #  continue
      num_games = fileinfo['num_games']
      for i in range(num_games):
        sample = (filename, i)
        if sample not in self.train_games:
          self.train_games.append(sample)
    print('toal num training samples: ' + str(len(self.train_games)))
    
  def compute_test_samples(self):
    if not os.path.isfile(self.test_sample_filename):
      test_games = self.draw_samples(self.num_test_games)
      test_sample_file = open(self.test_sample_filename, 'w')
      for sample in test_games:
        test_sample_file.write(str(sample) + '\n')
      test_sample_file.close()
    
    test_sample_file = open(self.test_sample_filename, 'r')
    sample_contents = test_sample_file.read()
    test_sample_file.close()
    for line in sample_contents.split('\n'):
      if line != '':
        (filename, index) = eval(line)
        self.test_games.append((filename, index))
    
  def draw_training_samples(self, num_sample_games):
    available_games = []
    index = KGSIndex(data_directory=self.data_dir)
    for fileinfo in index.file_info:
      filename = fileinfo['filename']
      #year = int(filename.split('-')[1].split('-')[0])
      #if year > self.cap_year:
      #  continue
      num_games = fileinfo['num_games']
      for i in range(num_games):
        available_games.append((filename, i))
    sample_set = set()
    while len(sample_set) < num_sample_games:
      sample = random.choice(available_games)
      if sample not in sample_set:
        sample_set.add(sample)
    print('Drawn ' + str(num_sample_games) + ' samples')
    return list(sample_set)
  
  def draw_all_training(self):
    available_games = []
    index = KGSIndex(data_directory=self.data_dir)
    
    for fileinfo in index.file_info:
      filename = fileinfo['filename']
      #year = int(filename.split('-')[1].split('-')[0])
      #if year > self.cap_year:
      #  continue
      num_games = fileinfo['num_games']
      for i in range(num_games):
        available_games.append((filename, i))
    print('>>> Total number of games used: ' + str(len(available_games)))
    sample_set = set()
    for sample in available_games:      
      if sample not in sample_set:
        sample_set.add(sample)
    print('Drawn all samples, ie ' + str(len(sample_set)) + ' samples:')
    return list(sample_set)
    pass

if __name__ == '__main__':
  print('dlgo.data.sampling')


