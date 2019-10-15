import MainWindow as main
import Functions as fc

addressMap = {
    0: 0x301,
    1: 0x302,
    2: 0x303,
    3: 0x304
}

def forward(self):
    print("Moving forward")
    Speed = 1500000
    for i in range(4):
        if (i % 2) == 0:
            print("network.send_message(", addressMap[i], fc.velocityArray(Speed), "0)")
        else:
            print("network.send_message(", addressMap[i], fc.velocityArray(-Speed), "0)")

    # network.send_message(addressMap[0], fc.velocityArray(Speed), 0)
    # network.send_message(addressMap[1], fc.velocityArray(-(Speed)), 0)
    # network.send_message(addressMap[2], fc.velocityArray(Speed), 0)
    # network.send_message(addressMap[3], fc.velocityArray(-(Speed)), 0)

def backward(self):
    print("Moving backward")
    Speed = 1500000
    for i in range(4):
        if (i % 2) == 0:
            print("network.send_message(", addressMap[i], fc.velocityArray(-Speed), "0)")
        else:
            print("network.send_message(", addressMap[i], fc.velocityArray(Speed), "0)")

    # network.send_message(addressMap[0], fc.velocityArray(-Speed), 0)
    # network.send_message(addressMap[1], fc.velocityArray(Speed), 0)
    # network.send_message(addressMap[2], fc.velocityArray(-Speed), 0)
    # network.send_message(addressMap[3], fc.velocityArray(Speed), 0)

def moveLeft(self):
    print("Moving left")
    Speed = 750000
    for i in range(4):
        #network.send_message(addressMap[i], fc.velocityArray(-Speed), 0)
        print("network.send_message(", addressMap[i], fc.velocityArray(-Speed), "0)")

def moveRight(self):
    print("Moving right")
    Speed = 750000
    for i in range(4):
        #network.send_message(addressMap[i], fc.velocityArray(Speed), 0)
        print("network.send_message(", addressMap[i], fc.velocityArray(Speed), "0)")

def holdStill(self):
    print("Stopping")
    Speed = 0
    for i in range(4):
        #network.send_message(addressMap[i], fc.velocityArray(Speed), 0)
        print("network.send_message(", addressMap[i], fc.velocityArray(Speed),"0)")

def setSpeed1(self):
    print("Motor Speed for: ", addressMap[0], "is ", self.motorSpeed1.text)
    print(fc.velocityArray(self.motorSpeed1.text))
    # network.send_message(addressMap[0], fc.velocityArray(self.motorSpeed1.text), 0)

def setSpeed2(self):
    print("Motor Speed for: ", addressMap[1], "is ", self.motorSpeed2.text)
    print(fc.velocityArray(self.motorSpeed2.text))
    # network.send_message(addressMap[1], fc.velocityArray(-(self.motorSpeed2.text)), 0)

def setSpeed3(self):
    print("Motor Speed for: ", addressMap[2], "is ", self.motorSpeed3.text)
    print(fc.velocityArray(self.motorSpeed3.text))
    # network.send_message(addressMap[2], fc.velocityArray(self.motorSpeed3.text), 0)

def setSpeed4(self):
    print("Motor Speed for: ", addressMap[3], "is ", self.motorSpeed4.text)
    print(fc.velocityArray(self.motorSpeed4.text))
    # network.send_message(addressMap[3], fc.velocityArray(-(self.motorSpeed4.text)), 0)

def setSpeedAll(self):
    # Enable operation and set target velocity
    # Enable operation command: 0x0F
    print("Speed set for all")
    # network.send_message(addressMap[0], fc.velocityArray(motorSpeed1), 0)
    # network.send_message(addressMap[1], fc.velocityArray(-motorSpeed2), 0)
    # network.send_message(addressMap[2], fc.velocityArray(motorSpeed3), 0)
    # network.send_message(addressMap[3], fc.velocityArray(-motorSpeed4), 0)