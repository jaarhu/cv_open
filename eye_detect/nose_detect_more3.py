#!/usr/bin/env python

import numpy as np
import argparse
import cv2
# OpenCV 3.0.1 in Ubuntu 16.04
from picamera.array import PiRGBArray
from picamera import PiCamera

## Define cascade classifier to frontal face
def detect_faces(image):
    
    haar_faces = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=4, 
                minSize=(30,30), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected

## Define cascade classifier to frontal face
def detect_eyes(image):
    
    haar_faces = cv2.CascadeClassifier("Nariz.xml")
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=3, 
                minSize=(5,5), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected

## Inicialize camera
camera = PiCamera()
camera.resolution = (640 , 480)
i=1

# keep looping over the frames in the video
while True:	   
           # grab the current frame
           rawCapture = PiRGBArray(camera)
           camera.capture(rawCapture, format="bgr")
           frame = rawCapture.array           	   
           #convert color to gray
           image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
           cv2.imshow('Imagen',frame)
           #function detect_face return coordinates if find a face            
           faces=detect_faces(image)
           
           if len(faces) != 0:
                 for (x,y,w,h) in faces:
       			roi_gray = image[y:y+h, x:x+w]    #crop the image to all face
			cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
			#function detect_eyes return coordinates if find a eye       		
			eyes = detect_eyes(roi_gray)
			print eyes
			i=1  #to look for two eyes
        		for (ex,ey,ew,eh) in eyes:
				#print eyes
				cv2.rectangle(image,(ex-2,ey-2),(ex+2,ey+2),(0,255,0),2)	

           if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
# cleanup the camera and close any open windows
cv2.destroyAllWindows()
