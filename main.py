import canopen
import MainWindow
import PIDWindow
import DataWindow
import can
import time
from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
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

MainWindow.MainScreen
PIDWindow.PIDScreen
DataWindow.DataScreen

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


kv = Builder.load_file("MainWindow.kv")
Builder.load_file("DataWindow.kv")
Builder.load_file("PIDWindow.kv")

class RobuROC(App):
    def build(self):
        self.icon = 'kivy.jpg'
        return kv

if __name__ == '__main__':
    RobuROC().run()
