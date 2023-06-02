import signal
import sacn
import sys
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from threading import Thread
from time import sleep

from DMXEnttecPro import Controller
from sys import platform
from stupidArtnet import StupidArtnetServer

import Gui2
from Gui import App


# ArtNet
def test_callback(data):
    counter1: int = 0
    for x in data:
        dmxPacket[counter1] = x
        counter1 = counter1 + 1


def handler(signum, frame):
    receiver.stop()
    exit(1)


def returnData():
    return dataIsEmpty


def threaded_function():
    print("running")
    #root = tk.Tk()
    #app = App(root)
    #app.editM1(mode)
    #app.editUnivers(str(universe))
    #app.setEmptyLable(str(dataIsEmpty))
    #app.Refresher()
    #root.mainloop()


def startThreadForGUI():
    thread = Thread(target=threaded_function)
    thread.start()
    # thread.join()
    # print("thread finished...exiting")


if __name__ == "__main__":
    print("starting")

    signal.signal(signal.SIGINT, handler)
    dataIsEmpty = "null"

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

    # sAcn
    if mode == "sacn":
        receiver = sacn.sACNreceiver()
        receiver.start()
        receiver.join_multicast(universe)


        @receiver.listen_on('universe', universe=universe)
        def callback(packet):
            counter2: int = 0
            for x in packet.dmxData:
                dmxPacket[counter2] = x
                counter2 = counter2 + 1

    # ArtNet
    if mode == "artnet":
        a = StupidArtnetServer()
        u1_listener = a.register_listener(
            universe, callback_function=test_callback)

    startThreadForGUI()

    # main loop
    while True:
        counter: int = 1
        dmxPacketEmpty = [0] * 512
        if dmxPacket == dmxPacketEmpty:
            dataIsEmpty = "True"
        else:
            dataIsEmpty = "False"
        #print(dataIsEmpty)
        for x in dmxPacket:
            dmx.set_channel(counter, x)
            counter = counter + 1
        dmx.submit()
        # print(dmxPacket)
        # print("send")
