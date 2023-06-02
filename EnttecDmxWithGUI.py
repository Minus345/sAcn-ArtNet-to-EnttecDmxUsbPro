# SuperFastPython.com
# example of running a function in another thread
from time import sleep
from threading import Thread
import tkinter as tk
from time import sleep
import sacn
import tkinter as tk
import tkinter.font as tkFont
from tkinter import *
from threading import Thread
from DMXEnttecPro import *
from sys import platform
from stupidArtnet import StupidArtnetServer

dmxPacket = [0] * 512
dataIsEmpty = True
dmx: Controller
running = True


def test_callback(data):
    counter1: int = 0
    for x in data:
        dmxPacket[counter1] = x
        counter1 = counter1 + 1


class App:
    def __init__(self, root):
        self.radio = IntVar()

        self.UsbPortVar = StringVar()
        self.UniverseVar = StringVar()
        self.NoDataText = StringVar()

        self.UsbPort = "Com1"
        self.Universe = 1
        self.mode = "null"

        # setting title
        root.title("Enttec Dmx Pro")
        #root.attributes('-fullscreen', True)
        # setting window size
        width = 480
        height = 320
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        Header = tk.Label(root)
        Header["anchor"] = "center"
        ft = tkFont.Font(family='Times', size=10)
        Header["font"] = ft
        Header["justify"] = "center"
        Header["text"] = "ArtNet / sAcn to Enttec Dmx Usb Pro"
        Header.place(x=0, y=0, width=478, height=32)

        UsbEntry = tk.Entry(root, textvariable=self.UsbPortVar)
        UsbEntry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=13)
        UsbEntry["font"] = ft
        UsbEntry["justify"] = "center"
        UsbEntry.place(x=100, y=50, width=90, height=40)

        UsbPortLabel = tk.Label(root)
        ft = tkFont.Font(family='Times', size=13)
        UsbPortLabel["font"] = ft
        UsbPortLabel["justify"] = "center"
        UsbPortLabel["text"] = "USB Port:"
        UsbPortLabel.place(x=10, y=50, width=90, height=40)

        Mode = tk.Label(root)
        ft = tkFont.Font(family='Times', size=13)
        Mode["font"] = ft
        Mode["justify"] = "center"
        Mode["text"] = "Mode:"
        Mode.place(x=10, y=100, width=90, height=40)

        ButtonSAcn = tk.Radiobutton(root, variable=self.radio, value=1)
        ft = tkFont.Font(family='Times', size=13)
        ButtonSAcn["font"] = ft
        ButtonSAcn["justify"] = "center"
        ButtonSAcn["text"] = "sAcn"
        ButtonSAcn.place(x=110, y=100, width=90, height=40)
        ButtonSAcn["command"] = self.ModeSAcn

        ButtonArtNet = tk.Radiobutton(root, variable=self.radio, value=2)
        ft = tkFont.Font(family='Times', size=13)
        ButtonArtNet["font"] = ft
        ButtonArtNet["justify"] = "center"
        ButtonArtNet["text"] = "ArtNet"
        ButtonArtNet.place(x=220, y=100, width=90, height=40)
        ButtonArtNet["command"] = self.ModeArtNet

        UniverseLable = tk.Label(root)
        ft = tkFont.Font(family='Times', size=13)
        UniverseLable["font"] = ft
        UniverseLable["justify"] = "center"
        UniverseLable["text"] = "Universe:"
        UniverseLable.place(x=10, y=140, width=90, height=40)

        UniverseEntry = tk.Entry(root, textvariable=self.UniverseVar)
        UniverseEntry["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=13)
        UniverseEntry["font"] = ft
        UniverseEntry["justify"] = "center"
        UniverseEntry.place(x=100, y=140, width=90, height=40)

        Start = tk.Button(root)
        Start["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=13)
        Start["font"] = ft
        Start["justify"] = "center"
        Start["text"] = "Start"
        Start.place(x=310, y=140, width=159, height=41)
        Start["command"] = self.thread

        Stop = tk.Button(root)
        Stop["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=13)
        Stop["font"] = ft
        Stop["justify"] = "center"
        Stop["text"] = "Stopp"
        Stop.place(x=310, y=190, width=159, height=41)
        Stop["command"] = self.stop

        self.NoData = tk.Label(root, text="null")
        self.NoData.place(x=10, y=190, width=200, height=40)

    def stop(self):
        global running
        global dmx
        running = False
        dmx.close()
        quit()

    def updateNoData(self, t):
        self.NoData.configure(text=t)

    def ModeSAcn(self):
        print("sAcn")
        self.mode = "sacn"
        self.radio.set(1)

    def ModeArtNet(self):
        print("ArtNet")
        self.mode = "artnet"
        self.radio.set(2)

    def SelectMode(self):
        # sAcn
        if self.mode == "sacn":
            receiver = sacn.sACNreceiver()
            receiver.start()
            receiver.join_multicast(int(self.Universe))

            @receiver.listen_on('universe', universe=int(self.Universe))
            def callback(packet):
                counter2: int = 0
                for x in packet.dmxData:
                    dmxPacket[counter2] = x
                    counter2 = counter2 + 1

        # ArtNet
        if self.mode == "artnet":
            a = StupidArtnetServer()
            u1_listener = a.register_listener(
                int(self.Universe), callback_function=test_callback)

    def thread(self):
        self.Universe = self.UniverseVar.get()
        self.UsbPort = self.UsbPortVar.get()
        self.SelectMode()
        global dmx
        if platform == "win32":
            # Windows
            print("windows")
            dmx = Controller(self.UsbPort, dmx_size=512)
        if platform == "linux" or platform == "linux2":
            # linux
            print("linux")
            dmx = Controller(self.UsbPort, dmx_size=512)

        print("mode: " + self.mode)
        print("univers: " + self.Universe)
        print("port: " + self.UsbPort)

        thread1 = Thread(target=task, args=(self,))
        # run the thread
        thread1.start()
        # wait for the thread to finish
        # print('Waiting for the thread...')


# a custom function that blocks for a moment
def task(self):
    # block for a moment
    sleep(1)
    # display a message
    global dataIsEmpty
    print('This is from another thread')
    while running:
        counter: int = 1
        dmxPacketEmpty = [0] * 512
        if dmxPacket == dmxPacketEmpty:
            dataIsEmpty = True
            App.updateNoData(self, "No Data receiving")
        else:
            App.updateNoData(self, "Data receiving")
        # print(dataIsEmpty)
        for x in dmxPacket:
            dmx.set_channel(counter, x)
            counter = counter + 1
        dmx.submit()
        #print(dmxPacket)
        # print("send"))


root = tk.Tk()
App(root)
root.mainloop()
