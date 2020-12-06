import cv2
import numpy as np

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)

markerImage = np.zeros((200, 200), dtype=np.uint8)
markerImage = cv2.aruco.drawMarker(dictionary, 9, 200, markerImage, 1)
cv2.imwrite("marker9.png", markerImage)
img = cv2.imread('marker9.png')
# img = cv2.resize(img, (640, 480))
cv2.imshow("marker", img)
cv2.waitKey()

##detecting markers

# dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
# parameters = cv2.aruco.DetectorParameters_create()
# #have to set frame to something
# markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(img, dictionary, parameters = parameters)
# frame_markers = cv2.aruco.drawDetectedMarkers(img.copy(), markerCorners, markerIds)
# print(markerIds)
# cv2.imshow('markers', frame_markers)
# cv2.waitKey()

# from visionProcessing import *
# from utils import *
#
# # myDrone = initializeTello()
# w, h = 640, 480
# arucoDict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
# parameters = cv2.aruco.DetectorParameters_create()
# mtx = np.float32([[622.36525763, 0., 307.57777951],
#                   [0., 621.76827265, 247.45519961],
#                   [0., 0., 1.]])
# dist = np.float32([[-4.09107478e-03, -7.38739614e-04, 1.68557817e-03, 1.16567623e-04, 1.34176960e-01]])
#
# img = cv2.imread(r'C:\Users\ad\Desktop\Tello\images\IMG_1597.jpg')
# img = cv2.resize(img, (640, 480))
# img, markers, twist, position = findAruco(arucoDict, img, parameters, mtx, dist)
# print('markercorners',markers[0], '\n')
# print('markerID',markers[1], '\n')
# print('rvec',twist[0], '\n')
# print('tvec',twist[1], '\n')
# print('position',position, '\n')
# #tvec is going to be in centimeters
# cv2.imshow('imag', img)
# cv2.waitKey()

#
#
#
#
