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

y_a=480
a=0
coordenadas_ant=[0,0,0,0]

## Inicialize camera
camera = PiCamera()
camera.resolution = (320 , 240)

# initialize the first frame in the video stream
firstFrame = None
posicion = "nada"
posicion_anterior= "nada"
# loop over the frames of the video
while 1:

	# grab the current frame and initialize the occupied/unoccupied
	rawCapture = PiRGBArray(camera)
	camera.capture(rawCapture , format="bgr")
	frame = rawCapture.array

	# resize the frame, convert it to grayscale, and blur it
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
		pos_x=x+w/2
		pos_y=y+h/4
		print "movimiento en:",pos_x,pos_y
		if pos_x < 100:
			print "izquierda"
			posicion="izquierda"
		elif pos_x >540:
			print "derecha"
			posicion="derecha"
	 	elif pos_x >100 and pos_x<540:
			print "centro"
			posicion="centro"
		if (posicion_anterior=="centro"):
		    	print "giro"
		posicion_anterior=posicion

	# show the frame and record if the user presses a key
	#cv2.imshow("Security Feed", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key is pressed, break from the lop
	if key == ord("q"):
		break

# close any open windows
cv2.destroyAllWindows()
