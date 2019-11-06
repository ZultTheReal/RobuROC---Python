
maxSpeed = 3000000;

# CAN bus IDs for ControlWord
COBID_HOST = 0x05

COBID_CONTROL = [0x201, 0x202, 0x203, 0x204]

# CAN bus IDs for readying velocity and current from motor controllers
COBID_ACT_VELOCITY = [0x371, 0x372, 0x373, 0x374]
COBID_ACT_CURRENT = [0x381, 0x382, 0x383, 0x384]

COBID_TAR_VELOCITY = [0x511, 0x512, 0x513, 0x514]
COBID_TAR_CURRENT = [0x521, 0x522, 0x523, 0x524]

WHEEL_RADIUS = 0.28 # meter

# Constants for transforming int-values read from CAN to actual values
SCALE_CURRENT = pow(2, 13)/40 # to Amps
SCALE_VELOCITY =  ((pow(2,17)/(2*20000)*pow(2,19))/1000)*32 # To RPM
SCALE_RPM_TO_MPS = (2 * 3.14)/60*WHEEL_RADIUS

COBID_SDO = [0x601, 0x602, 0x603, 0x604]
COBID_HEARTBEAT = [0x701, 0x702, 0x703, 0x704]

# Object indexes for configuration
INDEX_HEARTBEAT = 0x1016
SUBINDEX_HEARTBEAT = 1


INDEX_DECELERATION_LIMIT = 0x2062
SUBINDEX_DECELERATION_LIMIT = 4