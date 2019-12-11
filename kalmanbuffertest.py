import numpy as np
import time

kalmanMuBuffer = [None, None, None, None, None, None, None]

while(1):

    kalmanMuBuffer.pop()
    kalmanMuBuffer.insert(0,np.random.rand(2,2))

    time.sleep(1);
    
    print(kalmanMuBuffer)