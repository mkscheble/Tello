from djitellopy import Tello
import cv2
import numpy as np


def initializeTello():
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
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img


def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 6)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(myDrone, info, w, pid, pid2, pid3, pError, pError2, pError3, dir):
    ## PID
    error = info[0][0] - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))
    # print(speed)
    # print('area: ' + str(info[1]) + "\n")

    #PID for forwards backwards
    error2 = info[1] - 10000
    speed2 = pid2[0] * error2 + pid2[1] * (error2 - pError2)
    speed2 = int(np.clip(speed2, -100, 100))

    # PID for yaw angle, slower than left right movement
    error3 = info[1] - 10000
    speed3 = pid3[0] * error3 + pid3[1] * (error3 - pError3)
    speed3 = int(np.clip(speed3, -100, 100))

    if info[0][0] != 0:
        myDrone.yaw_velocity = speed3
        myDrone.left_right_velocity = speed
        print(speed)
        if info[1] != 0:
            if speed2 < 0:
                myDrone.move_forward = speed2
            else:
                myDrone.move_back = speed2
            print('s' + str(speed2) + '\n')
            print('e' + str(error2)+ '\n')
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0
    if myDrone.send_rc_control:
        myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)
    return error, error2, error3


def getDirection(img, info, specs):
    cx = info[0][0]
    cy = info[0][1]
    frameWidth = specs[0]
    frameHeight = specs[1]
    deadZone = specs[2]

    cv2.line(img, (int(frameWidth / 2) - deadZone, 0), (int(frameWidth / 2) - deadZone, frameHeight), (255, 255, 0), 3)
    cv2.line(img, (int(frameWidth / 2) + deadZone, 0), (int(frameWidth / 2) + deadZone, frameHeight), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) - deadZone), (frameWidth, int(frameHeight / 2) - deadZone), (255, 255, 0), 3)
    cv2.line(img, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone), (255, 255, 0), 3)

    if (cx < int(frameWidth / 2) - deadZone):
        cv2.putText(img, " GO LEFT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.rectangle(img, (0, int(frameHeight / 2 - deadZone)),
                      (int(frameWidth / 2) - deadZone, int(frameHeight / 2) + deadZone), (0, 0, 255), cv2.FILLED)
        dir = 1
    elif (cx > int(frameWidth / 2) + deadZone):
        cv2.putText(img, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.rectangle(img, (int(frameWidth / 2 + deadZone), int(frameHeight / 2 - deadZone)),
                      (frameWidth, int(frameHeight / 2) + deadZone), (0, 0, 255), cv2.FILLED)
        dir = 2
    elif (cy < int(frameHeight / 2) - deadZone):
        cv2.putText(img, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.rectangle(img, (int(frameWidth / 2 - deadZone), 0),
                      (int(frameWidth / 2 + deadZone), int(frameHeight / 2) - deadZone), (0, 0, 255), cv2.FILLED)
        dir = 3
    elif (cy > int(frameHeight / 2) + deadZone):
        cv2.putText(img, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
        cv2.rectangle(img, (int(frameWidth / 2 - deadZone), int(frameHeight / 2) + deadZone),
                      (int(frameWidth / 2 + deadZone), frameHeight), (0, 0, 255), cv2.FILLED)
        dir = 4
    return img, dir

def dothething(myDrone):
    myDrone.move_up(60)
    myDrone.move_right(60)

