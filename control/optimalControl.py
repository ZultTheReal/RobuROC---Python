import numpy as np
import math

class OptimalControl:
    data = [0.0,0.0]
    def __init__(self):
        self.clear()

    def clear(self):
                                                                    # Settings
        #self.refGain = np.array([
        #    [2,      0],
        #    [0,      1.9795]
        #])
        
        # Kr
        #self.feedbackGain = np.array([
        #    [0.9764, 0],
        #    [0,      0.2712]
        #])

        testNumber = 1

        self.refGains = [
            np.array([
                [1.0003, 0],
                [0,      1.1446*0.8]
            ]),
            np.array([
                [10,     0],
                [0,      10.015]
            ]),
            np.array([
                [2.236, 0],
                [0,     2.304]
            ]),
            np.array([
                [1.4144, 0],
                [0,      1.5198]
            ]),
            np.array([
                [0.1028, 0],
                [0,      0.5657]
            ]),
            np.array([
                [0.4478, 0],
                [0,      0.7142]
            ]),
            np.array([
                [0.7075, 0],
                [0,      0.9]
            ])
        ]

        self.feedbackGains = [
            np.array([
                [0.9764, 0],
                [0,      0.5877]
            ]),
            np.array([
                [9.976, 0],
                [0,      9.4586]
            ]),
            np.array([
                [2.2122, 0],
                [0,      1.7475]
            ]),
            np.array([
                [1.3904, 0],
                [0,      0.9630]
            ]),
            np.array([
                [0.0788, 0],
                [0,      0.0089]
            ]),
            np.array([
                [0.4239, 0],
                [0,      0.1573]
            ]),
            np.array([
                [0.6835, 0],
                [0,      0.3432]
            ])
        ]

        self.refGain = 2 * self.refGains[testNumber-1]
        self.feedbackGain = self.feedbackGains[testNumber-1]

        print("refGain:", self.refGain)
        print("feedGain:", self.feedbackGain)

        self.L = 0.685                                              #axle width
        self.r = 0.28                                     #wheel radius
        
        self.map = np.array([
            [1/self.r, -self.L/(2*self.r)],
            [1/self.r, self.L/(2*self.r)]
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
     
        capOutput = [max(min(i/ratio, 20.0), -20.0) for i in output]
        
        #print("RAD/S: ",capOutput)
        
        for x in range(2):
            self.data[x] = capOutput[x]
     
        return capOutput

        #currentMapping = self.iMap*wheelMapping                     # Mapping wheel speeds to motor currents (4,1)

        #return currentMappi
    
    
#optimal = OptimalControl()

#optimal.run(1.0, 0, 0.0, 0.0);