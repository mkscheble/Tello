from utils import *
import cv2
from writedata import *
from arucoTracking import *
from time import sleep
import time
dataQ = Queue()

# setting variables for width and height
# w, h = 360, 240 optional
w, h = 640, 480
deadZone = 100
"""pid controls left_right velocity, pid2 controls moving forward, pid3 controls yaw velocity"""
# if you have value over 120, image seems to buffer the frames and drone drifts off
pid = [120.0, 7.0, 0.1]
pid2 = [600.0, 5.0, 0.15]
pid3 = [120.0, 1.0, 0.15]

pidxs = [30.0, 2.0, 0.1]
pid2xs = [30.0, 2.0, 0.15]
pid3xs = [30.0, 1.0, 0.15]
# pError stands for previous error, used for PID controller
pError = 0
pError2 = 0
pError3 = 0
pErrorxs = 0
pError2xs = 0
pError3xs = 0

startCounter = 0  # 1 - No Flight, 0 Flight
specs = [w, h, deadZone]
# dir = 0
data = []
# sped = []
"""constants for aruco analysis, found from camera calibration done seperately, mtx is camera matrix"""
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
mtx = np.float32([[622.36525763, 0., 307.57777951],
                  [0., 621.76827265, 247.45519961],
                  [0., 0., 1.]])
dist = np.float32([[-4.09107478e-03, -7.38739614e-04, 1.68557817e-03, 1.16567623e-04, 1.34176960e-01]])

# initialize tello drone
myDrone = initializeTello()

# write to this file
myFile = 'data'
# create file
writeFileHeader(myFile)

# calls to velocity command, breaks if call it too much
speed = 0
speed2 = 0
speed3 = 0
frame = 0

iError = 0
iError2 = 0
iError3 = 0
iErrorxs = 0
iError2xs = 0
iError3xs = 0

boolean = True

start = time.time()
while True:

    # Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    # Step 1 - get the frame
    img = telloGetFrame(myDrone, w, h)
    if frame == 50:
        # img = telloGetFrame(myDrone, w, h)
        frame = 0
    else:
        frame = frame + 1
        continue

    # Step 2 - Track what is in frame
    """In our case we are using an aruco code"""
    # tracking face image, commented because we ain't using no face yuh
    # img, dir = getDirection(img, info, specs)
    # pError, pError2, pError3 = trackFace(myDrone, info, w, pid, pid2, pid3, pError, pError2, pError3, dir)

    # tracking aruco tag
    img, markers, twist = findAruco(arucoDict, img, parameters, mtx, dist)

    # Step 3 - Control, This is where we apply the error from where we want to be
    elapsed = time.time() - start
    if boolean:
        pError, pError2, pError3, speed, speed2, speed3, iError, iError2, iError3, boolean = trackAruco(myDrone, twist, pid,
                                                                                                        pid2, pid3, pError, pError2, pError3,
                                                                                                        iError, iError2, iError3, elapsed)
        if boolean == False:
            start = elapsed
    else:
        pError, pError2, pError3, speed, speed2, speed3, iError, iError2, iError3, boolean = trackAruco(myDrone, twist,
                                                                                                        pidxs, pid2xs, pid3xs,
                                                                                                        pErrorxs, pError2xs,
                                                                                                        pError3xs, iErrorxs,
                                                                                                        iError2xs,
                                                                                                        iError3xs,
                                                                                                        elapsed)
    # sped.append([twist[1],speed3])


    # Write data to queue
    data = []
    data.append(myDrone.get_height())
    data.append(elapsed)
    data.append(speed)
    data.append(speed2)
    data.append(speed3)
    data.append(pError)
    data.append(pError2)
    data.append(pError3)
    dataQ.put(data)

    # show the image, which is just the camera feed
    cv2.imshow('Camera Feed Tello', img)

    # Hold Q for 5 seconds and then the drone will land, need to be in image feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        # take data queue that we've been appending to and write to file
        appendtoFile(myFile, dataQ)
        cv2.destroyAllWindows()
        # print(sped)
        break

