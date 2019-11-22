import numpy as np
import math

class OptimalControl:

    def __init__(self):
        self.clear()

    def clear(self):
                                                                    # Settings
        self.refGain = np.array([
            [1.2, 0],
            [0,      1.8]
        ])
        
        # Kr
        self.feedbackGain = np.array([
            [0.3, 0],
            [0,      0.5]
        ])
        
        self.L = 0.685                                              #axle width
        self.r = 0.28                                     #wheel radius
        
        self.map = np.array([
            [1/self.r, 1/(2*self.r)],
            [1/self.r, -1/(2*self.r)]
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

        output = np.matmul(self.map, errorVector)[:,0] # Pull out the first column (the only column, as the output is a vector)
     
        ratio = 1
     
        capOutput = [max(min(i/ratio, 5.0), -5.0) for i in output]
        
        print("RAD/S: ",capOutput)
     
        return capOutput

        #currentMapping = self.iMap*wheelMapping                     # Mapping wheel speeds to motor currents (4,1)

        #return currentMappi
    
    
#optimal = OptimalControl()

#optimal.run(1.0, 0, 0.0, 0.0);