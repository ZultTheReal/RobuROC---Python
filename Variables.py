import canopen
import datetime

appOpen = True

network = canopen.Network()
network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)

logging = False

driveReady = False

maxSpeed = 1500000;

motorSpeed = {
    0: 0,
    1: 0,
    2: 0,
    3: 0
}

addressMap = {
    1: 0x301,
    2: 0x302,
    3: 0x303,
    4: 0x304
}

globalspeed = 1500000

liveSig = [None, None, None, None]
curSig = [None, None, None, None]
velSig = [None, None, None, None]

curCanID = [897, 898, 899, 900]
velCanID = [913, 914, 915, 916]

motCur = [0, 0, 0, 0]
motVel = [0, 0, 0, 0]

now = datetime.datetime.now()

currentScaling = (pow(2, 13))/40
velocityScaling = (1/3688000) * 3.14 * 0.5740

velfilename = "logs/Velocity/Velocity_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
velocityMeasurements = None
curfilename = "logs/Current/Current_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
currentMeasurements = None
posfilename = "logs/Position/Position_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
positionMeasurements = None
dirfilename = "logs/Direction/Direction_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
directionMeasurements = None




addressMap = {
    0: 0x301,
    1: 0x302,
    2: 0x303,
    3: 0x304
}

