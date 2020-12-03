from djitellopy import Tello
import cv2
import numpy as np
import time
from time import sleep
import helper


# ######################################################################
# width = 640  # WIDTH OF THE IMAGE
# height = 480  # HEIGHT OF THE IMAGE
# deadZone =100
# ######################################################################
 
# startCounter = 1
 
# # CONNECT TO TELLO
# me = Tello()
# me.connect()
# me.for_back_velocity = 0
# me.left_right_velocity = 0
# me.up_down_velocity = 0
# me.yaw_velocity = 0
# me.speed = 0
 
 
 
# print(me.get_battery())
# sleep(10)

# me.streamoff()
# me.streamon()
# ########################
 
# frameWidth = width
# frameHeight = height

# global imgContour
# global dir;
    
 
# while True:
 
#     # GET THE IMAGE FROM TELLO
#     frame_read = me.get_frame_read()
#     myFrame = frame_read.frame
#     img = cv2.resize(myFrame, (width, height))
#     imgContour = img.copy()
#     imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#     h_min = 0
#     h_max = 179
#     s_min = 0
#     s_max = 255
#     v_min = 75
#     v_max = 194
#     lower = np.array([h_min,s_min,v_min])
#     upper = np.array([h_max,s_max,v_max])
#     mask = cv2.inRange(imgHsv,lower,upper)
#     result = cv2.bitwise_and(img,img, mask = mask)
#     mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
#     imgBlur = cv2.GaussianBlur(result, (7, 7), 1)
#     imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
#     threshold1 = 221
#     threshold2 = 248
#     imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
#     kernel = np.ones((5, 5))
#     imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
#     helper.getContours(imgDil, imgContour)
#     helper.display(imgContour)
 
#     if startCounter == 0:
#        me.takeoff()
#        startCounter = 1
#        sleep(5)
 
#     position = 0
#     if dir == 1:
#     #    me.yaw_velocity = -60
#        me.move_left(20)
#        position -= 20

#     elif dir == 2:
#     #    me.yaw_velocity = 60
#        me.move_right(20)
#        position += 20
#     elif dir == 3:
#        me.up_down_velocity= 60
#     elif dir == 4:
#        me.up_down_velocity= -60
#     else:
#        me.left_right_velocity = 0; me.for_back_velocity = 0;me.up_down_velocity = 0; me.yaw_velocity = 0
#    # SEND VELOCITY VALUES TO TELLO

#     if me.send_rc_control:
#        me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)
 
#     stack = helper.stackImages(0.9, ([img, result], [imgDil, imgContour]))
#     cv2.imshow('Horizontal Stacking', stack)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         me.land()
#         break

# cv2.destroyAllWindows()