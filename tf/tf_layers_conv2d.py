import tensorflow as tf

b = tf.random_uniform([10, 10, 10, 10])
print b.shape
print b.get_shape()[0]
params = {
    'inputs': tf.random_uniform([1, 3, 3, 3]),
    'filters': b.get_shape()[0],
    'kernel_size': [3, 3],
    }

a = tf.layers.conv2d(**params)
print a.shape
with tf.Session() as sess:
  sess.run(tf.global_variables_initializer())
  print sess.run(a)
