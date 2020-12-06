from djitellopy import Tello
import cv2
import numpy as np
from time import sleep

def trackArucoX(myDrone, twist, pid, pError):
    """PID controller implemented for moving forward, yaw_axis, and left right velocity
    To Do: need to implement up and down and I think we can use direction for that"""

    """trim speeds to 30 because indoors and don't want a crazy velocity into the wall, 
    also because frames don't update quick enough, scared it might not update and just keep flying into the wall"""

    # Sends RC command based on distance of translation vector
    if np.all(twist[1]) != None:
        if np.all(twist[1][0][0]) != 0:
            # PID for left_right_forwards backwards
            error = twist[1][0][0][0]
            speed = pid[0] * error + pid[1] * (error - pError)
            speed = int(np.clip(speed, -30, 30))

            # error2 = twist[1][0][0][1]
            # speed2 = pid2[0] * error2 + pid2[1] * (error2 - pError2)
            # speed2 = int(np.clip(speed2, -30, 30))

            # # PID for forwards backwards
            # error3 = twist[1][0][0][2]
            # speed3 = pid3[0] * error3 + pid3[1] * (error3 - pError3)
            # speed3 = int(np.clip(speed2, -30, 30))

            # speed2 = 0
            # speed3 = 0
            # error2 = 0
            # error3 = 0


            # print('speed', speed,'\n')
            # print('speed2', speed2)
            # print('speed3', speed3, '\n')
            myDrone.left_right_velocity = speed
            myDrone.for_back_velocity = 0 #speed3
            myDrone.up_down_velocity = 0 #speed2
            myDrone.yaw_velocity = 0
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0
        error2 = 0
        error3 = 0
        speed = 0
        speed2 = 0
        speed3 = 0
    # if myDrone.send_rc_control:
    myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)

    # return errors for previous errors and PID controller
    return error, speed

def trackArucoY(myDrone, twist, pid, pError):
    """PID controller implemented for moving forward, yaw_axis, and left right velocity
    To Do: need to implement up and down and I think we can use direction for that"""

    """trim speeds to 30 because indoors and don't want a crazy velocity into the wall, 
    also because frames don't update quick enough, scared it might not update and just keep flying into the wall"""

    # Sends RC command based on distance of translation vector
    if np.all(twist[1]) != None:
        if np.all(twist[1][0][0]) != 0:
            # PID for left_right_forwards backwards
            # error = twist[1][0][0][0]
            # speed = pid[0] * error + pid[1] * (error - pError)
            # speed = int(np.clip(speed, -30, 30))

            error = twist[1][0][0][1]
            speed = pid[0] * error + pid[1] * (error - pError)
            speed = int(np.clip(speed, -30, 30))

            # # PID for forwards backwards
            # error3 = twist[1][0][0][2]
            # speed3 = pid3[0] * error3 + pid3[1] * (error3 - pError3)
            # speed3 = int(np.clip(speed2, -30, 30))

            # speed2 = 0
            # speed3 = 0
            # error2 = 0
            # error3 = 0


            # print('speed', speed,'\n')
            # print('speed2', speed2)
            # print('speed3', speed3, '\n')
            myDrone.left_right_velocity = 0
            myDrone.for_back_velocity = 0 #speed3
            myDrone.up_down_velocity = speed #speed2
            myDrone.yaw_velocity = 0
    else:
        myDrone.for_back_velocity = 0
        myDrone.left_right_velocity = 0
        myDrone.up_down_velocity = 0
        myDrone.yaw_velocity = 0
        error = 0
        error2 = 0
        error3 = 0
        speed = 0
        speed2 = 0
        speed3 = 0
    # if myDrone.send_rc_control:
    myDrone.send_rc_control(myDrone.left_right_velocity,
                                myDrone.for_back_velocity,
                                myDrone.up_down_velocity,
                                myDrone.yaw_velocity)

    # return errors for previous errors and PID controller
    return error, speed