import canopen
import can
import time
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout

addressMap = {
    0: 0x301,
    1: 0x302,
    2: 0x303,
    3: 0x304
}

motorSpeed = {
    1: None,
    2: None,
    3: None,
    4: None
}

motorSpeed1 = ObjectProperty(None)
motorSpeed2 = ObjectProperty(None)
motorSpeed3 = ObjectProperty(None)
motorSpeed4 = ObjectProperty(None)

liveSig = [None, None, None, None]
curSig = [None, None, None, None]
posSig = [None, None, None, None]

network = canopen.Network()

network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)


def velocityArray(value):
    data = [0x0F, 0]
    tempSpeed = int(value).to_bytes(4, byteorder="little", signed=True)
    return data + list(tempSpeed)

def readData(canid, data, timestamp):
    print( str(canid) + ":" + str( int.from_bytes(data, byteorder='little', signed=True)))

def enable():
    # Enable drive 1 with global NMT command
    # Reset command: 0x01
    for i in range(4):
        network.send_message(0, [0x1, i])

def quickStop():
    # Transitions the drives into quick stop state with a PDO message
    # Quick Stop command: 0x02
    quickStop = [0x02, 0]
    for i in range(4):
        network.send_message(addressMap[i], quickStop, remote=False)

def reset():
    # Reset drive 1 with global NMT command
    # Reset command: 0x81
    for i in range(4):
        network.send_message(0, [0x81, i])
        time.sleep(.2)

def disableVoltage():
    # Disable all drives with PDO message
    # To disable the voltage the drive must be in quick stop state
    # Disable Voltage command: 0x00
    disVoltage = [0x0, 0]
    for i in range(4):
        network.send_message(addressMap[i], disVoltage, remote=False)

def shutDown():
    # Shutdown the drives with a PDO message
    # Shutdown command: 0x06
    data = [0x06, 0]
    for i in range(4):
        print(i)
        network.send_message(addressMap[i], data, remote=False)

def startPeriodic(self):
    # RTR - Live Signal Drives
#        for i in range(0, 4):
#            liveSig[0] = network.send_periodic(1793 + i, 8, .1, remote=True)
#            network.subscribe(1793 + i, readData)

    #RTR - Actual Current
    for i in range(0, 4):
        curSig[i] = network.send_periodic(897 + i, 8, .1, remote=True)
        network.subscribe(897 + i, readData)

    #RTR - Actual Position
#        for i in range(0, 4):
#            posSig[0] = network.send_periodic(913 + i, 8, .1, remote=True)
#            network.subscribe(913 + i, readData)

def stopPeriodic(self):
    print("Stop periodic messages")

    for i in range(0, 4):
        #posSig[i].stop()
        curSig[i].stop()
        #liveSig[i].stop()



class MainWindow(Screen):

    def forward(self):
        print("Moving forward")
        Speed = 1500000
        network.send_message(addressMap[0], velocityArray(Speed), 0)
        network.send_message(addressMap[1], velocityArray(-(Speed)), 0)
        network.send_message(addressMap[2], velocityArray(Speed), 0)
        network.send_message(addressMap[3], velocityArray(-(Speed)), 0)

    def backward(self):
        print("Moving backward")
        Speed = 1500000
        network.send_message(addressMap[0], velocityArray(-Speed), 0)
        network.send_message(addressMap[1], velocityArray(Speed), 0)
        network.send_message(addressMap[2], velocityArray(-Speed), 0)
        network.send_message(addressMap[3], velocityArray(Speed), 0)

    def moveLeft(self):
        print("Moving left")
        Speed = 750000
        network.send_message(addressMap[0], velocityArray(-Speed), 0)
        network.send_message(addressMap[1], velocityArray(-Speed), 0)
        network.send_message(addressMap[2], velocityArray(-Speed), 0)
        network.send_message(addressMap[3], velocityArray(-Speed), 0)

    def moveRight(self):
        print("Moving right")
        Speed = 750000
        network.send_message(addressMap[0], velocityArray(Speed), 0)
        network.send_message(addressMap[1], velocityArray(Speed), 0)
        network.send_message(addressMap[2], velocityArray(Speed), 0)
        network.send_message(addressMap[3], velocityArray(Speed), 0)

    def holdStill(self):
        print("Stopping")
        Speed = 0
        network.send_message(addressMap[0], velocityArray(Speed), 0)
        network.send_message(addressMap[1], velocityArray(-(Speed)), 0)
        network.send_message(addressMap[2], velocityArray(Speed), 0)
        network.send_message(addressMap[3], velocityArray(-(Speed)), 0)

    def setSpeed1(self):
        print("Motor Speed for: ", addressMap[0], "is ", self.motorSpeed1.text)
        print(velocityArray(self.motorSpeed1.text))
        network.send_message(addressMap[1], velocityArray(self.motorSpeed1.text), 0)

    def setSpeed2(self):
        print("Motor Speed for: ", addressMap[1], "is ", self.motorSpeed2.text)
        print(velocityArray(self.motorSpeed2.text))
        network.send_message(addressMap[1], velocityArray(-(self.motorSpeed2.text)), 0)

    def setSpeed3(self):
        print("Motor Speed for: ", addressMap[2], "is ", self.motorSpeed3.text)
        print(velocityArray(self.motorSpeed3.text))
        network.send_message(addressMap[2], velocityArray(self.motorSpeed3.text), 0)

    def setSpeed4(self):
        print("Motor Speed for: ", addressMap[3], "is ", self.motorSpeed4.text)
        print(velocityArray(self.motorSpeed4.text))
        network.send_message(addressMap[3], velocityArray(-(self.motorSpeed4.text)), 0)

    def setSpeedAll(self):
        # Enable operation and set target velocity
        # Enable operation command: 0x0F
        print("Speed set for all")
        network.send_message(addressMap[0], velocityArray(motorSpeed1), 0)
        network.send_message(addressMap[1], velocityArray(-motorSpeed2), 0)
        network.send_message(addressMap[2], velocityArray(motorSpeed3), 0)
        network.send_message(addressMap[3], velocityArray(-motorSpeed4), 0)

    def appReset(self):
        reset()

    def appQuickStop(self):
        quickStop()

    def appEnable(self):
        enable()

    def appDisableVoltage(self):
        disableVoltage()

    def appShutDown(self):
        shutDown()

class PIDWindow(Screen):
    pass


class DataWindow(Screen):
    def dataStarPeriodic(self):
        startPeriodic(self)

    def dataStopPeriodic(self):
        stopPeriodic(self)






class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

    def do_layout(self, *args, **kwargs):
        super(WindowManager, self).do_layout()
        width, height = Window.size
        if width < 800:
            Window.size = 800, Window.size[1]
        if height < 480:
            Window.size = Window.size[0], 480


kv = Builder.load_file("design.kv")


class RobuROC(App):
    def build(self):
        self.icon = 'kivy.jpg'
        return kv


if __name__ == '__main__':
    RobuROC().run()
