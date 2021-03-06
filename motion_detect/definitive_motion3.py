#!/usr/bin/python
# import the necessary packages
import argparse
import datetime
import imutils
import time
import cv2
# OpenCV 3.0.1 in Ubuntu 16.04
from picamera.array import PiRGBArray
from picamera import PiCamera

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
args = vars(ap.parse_args())


y_a=240
a=0
coordenadas_ant=[0,0,0,0]

## Inicialize camera
camera = PiCamera()
#camera.resolution = (320 , 240)

# if the video argument is None, then we are reading from webcam
if args.get("video", None) is None:
	rawCapture = PiRGBArray(camera)
	camera.capture(rawCapture , format="bgr")
	frame = rawCapture.array

# otherwise, we are reading from a video file
else:
	camera = cv2.VideoCapture(args["video"])

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video
while True:
	# grab the current frame and initialize the occupied/unoccupied
	rawCapture = PiRGBArray(camera)
	camera.capture(rawCapture , format="bgr")
	frame = rawCapture.array

	# if the frame could not be grabbed, then we have reached the end
	# of the video
	#if not grabbed:
	#	break

	# resize the frame, convert it to grayscale, and blur it
	frame = imutils.resize(frame, width=500)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray, (21, 21), 0)

	# if the first frame is None, initialize it
	if firstFrame is None:
		firstFrame = gray
		continue
	# compute the absolute difference between the current frame and
	# first frame
	frameDelta = cv2.absdiff(firstFrame, gray)
	thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
	firstFrame=gray
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
	thresh = cv2.dilate(thresh, None, iterations=2)
	(_,cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	# loop over the contours
	for c in cnts:
		
		# if the contour is too small, ignore it
		if cv2.contourArea(c) < 8000:
			continue
		a=1
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
		(x, y, w, h) = cv2.boundingRect(c)
		if(y_a>=y):
			coordenadas=cv2.boundingRect(c)
		
	if a==1 and coordenadas_ant != coordenadas:
		(x,y,w,h) = coordenadas
		coordenadas_ant=coordenadas
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		#print "rectangulo:",x,w,y,h
		cord_x=x+w/2
		cord_y=y+h/4
		print "movimiento en:",cord_x,cord_y
		cv2.rectangle(frame, (cord_x, cord_y), (cord_x + 2, cord_y + 2), (255, 0, 0), 2)

	# show the frame and record if the user presses a key
	cv2.imshow("Security Feed", frame)
	cv2.imshow("Thresh", thresh)
	cv2.imshow("Frame Delta", frameDelta)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# close any open windows
cv2.destroyAllWindows()
