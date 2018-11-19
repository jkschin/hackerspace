''' This is a generalised video frame grabber for video analytics. Most online
videos have a size of 1280 x 720, throwing millions of images of this size into
deep neural network is infeasible. Scaling it by 4x to a size of 320 x 180 makes
the training much more feasible. Scaling comes with issues as some videos do not
follow same aspect ratio.

To circumvent the scale problem, videos that do not fit the aspect ratio will be
scaled accordingly on one dimension, and then cropped 5 times: top left; bottom
left; top right; bottom right; centre.  '''
import numpy as np
import cv2
import os

ctr = 0
interval = 1
frame_out_width = 320
frame_out_height = 180

def write_frame(frame):
	cv2.imwrite(str(ctr) + ".jpg",frame)

def write(cap):
	global ctr
	width, height, fps 	= cap.get(3), cap.get(4), cap.get(5)
	ratio = min(height/float(frame_out_height),width/float(frame_out_width))
	print ("Width:%d\nHeight:%d\nFPS:%d\n" %(width,height,fps) )
	while(True):
		ret, frame = cap.read()
		if ret == False:
			break
		if (ctr % interval) == 0:
      frame = cv2.resize(
          frame,
          (int(round(width/ratio)),int(round(height/ratio))),
          interpolation=cv2.INTER_AREA)
			cv2.imwrite(str(ctr) + ".jpg", frame)
		ctr += 1

def main():
	directory = "/home/samuelchin/tensorflow/my_code/data/av8/"
	for d in os.listdir(directory):
		if d.endswith(".mp4"):
			cap = cv2.VideoCapture(os.path.join(directory,d))
			write(cap)

main()


