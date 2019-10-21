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
posSig = [None, None, None, None]
tempSig = [None, None, None, None]

velCanID = [0x371, 0x372, 0x373, 0x374]
curCanID = [0x381, 0x382, 0x383, 0x384]
posCanID = [0x391, 0x392, 0x393, 0x394]

motCur = [0, 0, 0, 0]
motVel = [0, 0, 0, 0]
motPos = [0, 0, 0, 0]

now = datetime.datetime.now()

currentScaling = (pow(2, 13))/40
positionScaling = 1
velocityScaling = (1/(pow(2, 17)/(20000/65536))) * 1.8

curfilename = "logs/Current/Current_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
currentMeasurements = None
motposfilename = "logs/MotPosition/MotorPosition_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
motPositionMeasurements = None
velfilename = "logs/Velocity/Velocity_measurements_" + str(now.strftime("%Y-%m-%d_%H-%M-%S")) + ".txt"
velocityMeasurements = None
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

