import re
import numpy as np

data = open('../data/2018-01-25.dat','rb')

timestamp = data.read(35)
print('timestamp = ',timestamp)

for i in range(0,3):
    FrameBytesData = data.read(1928)
    print(FrameBytesData,'\n')
    FrameRegex = re.compile(b'(^\xaa\xaa\xaa\xaa\x57\x53..)(.*?)(\x97\x98..\xf0\xf0\xf0\xf0$)')
   
    try:
        m = FrameRegex.search(FrameBytesData).group(2)
    except:
        print('data is broken !')

    # M = re.split(b'\x97\x98..\x57\x53..',m)
    # #print(M)

    # N = b''.join(M)

    # X = np.frombuffer(N,dtype=np.uint8)

    # frame_array=np.reshape(X, newshape=(48, 16, 2))
        
    # frame=np.zeros((48, 16), dtype=int)
    # for i in range(0, 48):
    #     for j in range(0, 16):
    #         tmp=frame_array[i, j, 0]*256+frame_array[i, j, 1]
    #         frame[i, j]=tmp

    
