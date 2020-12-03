from utils import *
import cv2
from writedata import *
from time import sleep
import time
dataQ = Queue()

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
data = []


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
    ## Step 3
    pError, pError2, pError3 = trackFace(myDrone, info, w, pid, pid2, pid3, pError, pError2, pError3, dir)
    data = []
    data.append(myDrone.get_speed())
    data.append(myDrone.get_height())
    data.append(myDrone.get_flight_time())
    data.append(time.time())
    dataQ.put(data)

    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        appendtoFile(myFile, dataQ)
        cv2.destroyAllWindows()
        break
