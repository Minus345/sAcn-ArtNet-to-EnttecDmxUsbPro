import signal
import sacn
import sys

from DMXEnttecPro import Controller
from DMXEnttecPro.utils import get_port_by_serial_number, get_port_by_product_id
from sys import platform

print("starting")
print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))
# provide an IP-Address to bind to if you want to send multicast packets from a specific interface
receiver = sacn.sACNreceiver()
receiver.start()  # start the receiving thread

if platform == "win32":
    # Windows...
    print("windows")
    dmx = Controller(sys.argv[1], dmx_size=512)
if platform == "linux" or platform == "linux2":
    # linux
    print("linux")
    dmx = Controller(sys.argv[1], dmx_size=512)

# my_port = get_port_by_serial_number('EN160150A')
# my_port = get_port_by_product_id(24577)
# dmx = Controller(my_port, dmx_size=512)

dmx.set_dmx_parameters(output_rate=0)

if not sys.argv[2].isnumeric():
    print("false argument")
    receiver.stop()
    sys.exit(0)

universe: int = int(sys.argv[2])
print(universe)

dmxPacket = [0] * 512

receiver.join_multicast(universe)


@receiver.listen_on('universe', universe=universe)  # listens on universe 1
def callback(packet):  # packet type: sacn.DataPacket
    counter: int = 0
    for x in packet.dmxData:
        dmxPacket[counter] = x
        counter = counter + 1
        # print(dmxPacket)


def handler(signum, frame):
    receiver.stop()
    exit(1)


signal.signal(signal.SIGINT, handler)

while True:
    counter: int = 1
    for x in dmxPacket:
        dmx.set_channel(counter, x)
        counter = counter + 1
    dmx.submit()

    # dmx.set_channel(1, 255)  # Sets DMX channel 1 to max 255
    # dmx.submit()  # Sends the update to the controller
    # time.sleep(1)
    # dmx.set_channel(1, 0)  # Sets DMX channel 1 to max 255
    # dmx.submit()  # Sends the update to the controller
    # time.sleep(1)
