#!/usr/bin/env python

import numpy as np
import cv2
import time

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
camera = cv2.VideoCapture(0)
 
# allow the camera to warmup
#time.sleep(0.1)
 
# keep looping over the frames in the video
while True:
    # grab the current frame
    (grabbed, image) = camera.read()
    grabbed = camera.set(3,320)
    grabbed = camera.set(4,240)
    #image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces=detect_faces(image)
    print faces
    if len(faces) != 0:
        for (x,y,w,h) in faces:
            cv2.rectangle(image, (x, y), (x+w, y+h), 255)
            gray_smiles = image[y:y+h, x:x+w]
            smiles = detect_smiles(gray_smiles)
	    print "smile",smiles
            for (ex,ey,ew,eh) in smiles:
               cv2.rectangle(gray_smiles,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
               print "Sonrisa detectada"
            
        cv2.imwrite('detect.jpg', image)
        cv2.imshow("Frame", image) 		
    else:
        cv2.imshow("Frame", image)
    #cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
 

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

        # cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
