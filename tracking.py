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
pid = [120.0, 7.0, 0.001]
pid2 = [600.0, 5.0, 0.0015]
pid3 = [20.0, 5.0, 0.005]

pidxs = [42.0, 10.0, 0.005]
pid2xs = [65.0, 15.0, 0.005]
pid3xs = [7.0, 10.0, 0.004]
# pError stands for previous error, used for PID controller
pError = 0
pError2 = 0
pError3 = 0
pErrorxs = 0
pError2xs = 0
pError3xs = 0

startCounter = 0  # 1 - No Flight, 0 Flight
specs = [w, h, deadZone]
data = []
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

bigtag = 9
liltag = 50
boolean = True
framerate = 50
second = 0
start = time.time()
count = 0
while True:

    # Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1

    # Step 1 - get the frame
    img = telloGetFrame(myDrone, w, h)
    if frame == framerate:
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
    img, markerCorners, markerIDs, twist = findAruco(arucoDict, img, parameters, mtx, dist)
    # print(twist)
    # Step 3 - Control, This is where we apply the error from where we want to be
    elapsed = time.time() - start - second
    if boolean:
        if np.all(markerIDs) != None:
            if [bigtag] in markerIDs and np.all(twist) != None:
                ind = np.where(markerIDs == [bigtag])
                tvec = twist[1][ind][0]
                pError, pError2, pError3, speed, speed2, speed3, iError, iError2, iError3, boolean = trackAruco(myDrone, tvec, pid,
                                                                                                            pid2, pid3, pError, pError2, pError3,
                                                                                                            iError, iError2, iError3, elapsed)
            if boolean == False:
                if count == 10:
                    print('the cat is out of the bag \n')
                    pError, pError2, pError3 = 0, 0, 0
                    second = elapsed
                    framerate = 20
                    dataQ.put('\nsplit\n')
                    count = 0
                else:
                    count = count +1
                    boolean = True
    else:
        print('small pid')
        if np.all(markerIDs) != None:
            if [liltag] in markerIDs and np.all(twist) != None:
                ind = np.where(markerIDs == [liltag])
                tvec = twist[1][ind][0]
                pErrorxs, pError2xs, pError3xs, speed, speed2, speed3, iErrorxs, iError2xs, iError3xs = trackArucoSmall(myDrone, tvec,
                                                                                                        pidxs, pid2xs, pid3xs,
                                                                                                        pErrorxs, pError2xs,
                                                                                                        pError3xs, iErrorxs,
                                                                                                        iError2xs,
                                                                                                        iError3xs,
                                                                                                        elapsed)
                count = 0
            if np.abs(pErrorxs) < 0.1 and np.abs(pError2xs) < 0.1 and np.abs(pError3xs) < 0.04 \
                    and pErrorxs != 0 and pError2xs != 0 and pError3xs != 0:
                print('doing the thing accurate one')
                dothething(myDrone, -45, 35)
                dothething(myDrone, 33, -30)
                moveback(myDrone)
                myDrone.land()
                # take data queue that we've been appending to and write to file
                appendtoFile(myFile, dataQ)
                cv2.destroyAllWindows()
                break
        else:
            if count == 15:
                print('i gotta land')
                if np.abs(pErrorxs) < 0.15 and np.abs(pError2xs) < 0.15 and pError3xs < 0.06 \
                        and pErrorxs != 0 and pError2xs != 0 and pError3xs != 0:
                    print('doing the thing lat chance throw')
                    dothething(myDrone, -45, 35)
                    dothething(myDrone, 33, -27)
                    moveback(myDrone)
                myDrone.land()
                # take data queue that we've been appending to and write to file
                appendtoFile(myFile, dataQ)
                cv2.destroyAllWindows()
                break
            else:
                count = count + 1
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
    data.append(pErrorxs)
    data.append(pError2xs)
    data.append(pError3xs)
    dataQ.put(data)

    # show the image, which is just the camera feed
    cv2.imshow('Camera Feed Tello', img)

    # Hold Q for 5 seconds and then the drone will land, need to be in image feed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        # take data queue that we've been appending to and write to file
        appendtoFile(myFile, dataQ)
        cv2.destroyAllWindows()
        break

