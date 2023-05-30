import tkinter as tk
import tkinter.font as tkFont
from tkinter import *


class App:

    def __init__(self, root):
        self.text = StringVar()

        # setting title
        root.title("ArtNet / sAcn to Enttec Dmx Usb Pro")
        # setting window size
        width = 1085
        height = 607
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        L1 = tk.Label(root)
        L1["anchor"] = "center"
        ft = tkFont.Font(family='Times', size=10)
        L1["text"] = "ArtNet / sAcn to Enttec Dmx Usb Pro"
        L1.place(x=0, y=0, width=1086, height=71)

        self.M1 = Message(root, text=self.text.get())
        ft = tkFont.Font(family='Times', size=10)
        self.M1.place(x=120, y=150, width=244, height=76)

    def editM1(self, t):
        print(t)
        self.text = t
        self.M1.configure(text=t)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    app.editM1("hi")
    root.mainloop()
