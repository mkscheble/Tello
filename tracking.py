from utils import *
import cv2
from writedata import *
from time import sleep
import time
dataQ = Queue()

# setting variables for width and height
# w, h = 360, 240 optional
w, h = 640, 480
deadZone = 100
"""pid controls left_right velocity, pid2 controls moving forward, pid3 controls yaw velocity"""
pid = [0.001, 0.001, 0]
pid2 = [0.001, 0.001, 0]
pid3 = [0.001, 0.001, 0]

# pError stands for previous error, used for PID controller
pError = 0
pError2 = 0
pError3 = 0
startCounter = 1  # 1 - No Flight, 0 Flight
specs = [w, h, deadZone]
dir = 0
data = []

"""constants for aruco analysis, found from camera calibration done seperately, mtx is camera matrix"""
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
mtx = np.float32([[620.52798302, 0.0, 294.40771497],
                  [0.0, 621.57625105, 268.77465391],
                  [0.0, 0.0, 1.0]])
dist = np.float32([[0.0237036, -0.13064133, 0.01268512, -0.00664866, 0.27907396]])

# initialize tello drone
myDrone = initializeTello()

# write to this file
myFile = 'datacollection'
# create file
writeFileHeader(myFile)


while True:

    # Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    # Step 1 - get the frame
    img = telloGetFrame(myDrone, w, h)

    # Step 2 - Track what is in frame
    """In our case we are using an aruco code"""
    img, info = findFace(img)
    img, dir = getDirection(img, info, specs)
    img, markers, twist, position = findAruco(arucoDict, img, parameters, mtx, dist)
    # print(twist)
    # Step 3 - Control, This is where we apply the error from where we want to be
    pError, pError2, pError3 = trackFace(myDrone, info, w, pid, pid2, pid3, pError, pError2, pError3, dir)


    # Write data to queue
    data = []
    data.append(myDrone.get_speed())
    data.append(myDrone.get_height())
    data.append(myDrone.get_flight_time())
    data.append(time.time())
    dataQ.put(data)


    # show the image, which is just the camera feed
    cv2.imshow('Camera Feed Tello', img)

    # Hold Q for 5 seconds and then the drone will land, need to be in image feed
    if cv2.waitKey(5) & 0xFF == ord('q'):
        myDrone.land()
        # take data queue that we've been appending to and write to file
        appendtoFile(myFile, dataQ)
        cv2.destroyAllWindows()
        break
