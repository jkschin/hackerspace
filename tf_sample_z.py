import tensorflow as tf

z = tf.random_uniform([1,10], minval=-1, maxval=1)

sess = tf.Session()
for i in xrange(10):
  print sess.run(z)
