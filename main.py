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
    1: 0x301,
    2: 0x302,
    3: 0x303,
    4: 0x304
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

network = canopen.Network()

network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)


def velocityArray(value):
    data = [0x0F, 0]
    tempSpeed = int(value).to_bytes(4, byteorder="little", signed=True)
    return data + list(tempSpeed)

def receiveData():
    print("Received!")

def subscribeNetwork():
    print("Subscribed!")

def testData():
    print("Data available!")


class MainWindow(Screen):

    def forward(self):
        print("Moving forward")
        Speed = 1500000
        network.send_message(addressMap[1], velocityArray(Speed), 0)
        network.send_message(addressMap[2], velocityArray(-(Speed)), 0)
        network.send_message(addressMap[3], velocityArray(Speed), 0)
        network.send_message(addressMap[4], velocityArray(-(Speed)), 0)

    def backward(self):
        print("Moving backward")
        Speed = 1500000
        network.send_message(addressMap[1], velocityArray(-Speed), 0)
        network.send_message(addressMap[2], velocityArray(Speed), 0)
        network.send_message(addressMap[3], velocityArray(-Speed), 0)
        network.send_message(addressMap[4], velocityArray(Speed), 0)

    def moveLeft(self):
        print("Moving left")
        Speed = 750000
        network.send_message(addressMap[1], velocityArray(-Speed), 0)
        network.send_message(addressMap[2], velocityArray(-Speed), 0)
        network.send_message(addressMap[3], velocityArray(-Speed), 0)
        network.send_message(addressMap[4], velocityArray(-Speed), 0)

    def moveRight(self):
        print("Moving right")
        Speed = 750000
        network.send_message(addressMap[1], velocityArray(Speed), 0)
        network.send_message(addressMap[2], velocityArray(Speed), 0)
        network.send_message(addressMap[3], velocityArray(Speed), 0)
        network.send_message(addressMap[4], velocityArray(Speed), 0)

    def holdStill(self):
        print("Stopping")
        Speed = 0
        network.send_message(addressMap[1], velocityArray(Speed), 0)
        network.send_message(addressMap[2], velocityArray(-(Speed)), 0)
        network.send_message(addressMap[3], velocityArray(Speed), 0)
        network.send_message(addressMap[4], velocityArray(-(Speed)), 0)

    def setSpeed1(self):
        print("Motor Speed for: ", addressMap[1], "is ", self.motorSpeed1.text)
        print(velocityArray(self.motorSpeed1.text))
        network.send_message(addressMap[1], velocityArray(self.motorSpeed1.text), 0)

    def setSpeed2(self):
        print("Motor Speed for: ", addressMap[2], "is ", self.motorSpeed2.text)
        print(velocityArray(self.motorSpeed2.text))
        network.send_message(addressMap[2], velocityArray(-(self.motorSpeed2.text)), 0)

    def setSpeed3(self):
        print("Motor Speed for: ", addressMap[3], "is ", self.motorSpeed3.text)
        print(velocityArray(self.motorSpeed3.text))
        network.send_message(addressMap[3], velocityArray(self.motorSpeed3.text), 0)

    def setSpeed4(self):
        print("Motor Speed for: ", addressMap[4], "is ", self.motorSpeed4.text)
        print(velocityArray(self.motorSpeed4.text))
        network.send_message(addressMap[4], velocityArray(-(self.motorSpeed4.text)), 0)

    def setSpeedAll(self):
        # Enable operation and set target velocity
        # Enable operation command: 0x0F
        print("Speed set for all")
        network.send_message(addressMap[1], velocityArray(motorSpeed1), 0)
        network.send_message(addressMap[2], velocityArray(-motorSpeed2), 0)
        network.send_message(addressMap[3], velocityArray(motorSpeed3), 0)
        network.send_message(addressMap[4], velocityArray(-motorSpeed4), 0)

    def enable(self):
        # Enable drive 1 with global NMT command
        # Reset command: 0x01
        network.send_message(0, [0x1, 1])
        network.send_message(0, [0x1, 2])
        network.send_message(0, [0x1, 3])
        network.send_message(0, [0x1, 4])

    def quickStop(self):
        # Transitions the drives into quick stop state with a PDO message
        # Quick Stop command: 0x02
        quickStop = [0x02, 0]
        network.send_message(addressMap[1], quickStop, 0)
        network.send_message(addressMap[2], quickStop, 0)
        network.send_message(addressMap[3], quickStop, 0)
        network.send_message(addressMap[4], quickStop, 0)

    def reset(self):
        # Reset drive 1 with global NMT command
        # Reset command: 0x81
        network.send_message(0, [0x81, 1])
        network.send_message(0, [0x81, 2])
        network.send_message(0, [0x81, 3])
        network.send_message(0, [0x81, 4])


    def disableVoltage(self):
        # Disable all drives with PDO message
        # To disable the voltage the drive must be in quick stop state
        # Disable Voltage command: 0x00
        disVoltage = [0x0, 0]
        network.send_message(addressMap[1], disVoltage, 0)
        network.send_message(addressMap[2], disVoltage, 0)
        network.send_message(addressMap[3], disVoltage, 0)
        network.send_message(addressMap[4], disVoltage, 0)

    def shutDown(self):
        # Shutdown the drives with a PDO message
        # Shutdown command: 0x06
        shutDown = [0x06, 0]
        network.send_message(addressMap[1], shutDown, 0)
        network.send_message(addressMap[2], shutDown, 0)
        network.send_message(addressMap[3], shutDown, 0)
        network.send_message(addressMap[4], shutDown, 0)


class PIDWindow(Screen):
    pass


class DataWindow(Screen):

    def startPeriodic(self):
        # RTR - Live Signal Drives
        liveSig1 = network.send_periodic(1793, 8, .1, remote=True)
        network.send_periodic(1794, 8, .1, remote=True)
        network.send_periodic(1795, 8, .1, remote=True)
        network.send_periodic(1796, 8, .1, remote=True)

        #RTR - Actual Current
        network.send_periodic(897, 8, .1, remote=True)
        network.send_periodic(898, 8, .1, remote=True)
        network.send_periodic(899, 8, .1, remote=True)
        network.send_periodic(900, 8, .1, remote=True)

        #RTR - Actual Position
        network.send_periodic(913, 8, .1, remote=True)
        network.send_periodic(914, 8, .1, remote=True)
        network.send_periodic(915, 8, .1, remote=True)
        network.send_periodic(916, 8, .1, remote=True)

    def stopPeriodic(self):
        print("Stop periodic messages")




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
