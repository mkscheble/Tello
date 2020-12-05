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
mtx = [[606.42428705, 0.0,320.3971664],
 [0, 607.16835468, 219.84335448],
 [0., 0., 1.]]
dist = [[-0.00895433, -0.12056427, -0.00618839, 0.00344274, 0.4009607]]

mtx = np.float32(mtx)
dist = np.float32(dist)

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
