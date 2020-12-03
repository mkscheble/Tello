from utils import *
import cv2
from writedata import *
from time import sleep
import time
dataQ = Queue()
stateQ = LifoQueue()
#testing
# w, h = 360, 240
w, h = 640, 480
deadZone = 100
pid = [0.01, 0.01, 0]
pid2 = [0.01, 0.01, 0]
pid3 = [0.001, 0.001, 0]
pError = 0
pError2 = 0
pError3 = 0
startCounter = 1  # for no Flight 1   - for flight 0
specs = [w, h, deadZone]
dir = 0


myDrone = initializeTello()
myFile = 'thisone'
writeFileHeader(myFile)

while True:

    ## Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1
    # print('battery: ' + str(myDrone.get_battery()))
    ## Step 1
    img = telloGetFrame(myDrone, w, h)
    ## Step 2
    img, info = findFace(img)
    img, dir = getDirection(img, info, specs)
    print('direction')
    print(dir)
    ## Step 3
    pError, pError2, pError3 = trackFace(myDrone, info, w, pid, pid2, pid3, pError, pError2, pError3, dir)
    appendtoFile(myFile, myDrone.get_speed(), myDrone.get_flight_time())


    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        cv2.destroyAllWindows()
        break