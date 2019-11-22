import numpy as np
import math

class OptimalControl:

    def __init__(self):
        self.clear()

    def clear(self):
                                                                    # Settings
        self.refGain = np.array([
            [1.9409, 0],
            [0,      13.5762]
        ])
        
        # Kr
        self.feedbackGain = np.array([
            [0.2774, 0],
            [0,      0.0369]
        ])
        
        self.L = 0.685                                              #axle width
        self.wheelRadius = 0.28                                     #wheel radius
        
        self.map = np.array([
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

        output = np.matmul(self.map, errorVector)[:,0] # Pull out the first column (the only column, as the output is a vector)
     
        capOutput = [max(min(i, 8.0), -8.0) for i in output]
        
        print("RAD/S: ",capOutput)
     
        return capOutput

        #currentMapping = self.iMap*wheelMapping                     # Mapping wheel speeds to motor currents (4,1)

        #return currentMappi
    
    
optimal = OptimalControl()

optimal.run(0.0, 0.2, 0.0, 0.0);