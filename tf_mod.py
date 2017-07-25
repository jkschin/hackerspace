import tensorflow as tf

i = tf.placeholder(tf.int32)
a = tf.mod(i, 6)
sess = tf.Session()
sess.run(tf.global_variables_initializer())
for j in xrange(200):
  print sess.run(a, feed_dict={i: j})
