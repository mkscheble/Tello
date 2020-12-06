from queue import Queue
from queue import LifoQueue
import numpy as np

def writeFileHeader(dataFileName):
    fileout = open(dataFileName,'w')
    fileout.write('height, flight_time, time, speed, speed2, speed3, Error, Error2, Error3\n')
    fileout.close()

def appendtoFile(dataFileName, dataQ):
    fileout = open(dataFileName, 'a')  # append
    print('writing data to file')
    while not dataQ.empty():
        telemdata = dataQ.get()
        fileout.write(str(telemdata) + '\n')
    fileout.close()
