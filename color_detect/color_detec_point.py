#!/usr/bin/python
import cv2
import time
import colorsys
#from SimpleCV import Image

x=320
y=240
rojo=0
azul=0
verde=0

camera = cv2.VideoCapture(0)
        
# keep looping over the frames in the video
while True:
	   # grab the current frame
	   (grabbed, frame) = camera.read()
	   grabbed = camera.set(3,x)
	   grabbed = camera.set(4,y)
           print "bgr",frame[x/2,y/2]
	   tabla_color=frame[x/2,y/2]
	   if (tabla_color[0]>100) and (tabla_color[1]>100) and (tabla_color[2]>100):
                print "El color es blanco"
           elif (tabla_color[0]<65) and (tabla_color[1]<65) and (tabla_color[2]<65):
                print "El color es negro"
           else:
	  	 frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
           	 print "hsv",frame[x/2,y/2]
		 color_HSV=frame[x/2,y/2]
          	 if (color_HSV[1] > 57) and (color_HSV[2] > 49) :
                    if (color_HSV[0] > 152) and (color_HSV[0] < 197) :
                        print "El color es rojo"
                    elif (color_HSV[0] >= 15) and (color_HSV[0] < 49) and (color_HSV[1]>200):
                        print "El color es amarillo"
                    elif (color_HSV[0] > 49) and (color_HSV[0] < 80):
                        print "El color es verde"
                    elif (color_HSV[0] >= 80) and (color_HSV[0] < 129):
                        print "El color es azul"
                 else:
                    print "No distingo el color"
               
            #Mostramos la imagen
           cv2.imshow('frame',frame)
             
            #con la tecla 'q' salimos del programa
           if cv2.waitKey(1) & 0xFF == ord('q'):
                break
         
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
