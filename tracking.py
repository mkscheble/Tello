from utils import *
import cv2

myDrone = initializeTello()
width, height = 360, 240

while True:
    # Step 1 get the frame and show the image
    img = telloGetFrame(myDrone, width, height)
    cv2.imshow('Image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break