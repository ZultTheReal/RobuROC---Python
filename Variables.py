import canopen

liveSig = [None, None, None, None]
curSig = [None, None, None, None]
posSig = [None, None, None, None]

addressMap = {
    0: 0x301,
    1: 0x302,
    2: 0x303,
    3: 0x304
}

globalspeed = 1500000

network = canopen.Network()
network.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=1000000)