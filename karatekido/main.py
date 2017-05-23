from mss import mss
from PIL import Image
from datetime import datetime
from subprocess import Popen, PIPE
# import tensorflow as tf
import time
import cv2
import numpy as np
import random

b = 32
# def model(inp):
#     layers = [image]
#     layers.append(tf.layers.conv2d(layers[-1], b, 3, padding='same',
#         activation=tf.nn.relu))
#     layers.append(tf.layers.max_pooling2d(layers[-1], 2, 2))
#     layers.append(tf.layers.conv2d(layers[-1], b*2, 3, padding='same',
#         activation=tf.nn.relu))
#     layers.append(tf.layers.max_pooling2d(layers[-1], 2, 2))
#     layers.append(tf.layers.conv2d(layers[-1], b*4, 3, padding='same',
#         activation=tf.nn.relu))
#     layers.append(tf.layers.conv2d(layers[-1], b*8, 7, padding='valid',
#         activation=tf.nn.relu))
#     layers.append(tf.layers.conv2d(layers[-1], b*8, 1, padding='valid',
#         activation=tf.nn.relu))
#     layers.append(tf.layers.conv2d(layers[-1], 3, 1, padding='valid'))
#     logits = layers[-1]
#     logits = tf.squeeze(logits, [1, 2])
#     return logits

# def build_graph():
#     tf.placeholder`
#     tf.reset_default_graph()

def check_right_tree(img, tree_template):
    x, y = 1360, 604
    x_b, y_b = 50, 25
    tree = img[y-y_b:y+y_b, x-x_b:x+x_b, :]
    score = np.abs(np.sum(tree.astype(np.float32) -
        tree_template.astype(np.float32)))
    return score

def check_left_tree(img, tree_template):
    x, y = 1190, 604
    x_b, y_b = 50, 25
    tree = img[y-y_b:y+y_b, x-x_b:x+x_b, :]
    score = np.abs(np.sum(tree.astype(np.float32) -
        tree_template.astype(np.float32)))
    return score

def check_game_end(img, button_template):
    x, y = 1276, 929
    border = 70
    button = img[y-border:y+border, x-border:x+border, :]
    score = np.average(button - button_template)
    if score <= 1:
        return True
    else:
        return False

def make_move():
    n = random.randint(0, 2)
    if n == 0:
        print "LEFT"
        keypress("key Left ")
    elif n == 1:
        print "NOTHING"
        pass
    elif n == 2:
        print "RIGHT"
        keypress("key Right ")

delay = 0
threshold = 800000.0
def keypress(sequence):
    p = Popen(['xte'], stdin=PIPE)
    p.communicate(input=sequence)

def main():
    button_template = cv2.imread('button.png')
    left_template = cv2.imread('left_tree.png')
    right_template = cv2.imread('right_tree.png')
    count=0
    with mss() as sct:
        monitors = sct.enum_display_monitors()
        prev_left = 0
        prev_right = 0
        t = 0
        while True:
            start_t = time.time()
            sct.get_pixels(monitors[1])
            frame = Image.frombytes('RGB', (sct.width, sct.height), sct.image)
            frame = np.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            end_t = time.time()
            # print start_t-end_t
            game_end = check_game_end(frame, button_template)
            if game_end:
                print "Game Ended"
                time.sleep(1.0)
                keypress("mousemove 1276 929 ")
                time.sleep(1.0)
                keypress("mouseclick 1 ")
                time.sleep(1.0)
                keypress("mousemove 0 0 ")
                time.sleep(1.0)
                keypress("key Right ")
                keypress("key Right ")
            else:
                left_score = check_left_tree(frame, left_template)
                right_score = check_right_tree(frame, right_template)
                print left_score, right_score
                if left_score <= threshold and (t - prev_left) > 5:
                    print 'LEFT',
                    keypress("key Right ")
                    keypress("key Right ")
                    prev_left = t
                elif right_score <= threshold and (t - prev_right) > 5:
                    print 'RIGHT'
                    keypress("key Left ")
                    keypress("key Left ")
                    prev_right = t
            t += 1
            break
        cv2.imwrite('test.jpg', frame)
main()
# left_score = np.average(img[703:720, 738:808, :] - left)
# right_score = np.average(img[703:720, 858:928, :] - right)
# cv2.imwrite('left_cropped%d.jpg' %count, img[703:720, 738:808, :])
# cv2.imwrite('right_cropped%d.jpg'%count, img[703:720, 858:928, :])
# left = cv2.imread('left.jpg')[703:720, 738:808, :]
# right = cv2.imread('right.jpg')[703:720, 858:928, :]
# left = cv2.cvtColor(left, cv2.COLOR_BGR2RGB)
# right = cv2.cvtColor(right, cv2.COLOR_BGR2RGB)
# cv2.imwrite('left_cropped.jpg', left)
# cv2.imwrite('right_cropped.jpg', right)
