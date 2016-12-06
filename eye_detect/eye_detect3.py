#!/usr/bin/python
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
    
    haar_faces = cv2.CascadeClassifier("haarcascade_eye.xml")
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=4, 
                minSize=(10,10), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected

## Inicialize camera
camera = PiCamera()
camera.resolution = (640 , 480)

# keep looping over the frames in the video
while True:
           #convert color to gray
           rawCapture = PiRGBArray(camera)               
           camera.capture(rawCapture, format="bgr")
           frame = rawCapture.array
           # Convert color to gray
           image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
           #function detect_face return coordinates if find a face
           faces=detect_faces(image)
           #print faces
           if len(faces) != 0:
                 for (x,y,w,h) in faces:       			
       			pos_x=(x+w)/2
       			pos_y=(y+h)/2
       			print "Cara en: %s,%s"%(pos_x, pos_y)
       			cv2.rectangle(frame, (x, y), (x+w, y+h), 255)
			#function detect_eyes return coordinates if find a eye
       			roi_gray = image[y:y+h, x:x+w]    #crop the image to all face
			eyes = detect_eyes(roi_gray)

        		for (ex,ey,ew,eh) in eyes:
				   #  x1 and y1 are coordinates to first eye
				   x1=ex+x
				   y1=ey+y
				   print "Ojo 1 en: %s,%s"%(x1, y1)
				   
				   #  x2 and y2 are coordinates to second eye
				   x2=ex+ew+x
				   y2=ey+eh+y
				   print "Ojo 2 en: %s,%s"%(x2, y2)
				   
				   # Centroide
				   pos_x=(x1+x2)/2
				   pos_y=(y1+y2)/2
				   print "Centroide en: %s,%s"%(pos_x, pos_y)				   
				   # Left-Down corner
				   x_ld= pos_x-w/8
				   y_ld= pos_y+w/8
				   #Right-Up corner
    				   x_ru= pos_x+w/8
				   y_ru= pos_y-w/8
				   cv2.rectangle(frame, (x_ld, y_ld), (x_ru, y_ru), 255)  
				
        		cv2.imwrite('detect.jpg', frame)	   
           
           # Show the frame whatever there is a detection or not
           cv2.imshow("Image", frame)
           #  if the `q` key was pressed, break from the loop
           if cv2.waitKey(1) & 0xFF == ord('q'):
                break
 
# cleanup the camera and close any open windows
cv2.destroyAllWindows()
