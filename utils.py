from djitellopy import Tello
import cv2
import numpy as np
from time import sleep
import time
""" Using djitellopy api for easy access to functions"""

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
    sleep(5)
    return myDrone


def telloGetFrame(myDrone, w=360, h=240):
    """Get specific frames, and resize"""
    myFrame = myDrone.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame, (w, h))
    return img


def findFace(img):
    """ Tracking face image, using cascade, how I originally set up the tracking but switched it to aruco codes
    left in just in case we need it"""

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 6)

    # arrays of faces detected/area of each face
    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:

        # create rectangle around detected faces
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])

    if len(myFaceListArea) != 0:
        # choosing largest face from detected faces
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        #if no faces detected just return images with zero info
        return img, [[0, 0], 0]


def trackFace(myDrone, info, w, pid, pid2, pid3, pError, pError2, pError3, dir):
    """PID controller implemented for moving forward, yaw_axis, and left right velocity
    To Do: need to implement up and down and I think we can use direction for that"""
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

    # This code is written for face detection, which is the info, need to change for aruco tags
    if info[0][0] != 0:
        myDrone.yaw_velocity = speed3
        myDrone.left_right_velocity = speed
        print(speed)
        if info[1] != 0:
            if speed2 < 0:
                myDrone.move_forward = speed2
            else:
                myDrone.move_back = speed2
            # print('s' + str(speed2) + '\n')
            # print('e' + str(error2)+ '\n')
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
    # return errors for previous errors and PID controller
    return error, error2, error3


def getDirection(img, info, specs):
    """This function gets the direction the drone needs to travel to center the current tracking item: right now face, will be aruco tag
    dir: 1 LEFT
    dir: 2 RIGHT
    dir: 3 UP
    dir: 4 DOWN"""
    cx = info[0][0]
    cy = info[0][1]
    frameWidth = specs[0]
    frameHeight = specs[1]
    deadZone = specs[2]
    dir = 0
    # Uncomment this is want to see grids on camera image, kinda gross to look at though
    # cv2.line(img, (int(frameWidth / 2) - deadZone, 0), (int(frameWidth / 2) - deadZone, frameHeight), (255, 255, 0), 3)
    # cv2.line(img, (int(frameWidth / 2) + deadZone, 0), (int(frameWidth / 2) + deadZone, frameHeight), (255, 255, 0), 3)
    # cv2.line(img, (0, int(frameHeight / 2) - deadZone), (frameWidth, int(frameHeight / 2) - deadZone), (255, 255, 0), 3)
    # cv2.line(img, (0, int(frameHeight / 2) + deadZone), (frameWidth, int(frameHeight / 2) + deadZone), (255, 255, 0), 3)
    if cx != 0 or cy != 0:
        if (cx < int(frameWidth / 2) - deadZone):
            cv2.putText(img, " GO LEFT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
            # Uncomment this code to see grid filled, kinda gross
            # cv2.rectangle(img, (0, int(frameHeight / 2 - deadZone)),
            #               (int(frameWidth / 2) - deadZone, int(frameHeight / 2) + deadZone), (0, 0, 255), cv2.FILLED)
            dir = 1
        elif (cx > int(frameWidth / 2) + deadZone):
            cv2.putText(img, " GO RIGHT ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
            # Uncomment this code to see grid filled, kinda gross
            # cv2.rectangle(img, (int(frameWidth / 2 + deadZone), int(frameHeight / 2 - deadZone)),
            #               (frameWidth, int(frameHeight / 2) + deadZone), (0, 0, 255), cv2.FILLED)
            dir = 2
        elif (cy < int(frameHeight / 2) - deadZone):
            cv2.putText(img, " GO UP ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
            # Uncomment this code to see grid filled, kinda gross
            # cv2.rectangle(img, (int(frameWidth / 2 - deadZone), 0),
            #               (int(frameWidth / 2 + deadZone), int(frameHeight / 2) - deadZone), (0, 0, 255), cv2.FILLED)
            dir = 3
        elif (cy > int(frameHeight / 2) + deadZone):
            cv2.putText(img, " GO DOWN ", (20, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 3)
            # Uncomment this code to see grid filled, kinda gross
            # cv2.rectangle(img, (int(frameWidth / 2 - deadZone), int(frameHeight / 2) + deadZone),
            #               (int(frameWidth / 2 + deadZone), frameHeight), (0, 0, 255), cv2.FILLED)
            dir = 4
    return img, dir

def dothething(myDrone):
    """This function will be the given command when we center our drone and have it the correct distance from the drone.
     Ultimately, this will be used to draw on the whiteboard."""
    myDrone.move_up(60)
    myDrone.move_right(60)

def findAruco(img):
    """Detects the aruco markers and returns a detected markers on image and the image."""

    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
    parameters = cv2.aruco.DetectorParameters_create()
    # have to set frame to something
    markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(img, dictionary, parameters=parameters)
    frame_markers = cv2.aruco.drawDetectedMarkers(img, markerCorners, markerIds)
    return img, frame_markers


def arucoAnalysis(arucoDict, frame, parameters, mtx, dist):
    # Detect and draw the markers in the image
    markerCorners, markerIDs, rejectedCandidates = cv2.aruco.detectMarkers(frame, arucoDict, parameters=parameters)
    cv2.aruco.drawDetectedMarkers(frame, markerCorners, markerIDs)

    # Detect marker pose
    rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(markerCorners, 0.05, mtx, dist)
    # print(rvec)
    # Scaling up translation for ease of reading
    try:
        tvec = tvec*100
    except:
        x = 3;

    if np.all(markerIDs != None):
        for marker_idx in range(0,len(markerIDs)):
            # Draw rotation axes and display translation
            cv2.aruco.drawAxis(frame, mtx, dist, rvec[marker_idx], tvec[marker_idx], 5)
            font = cv2.FONT_HERSHEY_SIMPLEX
            text = str([round(pos,2) for pos in tvec[marker_idx][0]])
            position = tuple(markerCorners[marker_idx][0][0])
            cv2.putText(frame, text, position, font, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

            # Record data
    #         textRecorder.write(str([rvec[marker_idx][0].tolist(), tvec[marker_idx][0].tolist(), markerIDs[marker_idx][0]]))
    #         if marker_idx < len(markerIDs)-1:
    #             textRecorder.write(',')
    # else:
    #         textRecorder.write(str([rvec, tvec]))
    # textRecorder.write("\n")

    return frame, markerIDs, rvec, tvec