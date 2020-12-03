from utils import *
import cv2

myDrone = initializeTello()
width, height = 360, 240

while True:
    #Flight
    if start == 0:
        myDrone.takeoff()
        start = 1
    # Step 1 get the frame and show the image
    img = telloGetFrame(myDrone, width, height)
    img, info = findFace(img)
    pError = trackFace(myDrone, info, width, pid, pError)
    cv2.imshow('Image', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break