#!/usr/bin/env python

import numpy as np
import cv2


## Define cascade classifier to frontal face
def detect_gesture(image):

    haar_faces = cv2.CascadeClassifier("haarcascade_okaygesture.xml")
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=4, 
                minSize=(40,40), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected


##Inicialize camera
camera = cv2.VideoCapture(0)
i=1

# keep looping over the frames in the video
while True:
    # grab the current frame
    (grabbed, image) = camera.read()
    grabbed = camera.set(3,320)
    grabbed = camera.set(4,240)
    #frame=cv2.flip(frame,0)
           
    #convert color to gray
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image=image+image/4

    #function detect_face return coordinates if find a face
    faces=detect_gesture(image)
    if len(faces) != 0:
        for (x,y,w,h) in faces:
            pos_x=(x+w)/2
            pos_y=(y+h)/2
            print "Coordenadas en: %s,%s"%(pos_x, pos_y)
	    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("image",image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
