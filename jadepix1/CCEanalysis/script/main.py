import os
import sys
import re
import numpy as np

data = open('../data/Iron55Geant4EventData.dat','rb')
#data = open('../data/2018-01-25.dat','rb')

FrameNumber = 0
TimeStamp=data.read(36)
print(TimeStamp)

while True:

    OriginFrameBytesData = data.read(1928)

    if len(OriginFrameBytesData) != 1928:
        print('Finish read !','Total frames =',FrameNumber)
        break

    FrameRegex = re.compile(b'(^\xaa\xaa\xaa\xaa)(.*?)(\xf0\xf0\xf0\xf0$)',re.DOTALL)  

    try:
        m = FrameRegex.search(OriginFrameBytesData).group(2)
        #print(m)
        FrameNumber +=1
        print('Read',FrameNumber,'frames')

    except:
        print('Data is broken !')
        break

    M = re.split(b'\x97\x98..|\x57\x53..',m)
    FrameBytesData = b''.join(M)
    FrameIntData = np.frombuffer(FrameBytesData,dtype=np.uint8)
    #print(FrameIntData)
    #print(len(FrameBytesData))

    # frame_array=np.reshape(FrameIntData, newshape=(48, 16, 2))
        
    # frame=np.zeros((48, 16), dtype=int)
    # for i in range(0, 48):
    #     for j in range(0, 16):
    #         tmp=frame_array[i, j, 0]*256+frame_array[i, j, 1]
    #         frame[i, j]=tmp

data.close()

if __name__=="__main__":
    sys.exit()
 