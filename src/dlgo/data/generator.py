
import glob
import numpy as np
from tensorflow.keras.utils import to_categorical

class DataGenerator:
  def __init__(self, data_directory, samples):
    self.data_directory = data_directory
    self.samples = samples
    self.files = set(filename for filename, index in samples)
    self.num_samples = None
    
  def get_num_samples(self, batch_size=128, num_classes=19*19):
    if self.num_samples is not None:
      return self.num_samples
    else:
      self.num_samples = 0
      for x, y in self._generate():
        self.num_samples += x.shape[0]
      return self.num_samples
  
  def _generate(self, batch_size, num_classes):
    for zip_file_name in self.files:
      filename = zip_file_name.replace('tar.gz', '') + 'train'
      base = self.data_directory + '/' + filename + '_features_*.npy'
      for feature_file in glob.glob(base):
        label_file = feature_file.replace('features', 'labels')
        x = np.load(feature_file)
        y = np.load(label_file)
        x = x.astype('float32')
        y = to_categorical(y.astype('int'), num_classes)
        while x.shape[0] >= batch_size:
          x_batch, x = x[:batch_size], x[batch_size:]
          y_batch, y = y[:batch_size], y[batch_size:]
          yield x_batch, y_batch
  
  def generate(self, batch_size=128, num_classes=19*19):
    #TODO: dead loop?
    while True:
      for item in self._generate(batch_size, num_classes):
        yield item

if __name__ == '__main__':
  print('dlgo.data.generator')


