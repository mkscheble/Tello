from utils import *
import cv2
from writedata import *

w, h = 360, 240
pid = [0.4, 0.4, 0]
pError = 0
startCounter = 0  # for no Flight 1   - for flight 0

myDrone = initializeTello()
myFile = 'thisone'
writeFileHeader(myFile)

while True:

    ## Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1
    print('battery: ' + str(myDrone.get_battery()))
    ## Step 1
    img = telloGetFrame(myDrone, w, h)
    ## Step 2
    img, info = findFace(img)
    ## Step 3
    pError = trackFace(myDrone, info, w, pid, pError)
    appendtoFile(myFile, myDrone.get_speed(), myDrone.get_flight_time())
    
    # print(info[0][0])

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break