import signal
import sacn
import sys

from DMXEnttecPro import Controller
from sys import platform
from stupidArtnet import StupidArtnetServer

print("starting")
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
mode = sys.argv[3]
if mode == "artnet" or mode == "sacn":
    print(mode)
else:
    print("use artnet or sacn")
    exit(1)

if platform == "win32":
    # Windows
    print("windows")
    dmx = Controller(sys.argv[1], dmx_size=512)
if platform == "linux" or platform == "linux2":
    # linux
    print("linux")
    dmx = Controller(sys.argv[1], dmx_size=512)

universe: int = int(sys.argv[2])
dmx.set_dmx_parameters(output_rate=0)
dmxPacket = [0] * 512


# ArtNet
def test_callback(data):
    counter1: int = 0
    for x in data:
        dmxPacket[counter1] = x
        counter1 = counter1 + 1


if mode == "sacn":
    receiver = sacn.sACNreceiver()
    receiver.start()
    receiver.join_multicast(universe)

if mode == "artnet":
    a = StupidArtnetServer()
    u1_listener = a.register_listener(
        universe, callback_function=test_callback)


# sacn
@receiver.listen_on('universe', universe=universe)  # listens on universe 1
def callback(packet):  # packet type: sacn.DataPacket
    counter2: int = 0
    for x in packet.dmxData:
        dmxPacket[counter2] = x
        counter2 = counter2 + 1


def handler(signum, frame):
    receiver.stop()
    exit(1)


signal.signal(signal.SIGINT, handler)

# main loop
while True:
    counter: int = 1
    for x in dmxPacket:
        dmx.set_channel(counter, x)
        counter = counter + 1
    dmx.submit()
    print(dmxPacket)
    print("send")
