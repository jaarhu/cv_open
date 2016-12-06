#!/usr/bin/env python

import numpy as np
import cv2
import time
# OpenCV 3.0.1 in Ubuntu 16.04
from picamera.array import PiRGBArray
from picamera import PiCamera

def detect_faces(image):
    
    haar_faces = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    detected = haar_faces.detectMultiScale(image,  scaleFactor=1.3, 
                minNeighbors=4,  
                minSize=(30,30), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected

def detect_smiles(image):
    haar_faces = cv2.CascadeClassifier('haarcascade_smile.xml')
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=5, 
                minSize=(20, 20),
                maxSize=(100,100),
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected
 
## Inicialize camera
camera = PiCamera()
camera.resolution = (640 , 480)
 
# keep looping over the frames in the video
while True:
    # grab the current frame
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture , format="bgr")
    frame = rawCapture.array
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces=detect_faces(image)
    print faces
    if len(faces) != 0:
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), 255)
            gray_smiles = frame[y:y+h, x:x+w]
            smiles = detect_smiles(gray_smiles)
	    print "smile",smiles
            for (ex,ey,ew,eh) in smiles:
               cv2.rectangle(gray_smiles,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
               print "Sonrisa detectada"
        cv2.imwrite('detect.jpg', frame)
 		
    cv2.imshow("Imagen", frame)
    
    
    # if the `q` key was pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup the camera and close any open windows
cv2.destroyAllWindows()
