from queue import Queue
from queue import LifoQueue
import numpy as np

def writeFileHeader(dataFileName):
    fileout = open(dataFileName,'w')
    fileout.write('  index,   time,    ref,ctrl_LR,ctrl_FB,ctrl_UD,ctrl_YA,  pitch,   roll,    yaw,    vgx,    vgy,    vgz,   templ,   temph,    tof,      h,    bat,   baro,   time,    agx,    agy,    agz\n\r')
    fileout.close()

def appendtoFile(dataFileName, dataQ):
    fileout = open(dataFileName, 'a')  # append
    print('writing data to file')
    while not dataQ.empty():
        telemdata = dataQ.get()
        fileout.write(str(telemdata) + '\n')
    fileout.close()
