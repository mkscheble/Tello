from queue import Queue
from queue import LifoQueue
import numpy as np

def writeFileHeader(dataFileName):
    fileout = open(dataFileName,'w')
    fileout.write('  index,   time,    ref,ctrl_LR,ctrl_FB,ctrl_UD,ctrl_YA,  pitch,   roll,    yaw,    vgx,    vgy,    vgz,   templ,   temph,    tof,      h,    bat,   baro,   time,    agx,    agy,    agz\n\r')
    fileout.close()

def appendtoFile(dataFileName, speed, time):
    fileout = open(dataFileName, 'a')  # append
    print('writing data to file')
    fileout.write(str([speed, time]) +'\n')
    fileout.close()
