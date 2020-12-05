import os
import numpy as np
import cv2
import cv2.aruco as aruco
from utils import *
from time import sleep

def calibrate():
    myDrone = initializeTello()
    # cap = cv2.VideoCapture(0)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    # checkerboard of size (9 x 7) is used
    objp = np.zeros((7*9,3), np.float32)
    #adding the 1.8669 gives us our translation vectiors in centimeters
    objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2) * 1.8669

    # arrays to store object points and image points from all the images.
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    count = 0
    while(True):
        # Capture frame-by-frame
        frame = telloGetFrame(myDrone, 640, 480)
        # ret, frame = cap.read()
        # # resizing for faster detection
        # frame = cv2.resize(frame, (640, 480))
        # using a greyscale picture, also for faster detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (9,7), None)

        # If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)
            print(count)
            count = count + 1
            # Draw and display the corners
            cv2.drawChessboardCorners(frame, (9,7), corners, ret)
            sleep(2)
            # print('found')
            #write_name = 'corners_found'+str(idx)+'.jpg'

        # Display the resulting frame
        cv2.imshow('Calibration',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # cap.release()
    print('here')
    cv2.destroyAllWindows()
    cv2.waitKey(10)
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    print(ret, mtx, dist, rvecs, tvecs)
    fileout = open('calibration.txt','w')
    print('open')
    fileout.close()
    fileout = open('calibration.txt', 'a')
    fileout.write('ret: ' + str(ret) + '\n')
    fileout.write('mtx: ' + str(mtx) + '\n')
    fileout.write('dist: ' + str(dist) + '\n')
    fileout.write('rvecs: ' + str(rvecs) + '\n')
    fileout.write('tvecs:' + str(tvecs) + '\n')
    print('close')
    fileout.close()
calibrate()


# objp = np.zeros((7*9,3), np.float32)
# objp[:,:2] = np.mgrid[0:9,0:7].T.reshape(-1,2) *1.8669
# print(objp)
