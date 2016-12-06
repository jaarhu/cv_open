#!/usr/bin/env python

import cv2
# OpenCV 3.0.1 in Ubuntu 16.04
from picamera.array import PiRGBArray
from picamera import PiCamera

## Define cascade classifier to frontal face
def detect_gesture(image):

    haar_faces = cv2.CascadeClassifier("haarcascade_okaygesture.xml")
    detected = haar_faces.detectMultiScale(image, scaleFactor=1.3, 
                minNeighbors=4, 
                minSize=(40,40), 
                flags=cv2.CASCADE_SCALE_IMAGE)
    
    return detected


##Inicialize camera
camera = PiCamera()
camera.resolution = (640 , 480)

# keep looping over the frames in the video
while True:
    # grab the current frame
    rawCapture = PiRGBArray(camera)
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array
    #frame=cv2.flip(frame,0)
           
    #convert color to gray
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  
    #function detect_face return coordinates if find a face
    faces=detect_gesture(image)
    if len(faces) != 0:
        for (x,y,w,h) in faces:
            pos_x=(x+w)/2
            pos_y=(y+h)/2
            print "Coordenadas en: %s,%s"%(pos_x, pos_y)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
        cv2.imwrite('detect.jpg', frame)
    cv2.imshow("Imagen" , frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
# cleanup the camera and close any open windows
cv2.destroyAllWindows()
