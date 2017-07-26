import tensorflow as tf

params = {
    'inputs': tf.random_uniform([1, 3, 3, 3]),
    'filters': 1,
    'kernel_size': [3, 3],
    }

a = tf.layers.conv2d(**params)
with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  print sess.run(a)
