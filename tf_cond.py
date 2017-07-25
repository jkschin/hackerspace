import tensorflow as tf
import random

global_step = tf.Variable(0, trainable=False)
condition = tf.placeholder(tf.bool)
a = tf.cond(condition, lambda: tf.assign_add(global_step, 1),
    lambda: tf.assign_add(global_step, 1))
print a
sess = tf.Session()
sess.run(tf.global_variables_initializer())
for i in xrange(100):
  sess.run([a, global_step],feed_dict={condition: random.randint(0, 1)})
