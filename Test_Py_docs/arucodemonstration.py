import cv2
import numpy as np

# dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
#
# markerImage = np.zeros((200, 200), dtype=np.uint8)
# markerImage = cv2.aruco.drawMarker(dictionary, 33, 200, markerImage, 1)
# # cv2.imwrite("marker33.png", markerImage)
# img = cv2.imread('IMG_1597.jpg')
# img = cv2.resize(img, (640, 480))
# cv2.imshow("marker", img)
# cv2.waitKey()

##detecting markers

# dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
# parameters = cv2.aruco.DetectorParameters_create()
# #have to set frame to something
# markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(img, dictionary, parameters = parameters)
# frame_markers = cv2.aruco.drawDetectedMarkers(img.copy(), markerCorners, markerIds)
# print(markerIds)
# cv2.imshow('markers', frame_markers)
# cv2.waitKey()

from visionProcessing import *
from utils import *

# myDrone = initializeTello()
w, h = 640, 480
arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
mtx = np.float32([[616.86563666, 0., 321.92615976],
                  [0., 615.33126089, 236.21885561],
                  [0., 0., 1.]])
dist = np.float32([[-0.00803506, 0.00767694, -0.0028638, 0.00770982, 0.10991234]])

img = cv2.imread(r'C:\Users\ad\Desktop\Tello\images\IMG_1597.jpg')
img = cv2.resize(img, (640, 480))
img, markers, twist, position = findAruco(arucoDict, img, parameters, mtx, dist)
print('markercorners',markers[0], '\n')
print('markerID',markers[1], '\n')
print('rvec',twist[0], '\n')
print('tvec',twist[1], '\n')
print('position',position, '\n')
#tvec is going to be in centimeters
cv2.imshow('imag', img)
cv2.waitKey()

#
#
#
#
