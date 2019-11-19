import numpy as np

class OptimalControl:

    def __init__(self):
        self.clear()

    def clear(self):
                                                                    # Settings
        self.optGain = np.array([[2.603,0],[0,1]])          # Kr
        self.optFeedback = np.array([[0.9379,0],[0,1]])       # F
        self.L = 0.538                                              #axle width
        self.wheelRadius = 0.28                                     #wheel radius
        self.vRL = np.array([[1, 1], [self.L / self.wheelRadius, -(self.L / self.wheelRadius)]])
        # self.Ki = 1.2
        # self.iMap = np.array([[0,self.Ki],[self.Ki,0],[self.Ki,0], [0, self.Ki]])


    def run(self,velocityReference, omegaReference, velocityCurrent, omegaCurrent):
        #print(self.optGain, self.optGain[0][0] )
        velocityRefScaled = velocityReference * self.optGain[0][0]  # Vref*Kr(1,1)
        omegaRefScaled = omegaReference * self.optGain[1][1]        # Oref*Kr(2,2)
        
        velocityFeedback = self.optFeedback[0][0]*velocityCurrent   # F(1,1)*V
        omegaFeedback = self.optFeedback[1][1]*omegaCurrent         # F(2,2)*Omega
        
        stateErrorVelocity = velocityRefScaled-velocityFeedback     # velocity error
        stateErrorOmega = omegaRefScaled-omegaFeedback              # omega error

        WheelMappingR = self.vRL[0][0]*stateErrorVelocity+self.vRL[1][0]*stateErrorOmega     # Mapping state error values to right wheel
        WheelMappingL = self.vRL[0][1]*stateErrorVelocity+self.vRL[1][1]*stateErrorOmega           # Mapping state error values to left wheel

        wheelMapping = np.array([[WheelMappingR,WheelMappingL]])    #Collecting wheel maps in vector
        #print(wheelMapping)
        return wheelMapping[0][0], wheelMapping[0][1]

        #currentMapping = self.iMap*wheelMapping                     # Mapping wheel speeds to motor currents (4,1)

        #return currentMappi 