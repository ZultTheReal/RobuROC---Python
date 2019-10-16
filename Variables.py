import canopen
import datetime

liveSig = [None, None, None, None]
curSig = [None, None, None, None]
posSig = [None, None, None, None]

curCanID = [897, 898, 899, 900]
posCanID = [913, 914, 915, 916]

now = datetime.datetime.now()

currentScaling = (pow(2, 13))/40

curfilename = "logs/Current/Current_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
currentmeasurements = open(curfilename, "a+")

posfilename = "logs/Position/Position_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
postionmeasurements = open(posfilename, "a+")

addressMap = {
    0: 0x301,
    1: 0x302,
    2: 0x303,
    3: 0x304
}

globalspeed = 1500000

network = canopen.Network()
network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)