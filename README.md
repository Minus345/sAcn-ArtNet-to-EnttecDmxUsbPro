# sAcn / artnet to EnttecDmxUsbPro

sAcn / artnet to EnttecDmxUsbPro phyton script

Tipp:

- `python -m DMXEnttecPro.utils`  
  find usb Port
- you have to be root

## Used librarys:

- `pip install sacn`
- `pip install DMXEnttecPro`
- `pip install pyserial`
- `pip install stupidartnet`

## Parameters:

- **usbPort:**
    - linux: `/dev/ttyUSB0`
    - windows: `COM4`
- **Universe**
    - Use specific Port form Artnet/sAcn
- **Mode**
    - sacn | artnet 
