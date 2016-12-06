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

def detect_profilefaces(image):
    
    haar_faces = cv2.CascadeClassifier('haarcascade_profileface.xml')
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=4, 
                minSize=(30,30), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected

## Inicialize camera
camera = PiCamera()
camera.resolution = (640 , 480)
#camera.framerate = 32

# keep looping over the frames in the video
while True:
    # grab the current frame
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture , format="bgr")
    frame = rawCapture.array
    # Convert color to gray
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces=detect_faces(image)

    if len(faces) != 0:
        for (x,y,w,h) in faces:
            pos_x=(x+w)/2
            pos_y=(y+h)/2
            print "Cara en: %s,%s"%(pos_x, pos_y)
            cv2.rectangle(frame, (x, y), (x+w, y+h), 255)

        cv2.imwrite('detect.jpg', frame)
    else:
        faces=detect_profilefaces(image)
        if len(faces) != 0:
            for (x,y,w,h) in faces:
                pos_x=(x+w)/2
                pos_y=(y+h)/2
                print "Perfil en: %s,%s"%(pos_x, pos_y)
                cv2.rectangle(frame, (x, y), (x+w, y+h), 255)

            cv2.imwrite('detect.jpg', frame)

    # Show the frame whatever there is a detection or not
    cv2.imshow("Image", frame)
    # Clear the stream in preparation for the next frame
    #rawCapture.truncate(0)
    # If the `q` key was pressed, break from the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup the camera and close any open windows
cv2.destroyAllWindows()

