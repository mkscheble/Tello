def writeFileHeader(dataFileName):
    fileout = open(dataFileName,'w')   
    fileout.close()

def appendtoFile(dataFileName, position):
    fileout = open(data_file_name, 'a')  # append
    print('writing data to file')
    fileout.write('position: ' + str(position))
    fileout.close()