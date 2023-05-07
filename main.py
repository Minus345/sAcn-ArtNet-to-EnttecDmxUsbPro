import sacn
import time

from DMXEnttecPro import Controller
from DMXEnttecPro.utils import get_port_by_serial_number, get_port_by_product_id

# provide an IP-Address to bind to if you want to send multicast packets from a specific interface
receiver = sacn.sACNreceiver()
receiver.start()  # start the receiving thread

my_port = get_port_by_serial_number('EN160150A')
my_port = get_port_by_product_id(24577)
dmx = Controller(my_port)

# dmx = Controller('COM8')  # Typical of Windows
# dmx = Controller('/dev/ttyUSB0')  # Typical of Linux

dmxPacket = [0] * 512

receiver.join_multicast(1)


@receiver.listen_on('universe', universe=1)  # listens on universe 1
def callback(packet):  # packet type: sacn.DataPacket
    counter: int = 0
    for x in packet.dmxData:
        dmxPacket[counter] = x
        counter = counter + 1
        #print(dmxPacket)


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
