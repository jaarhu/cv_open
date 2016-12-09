#!/usr/bin/python
# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import imutils
import cv2
import time
# OpenCV 3.0.1 in Ubuntu 16.04
from picamera.array import PiRGBArray
from picamera import PiCamera

# initialize the HOG descriptor/person detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

## Inicialize camera
camera = PiCamera()
camera.resolution = (640 , 480)

# keep looping over the frames in the video
while True:
        # grab the current frame and resize
        rawCapture = PiRGBArray(camera)
        camera.capture(rawCapture , format="bgr")
        frame = rawCapture.array
        image = imutils.resize(frame, width=min(640, frame.shape[1]))
        orig = image.copy()

        # detect people in the image
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4),padding=(8, 8), scale=1.05)

        # draw the original bounding boxes
        for (x, y, w, h) in rects:
                cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # apply non-maxima suppression to the bounding boxes using a
        # fairly large overlap threshold to try to maintain overlapping
        # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

        # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
                cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        # show some information on the number of bounding boxes
        print("[INFO] {}: {} original boxes, {} after suppression".format("frame", len(rects), len(pick)))

        # show the output images
        cv2.imshow("Before NMS", orig)
        cv2.imshow("After NMS", image)
        cv2.imwrite('detect.jpg', image)
        
        # If the `q` key was pressed, break from the loop        
        print("!!! Press 'q' now to quit")
        time.sleep(2)
        # If the `q` key was pressed, break from the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
                print("---> Press any key for the following video frame acquisition")
                cv2.waitKey(0)

# Close any open windows
cv2.destroyAllWindows()
 
