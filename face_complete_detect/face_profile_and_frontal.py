#!/usr/bin/env python

import numpy as np
import argparse
import cv2

## Define cascade classifier to frontal face
def detect_faces(image):
    
    haar_faces = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=4, 
                minSize=(30,30), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected

def detect_profilefaces(image):
    
    haar_faces = cv2.CascadeClassifier('haarcascade_profileface.xml')
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=4, 
                minSize=(30,30), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected

## Inicialize camera
camera = cv2.VideoCapture(0)

# keep looping over the frames in the video
while True:
   # grab the current frame
    (grabbed, image) = camera.read()
    grabbed = camera.set(3,320)
    grabbed = camera.set(4,240)
   
   #convert color to gray

    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
   # image=image+image/4
    faces=detect_faces(image)

    if len(faces) != 0:
        for (x,y,w,h) in faces:
            pos_x=(x+w)/2
            pos_y=(y+h)/2
            print "Cara en: %s,%s"%(pos_x, pos_y)
            cv2.rectangle(image, (x, y), (x+w, y+h), 255)

        cv2.imwrite('detect.jpg', image)
        cv2.imshow("Image", image)
    else:
        faces=detect_profilefaces(image)
        if len(faces) != 0:
            for (x,y,w,h) in faces:
                pos_x=(x+w)/2
                pos_y=(y+h)/2
                print "Perfil en: %s,%s"%(pos_x, pos_y)
                cv2.rectangle(image, (x, y), (x+w, y+h), 255)

            cv2.imwrite('detect.jpg', image)
            cv2.imshow("Image", image)
        else:
            cv2.imshow("Image", image)
    #cv2.imshow('frame', stream.array)
    key = cv2.waitKey(1) & 0xFF
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()

