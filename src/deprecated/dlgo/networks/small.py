from __future__ import absolute_import

from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.layers import Conv2D, ZeroPadding2D


def layers(input_shape):
  return [
    ZeroPadding2D(padding=3, input_shape=input_shape, data_forma='channel_first'),
    Conv2D(48, (7, 7), data_format='channel_first'),
    Activation('relu'),
    
    ZeroPadding2D(padding=2, data_forma='channel_first'),
    Conv2D(32, (5, 5), data_forma='channel_first'),
    Activation('relu'),
    
    ZeroPadding2D(padding=2, data_forma='channel_first'),
    Conv2D(32, (5, 5), data_forma='channel_first'),
    Activation('relu'),
    
    Flatten(),
    Dense(512),
    Activation('relu'),
  ]

if __name__ == '__main__':
  print('dlgo.network.small')


