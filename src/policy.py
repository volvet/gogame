# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 12:50:43 2020

@author: Administrator
"""


import math
import os
import sys
import tensorflow as tf
from tensorflow.python.client import device_lib

import features
import go
import utils


def get_available_devices():
  devices = device_lib.list_local_devices()
  return [x.name for x in devices]

def get_available_cpus():
  devices = device_lib.list_local_devices()
  return [x.name for x in devices if x.device_type == 'CPU']

def get_available_gpus():
  devices = device_lib.list_local_devices()
  return [x.name for x in devices if x.device_type == "GPU"]


class PolicyNetwork(object):
  def __init__(self, features=features.DEFAULT_FEATURES, k=32, num_int_conv_layers=3, use_cpu=False):
    self.num_input_planes = sum(f.planes for f in features)
    self.k = k
    self.num_int_conv_layers = num_int_conv_layers
    self.test_summary_writer = None
    self.training_summary_writer = None
    self.test_stats = StatisticsCollector()
    self.training_stats = StatisticsCollector()
    self.session = tf.compat.v1.Session()
    tf.compat.v1.disable_v2_behavior()
    if use_cpu:
      with tf.device('/cpu:0'):
        self.setup_network()
    else:
      self.setup_network()
      
  def setup_network(self):
    global_step = tf.Variable(0, name='global_step', trainable=False)
    x = tf.compat.v1.placeholder(tf.float32, [None, go.N, go.N, self.num_input_planes])
    y = tf.compat.v1.placeholder(tf.float32, shape=[None, go.N**2])
    
    def _weight_variable(shape, name):
      number_inputs_added = utils.product(shape[:-1])
      stddev = 1/math.sqrt(number_inputs_added)
      return tf.Variable(tf.compat.v1.truncated_normal(shape, stddev=stddev), name=name)
   
    def _conv2d(x, W):
      return tf.nn.conv2d(x, W, strides=[1,1,1,1], padding='SAME')

    W_conv_init = _weight_variable([5, 5, self.num_input_planes, self.k], 'W_conv_init')
    h_conv_init = tf.nn.relu(_conv2d(x, W_conv_init), name='h_conv_init')
    
    W_conv_intermediate = []
    h_conv_intermediate = []
    _current_h_conv = h_conv_init
    for i in range(self.num_int_conv_layers):
      with tf.name_scope('layer'+str(i)):
        W_conv_intermediate.append(_weight_variable([3, 3, self.k, self.k], name='W_conv'))
        h_conv_intermediate.append(tf.nn.relu(_conv2d(_current_h_conv, W_conv_intermediate[-1]), name='h_conv'))
        _current_h_conv = h_conv_intermediate[-1]
    
    W_conv_final = _weight_variable([1, 1, self.k, 1], name='W_conv_final')
    b_conv_final = tf.Variable(tf.constant(0, shape=[go.N**2], dtype=tf.float32), name='b_conv_final')
    h_conv_final = _conv2d(h_conv_intermediate[-1], W_conv_final)
    logits = tf.reshape(h_conv_final, [-1, go.N**2]) + b_conv_final
    output = tf.nn.softmax(logits)
  
    log_likelihood_cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=y))
    train_step = tf.compat.v1.train.AdamOptimizer(1e-4).minimize(log_likelihood_cost, global_step=global_step)
    was_correct = tf.equal(tf.argmax(logits, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(was_correct, tf.float32))
    
    weight_summeries = tf.compat.v1.summary.merge([tf.compat.v1.summary.histogram(weight_var.name, weight_var)
                                        for weight_var in [W_conv_init] + W_conv_intermediate + [W_conv_final, b_conv_final]],
                                        name='weight_summaries')
    
    activation_summaries = tf.compat.v1.summary.merge([tf.compat.v1.summary.histogram(act_var.name, act_var)
                                        for act_var in [h_conv_init] + h_conv_intermediate + [h_conv_final]],
                                        name='activation_summaries')
    
    saver = tf.compat.v1.train.Saver()
    for name, thing in locals().items():
      if not name.startswith('_'):
        setattr(self, name, thing)
        
    #print(locals())

  def initialize_logging(self, tensorboard_logdir):
    self.test_summary_writer = tf.summary.FileWriter(os.path.join(tensorboard_logdir, 'test'), self.session.graph)
    self.training_summary_writer = tf.summary.FileWriter(os.path.join(tensorboard_logdir, 'training'), self.session.graph)

  def initialize_variables(self, save_file=None):
    self.session.run(tf.global_variables_initializer())
    if save_file is not None:
      self.saver.restore(self.session, save_file)

  def get_global_step(self):
    return self.session.run(self.global_step)

  def save_variables(self, save_file):
    if save_file is not None:
      print('Saving checkpoint to %s' % save_file, file=sys.stderr)
      self.saver.save(self.session, save_file)

  def train(self, training_data, batch_size=32):
    num_minibatches = training_data.data_size // batch_size

class StatisticsCollector(object):
  graph = tf.Graph()
  with tf.device('/cpu:0'), graph.as_default():
    accuracy = tf.compat.v1.placeholder(tf.float32, [])
    cost = tf.compat.v1.placeholder(tf.float32, [])
    accuracy_summary = tf.compat.v1.summary.scalar('accuracy', accuracy)
    cost_summary = tf.compat.v1.summary.scalar('log_likelihood_cost', cost)
    accuracy_summaries = tf.compat.v1.summary.merge([accuracy_summary, cost_summary], name='accuracy_summaries')
    
  session = tf.compat.v1.Session(graph=graph)
  
  def __init__(self):
    self.accuracies = []
    self.costs = []
    
  def report(self, accuracy, cost):
    self.accuracies.append(accuracy)
    self.cost.append(accuracy)
    
  def collect(self):
    avg_acc = sum(self.accuracies) / len(self.accuracies)
    avg_cost = sum(self.costs) / len(self.costs)
    self.accuracies = []
    self.costs = []
    summary = self.session.run(self.accuracy_summaries, feed_dict={self.accuracy:avg_acc, self.cost:avg_cost})
    return avg_acc, avg_cost, summary
    

if __name__ == '__main__':
  stats = StatisticsCollector()
  print(stats)
  net = PolicyNetwork()
  print(net)