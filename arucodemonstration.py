import cv2
import numpy as np

# dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)

# markerImage = np.zeros((200, 200), dtype=np.uint8)
# markerImage = cv2.aruco.drawMarker(dictionary, 33, 200, markerImage, 1)
# cv2.imwrite("marker33.png", markerImage)
img = cv2.imread('IMG_1597.jpg')
img = cv2.resize(img, (640, 480))
cv2.imshow("marker", img)
cv2.waitKey()

##detecting markers

dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_250)
parameters = cv2.aruco.DetectorParameters_create()
#have to set frame to something
markerCorners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(img, dictionary, parameters = parameters)
frame_markers = cv2.aruco.drawDetectedMarkers(img.copy(), markerCorners, markerIds)
print(markerIds)
cv2.imshow('markers', frame_markers)
cv2.waitKey()







