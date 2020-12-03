import cv2
import numpy as np

# dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# markerImage = np.zeros((200, 200), dtype=np.uint8)
# markerImage = cv2.aruco.drawMarker(dictionary, 33, 200, markerImage, 1)
# cv2.imwrite("marker33.png", markerImage)
img = cv2.imread('marker33.png')
# cv2.imshow("marker", img)
# cv2.waitKey(0)
##detecting markers

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
#have to set frame to something
markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(img, dictionary, parameters = parameters)




