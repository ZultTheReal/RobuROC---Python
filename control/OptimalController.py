import numpy as np

class OptimalController:

    def __init__(self):
        self.clear()

    def clear(self):
                                                                    # Settings
        self.optGain = np.array([[20.0691,0],[0,74.6329]])          # Kr
        self.optFeedback = np.array([[18.4056,0],[0,2.7297]])       # F
        self.L = 0.538                                              #axle width
        self.wheelRadius = 0.28                                     #wheel radius
        self.omegaRL = np.array([[1, 1], [self.L / self.wheelRadius, -(self.L / self.wheelRadius)]])
        # self.Ki = 1.2
        # self.iMap = np.array([[0,self.Ki],[self.Ki,0],[self.Ki,0], [0, self.Ki]])


    def OptimalControl(self,velocityReference, omegaReference, velocityCurrent, omegaCurrent):
        velocityRefScaled = velocityReference * self.optGain[0][0]  # Vref*Kr(1,1)
        omegaRefScaled = omegaReference * self.optGain[1][1]        # Oref*Kr(2,2)

        velocityFeedback = self.optFeedback[0][0]*velocityCurrent   # F(1,1)*V
        omegaFeedback = self.optFeedback[1][1]*omegaCurrent         # F(2,2)*Omega

        stateErrorVelocity = velocityRefScaled-velocityFeedback     # velocity error
        stateErrorOmega = omegaRefScaled-omegaFeedback              # omega error

        WheelMappingR = self.omegaRL[0][0]*stateErrorVelocity+self.omegaRL[1][0]*stateErrorVelocity     # Mapping state error values to right wheel
        WheelMappingL = self.omegaRL[0][1]*stateErrorOmega+self.omegaRL[1][1]*stateErrorOmega           # Mapping state error values to left wheel

        wheelMapping = np.array([[WheelMappingR,WheelMappingL]])    #Collecting wheel maps in vector

        return wheelMapping

        #currentMapping = self.iMap*wheelMapping                     # Mapping wheel speeds to motor currents (4,1)

        #return currentMapping