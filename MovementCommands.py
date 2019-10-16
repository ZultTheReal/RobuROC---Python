import MainWindow as mw
from MainWindow import *
import Variables
from Variables import *
import Functions
from Functions import *


def forward(self):
    print("Moving forward")
    for i in range(4):
        if (i % 2) == 0:
            network.send_message(Variables.addressMap[i], velocityArray(Variables.globalspeed), 0)
            print("network.send_message(", Variables.addressMap[i], velocityArray(Variables.globalspeed), "0)")
        else:
            network.send_message(Variables.addressMap[i], velocityArray(-Variables.globalspeed), 0)
            print("network.send_message(", Variables.addressMap[i], velocityArray(-Variables.globalspeed), "0)")

    # network.send_message(addressMap[0], velocityArray(Speed), 0)
    # network.send_message(addressMap[1], velocityArray(-(Speed)), 0)
    # network.send_message(addressMap[2], velocityArray(Speed), 0)
    # network.send_message(addressMap[3], velocityArray(-(Speed)), 0)

def backward(self):
    print("Moving backward")
    for i in range(4):
        if (i % 2) == 0:
            network.send_message(Variables.addressMap[i], velocityArray(-Variables.globalspeed),0)
            print("network.send_message(", Variables.addressMap[i], velocityArray(-Variables.globalspeed), "0)")
        else:
            network.send_message(Variables.addressMap[i], velocityArray(Variables.globalspeed), 0)
            print("network.send_message(", Variables.addressMap[i], velocityArray(Variables.globalspeed), "0)")

    # network.send_message(addressMap[0], velocityArray(-Speed), 0)
    # network.send_message(addressMap[1], velocityArray(Speed), 0)
    # network.send_message(addressMap[2], velocityArray(-Speed), 0)
    # network.send_message(addressMap[3], velocityArray(Speed), 0)

def moveLeft(self):
    print("Moving left")
    for i in range(4):
        network.send_message(Variables.addressMap[i], velocityArray(-Variables.globalspeed), 0)
        print("network.send_message(", Variables.addressMap[i], velocityArray(-Variables.globalspeed/2), "0)")

def moveRight(self):
    print("Moving right")
    for i in range(4):
        network.send_message(Variables.addressMap[i], velocityArray(Variables.globalspeed), 0)
        print("network.send_message(", Variables.addressMap[i], velocityArray(Variables.globalspeed/2), "0)")

def holdStill(self):
    print("Stopping")
    stopspeed = 0
    for i in range(4):
        network.send_message(Variables.addressMap[i], velocityArray(stopspeed), 0)
        print("network.send_message(", Variables.addressMap[i], velocityArray(stopspeed), "0)")

def setSpeed1(self):
    print("Motor Speed for: ", Variables.addressMap[0], "is ", self.motorSpeed1.text)
    print(velocityArray(self.motorSpeed1.text))
    network.send_message(Variables.addressMap[0], velocityArray(self.motorSpeed1.text), 0)

def setSpeed2(self):
    print("Motor Speed for: ", Variables.addressMap[1], "is ", self.motorSpeed2.text)
    print(velocityArray(self.motorSpeed2.text))
    network.send_message(Variables.addressMap[1], velocityArray(-(self.motorSpeed2.text)), 0)

def setSpeed3(self):
    print("Motor Speed for: ", Variables.addressMap[2], "is ", self.motorSpeed3.text)
    print(velocityArray(self.motorSpeed3.text))
    network.send_message(Variables.addressMap[2], velocityArray(self.motorSpeed3.text), 0)

def setSpeed4(self):
    print("Motor Speed for: ", Variables.addressMap[3], "is ", self.motorSpeed4.text)
    print(velocityArray(self.motorSpeed4.text))
    network.send_message(Variables.addressMap[3], velocityArray(-(self.motorSpeed4.text)), 0)

def setSpeedAll(self):
    # Enable operation and set target velocity
    # Enable operation command: 0x0F
    print("Speed set for all")
    network.send_message(Variables.addressMap[0], velocityArray(motorSpeed1), 0)
    network.send_message(Variables.addressMap[1], velocityArray(-motorSpeed2), 0)
    network.send_message(Variables.addressMap[2], velocityArray(motorSpeed3), 0)
    network.send_message(Variables.addressMap[3], velocityArray(-motorSpeed4), 0)