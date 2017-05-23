from mss import mss
from PIL import Image
from datetime import datetime
from subprocess import Popen, PIPE
import tensorflow as tf
import time
import cv2
import numpy as np

b = 32
def model(inp, b):
    layers = [image]
    layers.append(tf.layers.conv2d(layers[-1], b, 3, padding='same',
        activation=tf.nn.relu))
    layers.append(tf.layers.max_pooling2d(layers[-1], 2, 2))
    layers.append(tf.layers.conv2d(layers[-1], b*2, 3, padding='same',
        activation=tf.nn.relu))
    layers.append(tf.layers.max_pooling2d(layers[-1], 2, 2))
    layers.append(tf.layers.conv2d(layers[-1], b*4, 3, padding='same',
        activation=tf.nn.relu))
    layers.append(tf.layers.conv2d(layers[-1], b*8, 7, padding='valid',
        activation=tf.nn.relu))
    layers.append(tf.layers.conv2d(layers[-1], b*8, 1, padding='valid',
        activation=tf.nn.relu))
    layers.append(tf.layers.conv2d(layers[-1], 3, 1, padding='valid'))
    logits = layers[-1]
    logits = tf.squeeze(logits, [1, 2])
    return logits



# policy gradient methods
print "SLEEPING FOR 3 SECONDS"
# time.sleep(3)
def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)

left = cv2.imread('left.jpg')[703:720, 738:808, :]
right = cv2.imread('right.jpg')[703:720, 858:928, :]
left = cv2.cvtColor(left, cv2.COLOR_BGR2RGB)
right = cv2.cvtColor(right, cv2.COLOR_BGR2RGB)
cv2.imwrite('left_cropped.jpg', left)
cv2.imwrite('right_cropped.jpg', right)
count=0
with mss() as sct:
    monitors = sct.enum_display_monitors()
    while True:
        sct.get_pixels(monitors[2])
        img = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
        img = np.array(img)
        left_score = np.average(img[703:720, 738:808, :] - left)
        right_score = np.average(img[703:720, 858:928, :] - right)
        cv2.imwrite('left_cropped%d.jpg' %count, img[703:720, 738:808, :])
        cv2.imwrite('right_cropped%d.jpg'%count, img[703:720, 858:928, :])
        count += 1
        print left_score, right_score
        # if left_score < right_score:
        #     print "RIGHT"
        #     keypress('key Right ')
        #     time.sleep(0.1)
        #     keypress('key Right ')
        # else:
        #     print "LEFT"
        #     keypress('key Left ')
        #     time.sleep(0.1)
        #     keypress('key Left ')
        # img.save('raw2.jpg'.format(str(datetime.now())))
        end = time.time()
        time.sleep(0.5)
        # print end-start
