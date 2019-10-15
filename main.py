import canopen
import MainWindow
import PIDWindow
import DataWindow
import ApplicationManager
from kivy.app import App
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty

liveSig = [None, None, None, None]
curSig = [None, None, None, None]
posSig = [None, None, None, None]

motorSpeed1 = ObjectProperty(None)
motorSpeed2 = ObjectProperty(None)
motorSpeed3 = ObjectProperty(None)
motorSpeed4 = ObjectProperty(None)

# network = canopen.Network()
# network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)

kv = Builder.load_file("MainDesign.kv")
Builder.load_file("DataDesign.kv")
Builder.load_file("PIDDesign.kv")

class RobuROC(App):
    def build(self):
        self.icon = 'kivy.jpg'
        return kv

if __name__ == '__main__':
    RobuROC().run()