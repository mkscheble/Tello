# from utlis import *
import cv2
from djitellopy import Tello
from time import sleep
def initializeTello():
    """connect to Tello, set velocities equal to zero, turn stream on"""
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone.left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print(myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone
def telloGetFrame(myDrone, w=360, h=240):
    """Get specific frames, and resize"""
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img
w, h = 360, 240
pid = [0.4, 0.4, 0]
pError = 0
startCounter = 0  # for no Flight 1   - for flight 0

myDrone = initializeTello()
count = 0
while True:

    ## Flight
    if startCounter == 0:
        myDrone.takeoff()
        startCounter = 1
        sleep(5)

    ## Step 1
    img = telloGetFrame(myDrone, w, h)
    # print(info[0][0])
    if count == 1:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 60
        myDrone.yaw_velocity = 0
        count = count + 1
        print(30)
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
        sleep(1)
    if count == 2:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = -60
        myDrone.yaw_velocity = 0
        count = 0
        print(-30)
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
        sleep(1)
    count = count + 1
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        myDrone.land()
        break