#!/usr/bin/python
import numpy as np
import cv2
# OpenCV 3.0.1 in Ubuntu 16.04
from picamera.array import PiRGBArray
from picamera import PiCamera

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

eye_cascade = cv2.CascadeClassifier('Nariz_nuevo.xml') 
i=0

## Inicialize camera
camera = PiCamera()
camera.resolution = (640 , 480)
 
while(True):
    #leemos un frame y lo guardamos
    # Take a frame
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    img = rawCapture.array
    # Convert color to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
	print eyes
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(img,(x+ex,y+ey),(x+ex+ew,y+ey+eh),(0,255,0),2)
    cv2.imwrite('detect.jpg',img)
        
    #Mostramos la imagen
    cv2.imshow('img',img)
         
    #con la tecla 'q' salimos del programa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2-destroyAllWindows()
