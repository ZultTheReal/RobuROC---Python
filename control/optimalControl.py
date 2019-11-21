import numpy as np
import math

class OptimalControl:

    def __init__(self):
        self.clear()

    def clear(self):
                                                                    # Settings
        self.refGain = np.array([
            [20.099, 0],
            [0,      30.636]
        ])
        
        # Kr
        self.feedbackGain = np.array([
            [18.103, 0],
            [0,      7.428]
        ])
        
        self.L = 0.538                                              #axle width
        self.wheelRadius = 0.28                                     #wheel radius
        
        self.curMap = np.array([
            [1, -1],
            [1, 1],
            [1, 1],
            [1, -1]
        ])

    def run(self,velocityReference, omegaReference, velocityActual, omegaActual):
        
        refVector = np.array([
            [velocityReference],
            [omegaReference]
        ])

        feedbackVector = np.array([
            [velocityActual],
            [omegaActual]
        ])
        
        errorVector = np.matmul(self.refGain, refVector) - np.matmul(self.feedbackGain, feedbackVector)

        output = np.matmul(self.curMap, errorVector)[:,0] # Pull out the first column (the only column, as the output is a vector)
     
        capOutput = [max(min(i, 20.0), -20.0) for i in output]
        
        print("CUR: ",capOutput)
     
        return capOutput

        #currentMapping = self.iMap*wheelMapping                     # Mapping wheel speeds to motor currents (4,1)

        #return currentMappi
    
    
#optimal = OptimalControl()

#optimal.run(0.0, 0.6, 0.0, 0.0);