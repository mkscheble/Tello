def writeFileHeader(dataFileName):
    fileout = open(dataFileName,'w')
    fileout.write('begin')
    fileout.close()

def appendtoFile(dataFileName, speed, time):
    fileout = open(dataFileName, 'a')  # append
    print('writing data to file')
    fileout.write('[str(speed), str(time)]')
    fileout.close()