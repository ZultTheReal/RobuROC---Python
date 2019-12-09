import numpy as np
from numpy.linalg import inv
#import math

WHEEL_RADIUS = 0.28 # meter
WIDTH_CAR = 0.69 # meter
dt = 0.05
nrStates = 7
nrSensors = 8
eTol = 0.7


class EKF:
    data = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    
    def __init__(self):
        self.mu = np.zeros((nrStates,1)) # X, Y, Theta, Vb, Omega, Sl, Sr
        self.sigma = np.zeros((nrStates,nrStates))
        self.G = np.zeros((nrStates,nrStates))
        self.H = np.zeros((nrStates,nrSensors))
        self.K = np.zeros((nrStates,nrSensors))
        self.z = np.zeros((nrSensors,1))
        self.u = np.zeros((2,1))
        self.Sl = 0.05 # slip "sensor" left, value used to init state
        self.Sr = 0.05 # slip "sensor" right, value used to init state
        
        
        

        #State space covariance
        self.R = np.array([[1e-11,   0,      0,      0,      0,      0,      0], #X
                           [0,      1e-11,   0,      0,      0,      0,      0], #Y
                           [0,      0,      1e-8,   0,      0,      0,      0], #Theta
                           [0,      0,      0,      1e-5,   0,      0,      0], #Vb
                           [0,      0,      0,      0,      1e-5,   0,      0], #Omega
                           [0,      0,      0,      0,      0,      1e-2,   0], #Sl
                           [0,      0,      0,      0,      0,      0,      1e-2]]) #Sr 

        #Sensor covariance
        self.Q = np.array([[1e-7,   0,      0,      0,      0,      0,      0,      0],  # X_gps
                           [0,      1e-7,   0,      0,      0,      0,      0,      0],  #Y_gps
                           [0,      0,      1e-2,   0,      0,      0,      0,      0],  #Theta_gps
                           [0,      0,      0,      1e-8,   0,      0,      0,      0], #Theta_mag
                           [0,      0,      0,      0,      1e-4,   0,      0,      0],  #V_gps
                           [0,      0,      0,      0,      0,      1e-7,   0,      0], #Omega_gyro
                           [0,      0,      0,      0,      0,      0,      1e2,   0], #Sl
                           [0,      0,      0,      0,      0,      0,      0,      1e2]]) #Sr  

    def set_Init(self,gpsX,gpsY,magTheta):
        self.mu = np.array([[gpsX],[gpsY],[magTheta],[0],[0],[self.Sl],[self.Sr]]) #Init mu with expected values 
        self.sigma = self.R
        return

    def slipSens(self,omegaLw,omegaRw,V_gps,Omega_gyro, gpsAvailble): #Calculate estimated "sensor" slip
        if ((gpsAvailble == 1) and (V_gps > 0.3) and (abs(omegaLw) > 0.2) and (abs(omegaRw) > 0.2)):
            Sl = (1 - (2* V_gps - Omega_gyro* WIDTH_CAR)/(2*WHEEL_RADIUS*omegaLw))
            Sr = (1 - (2* V_gps + Omega_gyro* WIDTH_CAR)/(2*WHEEL_RADIUS*omegaRw))
            Sl, Sr = self.correctSlip(Sl,Sr)
            return Sl,Sr,1 # moving =1
        else:
            return 0,0,0 # moving = 0
    
    def correctSlip(self,Sl,Sr): #Function to make sure slip never gets below zero or above 1 
        if Sl < 0:
            Sl =0
        elif Sl > 1:
            Sl = 1 

        if Sr < 0:
            Sr = 0
        elif Sr > 1:
            Sr = 1 
        return Sl, Sr

    def correctGps(self,Theta_Gps,Theta_mag):
        if (Theta_Gps < eTol) and (Theta_mag > (2*np.pi - eTol)): #eg. Gps 0.1pi, mag 1.9pi --> Gps becoms 2.1pi
            return Theta_Gps + 2*np.pi

        elif (Theta_Gps > (2*np.pi - eTol)) and (Theta_mag <  eTol): #eg. Gps 1.9pi, mag 0.1pi --> Gps becoms -0.1pi
            return Theta_Gps - 2*np.pi
        return Theta_Gps

    def correctThetaPredict(self,Theta_predict,Theta_mag):
        if (Theta_predict < eTol) and (Theta_mag > (2*np.pi - eTol)): #eg. Gps 0.1pi, mag 1.9pi --> Gps becoms 2.1pi
            return Theta_predict + 2*np.pi

        elif (Theta_predict > (2*np.pi - eTol)) and (Theta_mag <  eTol): #eg. Gps 1.9pi, mag 0.1pi --> Gps becoms -0.1pi
            return Theta_predict - 2*np.pi
        return Theta_predict
        

    def updateEKF(self,omegaLw,omegaRw, X_gps, Y_gps, Theta_gps, Theta_mag, V_gps, Omega_gyro, gpsAvailble):
        self.Sl,self.SR, moving = self.slipSens(omegaLw,omegaRw,V_gps,Omega_gyro, gpsAvailble) 
        Theta_gps = self.correctGps(Theta_gps,Theta_mag)

        # u is the input vector containing omegaLw and omegaRw
        self.u = np.array([[omegaLw],[omegaRw]])

        # Z is the sensor vector in order: X_gps, Y_gps, Theta_gps, Theta_mag, V_gps, Omega_gyro, Sl, Sr
        self.z = np.array([[X_gps],[Y_gps],[Theta_gps],[Theta_mag],[V_gps],[Omega_gyro],[self.Sl],[self.Sr]])
        
        #init matrixes
        self.G = self.Gmatrix(self.mu,self.u)
        self.H = self.Hmatrix(gpsAvailble, moving)


        #predict
        self.mu = self.gFunc(self.mu,self.u)
        #print(self.mu[4])
        self.sigma = self.G @ self.sigma @ self.G.transpose() + self.R

        # Correcting predicted values 
        self.mu[2,0] = self.correctThetaPredict(self.mu[2,0],Theta_mag)
    

        #Update
        self.K = self.sigma @ self.H.transpose() @ (inv(self.H @ self.sigma @ self.H.transpose() + self.Q))
        self.mu = self.mu + self.K @ (self.z - self.H @ self.mu)
        self.sigma = (np.identity(nrStates) - self.K @ self.H) @ self.sigma

        # Correct slip since it cannot be below zero
        self.mu[5,0],self.mu[6,0] = self.correctSlip(self.mu[5,0],self.mu[6,0])
        for x in range(nrStates):
            self.data[x] = float(self.mu[x])





        
    def gFunc(self,mu,u):
        return np.array([[mu[0,0] + dt*np.cos(mu[2,0])*mu[3,0]],  #x  = mu[0,0]
                         [mu[1,0] + dt*np.sin(mu[2,0])*mu[3,0]],  #y  = mu[1,0]
                         [mu[2,0] + dt*mu[4,0]],  #theta = mu[2,0]
                         [(u[0,0]*WHEEL_RADIUS*(1-mu[5,0]) + u[1,0]*WHEEL_RADIUS*(1-mu[6,0]))/2],   #Vb = mu[3,0]
                         [(- u[0,0]*WHEEL_RADIUS*(1-mu[5,0]) + u[1,0]*WHEEL_RADIUS*(1-mu[6,0]))/WIDTH_CAR ], #omega = mu[4,0]
                         [mu[5,0]  ],  #Sl = mu[5,0]
                         [mu[6,0]  ]]) #Sr = mu[6,0]

    def Gmatrix(self,mu,u):
        return np.array([[1,    0,  -dt*mu[3,0]*np.sin(mu[2,0]),    dt*np.cos(mu[2,0]),     0,      0,                              0],
                         [0,    1,  dt*mu[3,0]*np.cos(mu[2,0]),     dt*np.sin(mu[2,0]),     0,      0,                              0],
                         [0,    0,  1,                              0,                      dt,     0,                              0],
                         [0,    0,  0,                              0,                      0,      -WHEEL_RADIUS*u[0,0]/2,         -WHEEL_RADIUS*u[1,0]/2],
                         [0,    0,  0,                              0,                      0,      WHEEL_RADIUS*u[0,0]/WIDTH_CAR,  -WHEEL_RADIUS*u[1,0]/WIDTH_CAR],
                         [0,    0,  0,                              0,                      0,      1,                              0],
                         [0,    0,  0,                              0,                      0,      0,                              1]])   

    def Hmatrix(self,gpsAvailble,moving):
        if gpsAvailble == 1:
            if moving == 1:
                return np.array([   [1,       0,       0,       0,       0,       0,       0], #GPS_x
                                    [0,       1,       0,       0,       0,       0,       0], #GPS_y
                                    [0,       0,       1,       0,       0,       0,       0], #Theta_Gps
                                    [0,       0,       1,       0,       0,       0,       0], #Theta_mag
                                    [0,       0,       0,       1,       0,       0,       0], #V_gps
                                    [0,       0,       0,       0,       1,       0,       0], #omega_gyro
                                    [0,       0,       0,       0,       0,       1,       0], # Sl_sens
                                    [0,       0,       0,       0,       0,       0,       1]]) # Sr_sens

            else:
                return np.array([   [1,       0,       0,       0,       0,       0,       0], #GPS_x
                                    [0,       1,       0,       0,       0,       0,       0], #GPS_y
                                    [0,       0,       1,       0,       0,       0,       0], #Theta_Gps
                                    [0,       0,       1,       0,       0,       0,       0], #Theta_mag
                                    [0,       0,       0,       1,       0,       0,       0], #V_gps
                                    [0,       0,       0,       0,       1,       0,       0], #omega_gyro
                                    [0,       0,       0,       0,       0,       0,       0], # Sl_sens
                                    [0,       0,       0,       0,       0,       0,       0]]) # Sr_sens

        else:
            return np.array([   [0,       0,       0,       0,       0,       0,       0], #GPS_x
                                [0,       0,       0,       0,       0,       0,       0], #GPS_y
                                [0,       0,       0,       0,       0,       0,       0], #Theta_Gps
                                [0,       0,       1,       0,       0,       0,       0], #Theta_mag
                                [0,       0,       0,       0,       0,       0,       0], #V_gps
                                [0,       0,       0,       0,       1,       0,       0], #omega_gyro
                                [0,       0,       0,       0,       0,       0,       0], # Sl_sens
                                [0,       0,       0,       0,       0,       0,       0]]) # Sr_sens




# def testKalmann(EKF): #only testcode, not to be used 
#     import csv
#     import matplotlib.pyplot as plt

#     reader = csv.reader(open("M_tab.csv", "rt"), delimiter=",")
#     data = list(reader)
#     rows = len(data)
#     collums = len(data[0])
#     #print(rows,collums)
#     #print(data[0])

#     EKF.set_Init(float(data[1][2]),float(data[1][3]),float(data[1][5]))

#     x = list(EKF.mu[0])
#     y = list(EKF.mu[1])
#     theta= list(EKF.mu[2])
#     Vb = list(EKF.mu[3])
#     omega = list(EKF.mu[4])
#     Sl = list(EKF.mu[5])
#     Sr = list(EKF.mu[6])
#     gpsAvail = [0]
#     slipSensVal = [(0,0,0)]


#     for k in range(2,rows):
#         if abs(float(data[k][6]))  < 0.3:
#             gpsAvailble = 0
#         else:
#             gpsAvailble = 1
#         EKF.updateEKF( float(data[k][0]),float(data[k][1]),float(data[k][2]),float(data[k][3]),float(data[k][4]),float(data[k][5]),float(data[k][6]),float(data[k][7]),gpsAvailble  )
#         #plt.plot(EKF.mu[0],EKF.mu[1])
#         x.append(float(EKF.mu[0]))
#         y.append(float(EKF.mu[1]))
#         theta.append(float(EKF.mu[2]))
#         Vb.append(float(EKF.mu[3]))
#         omega.append(float(EKF.mu[4]))
#         Sl.append(float(EKF.mu[5]))
#         Sr.append(float(EKF.mu[6]))
#         gpsAvail.append(gpsAvailble)
#         slipSensVal.append(EKF.slipSens(float(data[k][0]),float(data[k][1]),float(data[k][6]),float(data[k][7]), gpsAvailble))


#     plt.figure(1)
#     plt.subplot(3,2,(1,3))
#     plt.plot(x,y)


#     plt.subplot(3,2,2)
#     plt.plot(theta)

#     plt.subplot(3,2,4)
#     plt.plot(Vb)

#     plt.subplot(3,2,6)
#     plt.plot(omega)

#     plt.subplot(3,2,5)
#     plt.plot(Sl)
#     plt.plot(Sr)

#     plt.figure(2)
    

#     slSens = [row[0] for row in slipSensVal]
#     srSens  = [row[1] for row in slipSensVal]
#     moving = [row[2] for row in slipSensVal]

#     plt.plot(gpsAvail, label="GPSAvail")
#     plt.plot(slSens, label="slSens")
#     plt.plot(srSens, label="srSens")
#     plt.plot(moving,label="moving")
#     plt.legend()
#     plt.show()


# #Testcode
# EKF = EKF()
# testKalmann(EKF)