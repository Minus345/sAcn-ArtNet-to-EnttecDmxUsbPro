# sAcn / artnet to EnttecDmxUsbPro

sAcn / artnet to Enttec Dmx Usb Pro phyton script

### Setup:

Install all the libraries, plug in your Dmx Usb Pro Interface and start the programm.  
For Windows you can use the compiled exe.

### Tipp:

- `python -m DMXEnttecPro.utils`  
  find usb Port
- you have to be root on linux

### Tested on:

- windows 10
- raspberrypi

## Used librarys:

- `pip install sacn`
- `pip install DMXEnttecPro`
- `pip install pyserial`
- `pip install stupidartnet`

## Parameters:

| Parameter |                Name                 |                     Example                      |
|-----------|:-----------------------------------:|:------------------------------------------------:|
| 1         |        Selects the Usb Port         |      linux: `/dev/ttyUSB0` Windows: `COM1`       |
| 2         | Sets the Universe for Artnet / sAcn | Artnet: starting with `0` sAcn starting with `1` |
| 3         |            Sets the mode            |                `sacn` or `artnet`                |
