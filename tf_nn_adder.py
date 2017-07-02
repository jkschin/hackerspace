import numpy as np
import tensorflow as tf
import time
from collections import defaultdict

total_samples = 1000000
batch_size = 10000
epochs = 100
steps = total_samples / batch_size
num_features = 10
base_lr = 0.01
data_features = np.random.rand(total_samples, num_features)
data_labels = np.sum(data_features, axis=1)

WEIGHTS = 0
BIASES = 1
PREDICTIONS = 2
LOSSES = 3
W_GRADIENTS = 4
B_GRADIENTS = 5

def train():
  nested_dict = lambda: defaultdict(nested_dict)
  output_dict = nested_dict()
  graph = tf.Graph()
  with graph.as_default():
    global_step = tf.Variable(0, trainable=False)
    features = tf.placeholder(tf.float32, shape=[batch_size, num_features])
    labels = tf.placeholder(tf.float32, shape=[batch_size])
    w = tf.get_variable('weights', shape=[num_features, 1])
    b = tf.get_variable('bias', shape=[1])
    predictions = tf.squeeze(tf.matmul(features, w) + b)
    loss = tf.reduce_mean(tf.square(predictions - labels))
    gradients = tf.gradients(loss, [w, b])
    lr = tf.train.exponential_decay(base_lr, global_step, steps*10, 0.96,
        staircase=True)
    weights_op = tf.assign_sub(w, lr * gradients[0])
    bias_op = tf.assign_sub(b, lr * gradients[1])
    add_op = tf.assign_add(global_step, 1)
    train_op = tf.group(weights_op, bias_op, add_op)
    init_op = tf.global_variables_initializer()
  sess = tf.Session(graph=graph)
  sess.run(init_op)
  for j in xrange(epochs):
    for k in xrange(steps):
      s_idx = k * batch_size
      e_idx = s_idx + batch_size
      run_vals = sess.run(
          [ w,
            b,
            predictions,
            loss,
            gradients[0],
            gradients[1],
            lr,
            train_op],
          feed_dict = { features: data_features[s_idx: e_idx],
                        labels: data_labels[s_idx: e_idx]})
      print '''
Epoch: %d Step: %d
Weights:
%s
Biases: %s
Loss: %f
Learning Rate: %f
            ''' \
            %(j, k, run_vals[0], run_vals[1], run_vals[3], run_vals[6])
      if j == 0 and k == 0:
        time.sleep(10)
      for l, l_val in enumerate(run_vals):
        output_dict[j][k][l] = np.array(l_val)
  sess.close()
  return output_dict

if __name__ == '__main__':
  output_dict = train()


