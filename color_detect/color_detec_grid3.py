#!/usr/bin/python
import cv2
import time
import colorsys
# OpenCV 3.0.1 in Ubuntu 16.04
from picamera.array import PiRGBArray
from picamera import PiCamera

## Inicialize camera
camera = PiCamera()
x=320
y=240
camera.resolution = (x , y)
        
# keep looping over the frames in the video
while True:
	   # grab the current frame
	   rawCapture = PiRGBArray(camera)
	   camera.capture(rawCapture, format="bgr")
	   frame = rawCapture.array
##           sumatorio=[0,0,0]
##           tabla_color=[0,0,0]
           color=[0,0,0]

##	   for i in range(1,11):
##	       tabla_color1=frame[x/2-3*i,y/2-3*i]
##	       tabla_color1=[tabla_color1[0]/4,tabla_color1[1]/4,tabla_color1[2]/4]
##	       tabla_color2=frame[x/2+3*i,y/2+3*i]
##	       tabla_color2=[tabla_color2[0]/4,tabla_color2[1]/4,tabla_color2[2]/4]
##	       tabla_color3=frame[x/2+3*i,y/2-3*i]
##	       tabla_color3=[tabla_color3[0]/4,tabla_color3[1]/4,tabla_color3[2]/4]
##               tabla_color4=frame[x/2-3*i,y/2+3*i]
##	       tabla_color4=[tabla_color4[0]/4,tabla_color4[1]/4,tabla_color4[2]/4]
####	       print tabla_color1
####	       print tabla_color2
####	       print tabla_color3
####	       print tabla_color4
####
####               print i
##               tabla_color[0]=(tabla_color1[0]+tabla_color2[0]+tabla_color3[0]+tabla_color4[0])
##               tabla_color[1]=(tabla_color1[1]+tabla_color2[1]+tabla_color3[1]+tabla_color4[1])
##               tabla_color[2]=(tabla_color1[2]+tabla_color2[2]+tabla_color3[2]+tabla_color4[2])
##               #print "tabla",tabla_color
##               sumatorio=[sumatorio[0]+tabla_color[0],sumatorio[1]+tabla_color[1],sumatorio[2]+tabla_color[2]]
##               print "sum",sumatorio
##	   tabla=[sumatorio[0]/10,sumatorio[1]/10,sumatorio[2]/10]
##
##           print tabla
##
##	   
##
##	   if (tabla[0]>100) and (tabla[1]>100) and (tabla[2]>100):
##                print "El color es blanco"
##           elif (tabla[0]<65) and (tabla[1]<65) and (tabla[2]<65):
##                print "El color es negro"
           if 1:
                sumatorioHSV=[0,0,0]
                frame=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
                colorA=frame[x/2-3*1,y/2-3*1]
                print "colorA",colorA
                for i in range(1,11):
                   color1=frame[x/2-3*i,y/2-3*i]
                   color1=[color1[0]/4,color1[1]/4,color1[2]/4]
                   color2=frame[x/2+3*i,y/2+3*i]
                   color2=[color2[0]/4,color2[1]/4,color2[2]/4]
                   color3=frame[x/2+3*i,y/2-3*i]
                   color3=[color3[0]/4,color3[1]/4,color3[2]/4]
                   color4=frame[x/2-3*i,y/2+3*i]
                   color4=[color4[0]/4,color4[1]/4,color4[2]/4]
                   color[0]=(color1[0]+color2[0]+color3[0]+color4[0])
                   color[1]=(color1[1]+color2[1]+color3[1]+color4[1])
                   color[2]=(color1[2]+color2[2]+color3[2]+color4[2])
                   sumatorioHSV=[sumatorioHSV[0]+color[0],sumatorioHSV[1]+color[1],sumatorioHSV[2]+color[2]]
                color_HSV=[sumatorioHSV[0]/10,sumatorioHSV[1]/10,sumatorioHSV[2]/10]
                print "HSV",color_HSV

	  	 
##           	 print "hsv",frame[x/2,y/2]
##		 tabla_color_HSV=frame[x/2,y/2]
##		 color_HSV=tabla_color_HSV[0]

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
cv2.destroyAllWindows()
