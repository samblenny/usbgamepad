# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
"""
usb-gamepad

Interesting vendor:product IDs:
  045e:028e  XInput Gamepad (*many* gamepads and adapters match this)
  2dc8:3107  8BitDo 8BitDo USB Wireless Adapter 2 (idle, no connection)

The 8BitDo adapter switches vendor and product IDs when it has a connection
to a Bluetooth gamepad. When idle, it presents as 2dc8:3107. When connected,
it presents as 045e:028e (unless you set it to some other mode?).

names available in the CircuitPython version of usb.core:
 find Device USBError USBTimeoutError
The full PyUSB version has more classes and methods, but those extra things
won't transfer over to CircuitPython, so I'm ignoring them.
"""
from usb import core
from time import sleep
from struct import unpack


# Button bitmask constants
BTN = {
    'dUp':    0x0001,
    'dDn':    0x0002,
    'dL':     0x0004,
    'dR':     0x0008,
    'Start':  0x0010,
    'Select': 0x0020,
    'LHat':   0x0040,
    'RHat':   0x0080,
    'L':      0x0100,
    'R':      0x0200,
    'Home':   0x0400,
    'B':      0x1000,
    'A':      0x2000,
    'Y':      0x4000,
    'X':      0x8000,
    }

def decode(btn, L2, R2):
    """Decode the button bitfield along with L2 and R2"""
    names = []
    for k in sorted(BTN):
        v = BTN[k]
        if btn & v:
            names.append(k)
    if L2:
        names.append("L2")
    if R2:
        names.append("R2")
    return " ".join(names)

def stick(x, y):
    """Format stick coordinates (each axis is 16-bit signed int)"""
    return "(%6d,%6d)" % (x, y)

def start_xpad(device):
    """Initialize ggamepad and poll for input changes, print updates"""
    interface = 0
    # Tell the linux kernel to let go of this gamepad so we can use it
    if device.is_kernel_driver_active(interface):
        print("detaching kernel driver")
        device.detach_kernel_driver(interface)
    # Make sure that configuration is set (kernel driver usually does this)
    try:
        _ = device.get_active_configuration()
        print("configuration already set")
    except core.USBError:
        print("setting configuration")
        device.set_configuration()
    # Start polling for input events
    prev = None
    while True:
        sleep(0.05)  # aim for about 20 Hz
        # First read after a not having polled for a while will usually give
        # a "[Errno 75] Overflow" exception, but a second read immediately
        # after the error response should normally work. It seems like each
        # read triggers an input scan by the controller which needs about 4 ms
        # to do all it's ADC stuff and whatever. Also, those input scans seem
        # to expire if you don't do another read soon enough.
        try:
            print(device.read(0x81, 64))
        except core.USBError as e:
            pass
        try:
            data = device.read(0x81, 64)  # type is array.array('B')
            if data != prev:
                if (len(data) != 20) or (data[0] != 0) or (data[1] != 0x14):
                    # Skip unexpected responses
                    print(' '.join(['%02x' % b for b in data]))
                    continue
                # Unpack normal responses
                prev = data
                (btn, L2, R2, LX, LY, RX, RY) = unpack('<HBBhhhh', data[2:14])
                print("(%6d,%6d)  (%6d,%6d) " % (LX, LY, RX, RY),
                    decode(btn, L2, R2))
                # Stop if home button pressed
                if btn & BTN['Home']:
                    return
        except core.USBError as e:
            print(e)
            if e.errno == 19:
                # 19 = "No such device (it may have been disconnected)"
                return


"""
Mapping of controls to response bytes:

   L  0014  0001  00  00  0000 0000  0000 0000  00 00 00 00 00 00
   R  0014  0002
Home  0014  0004
   B  0014  0010
   A  0014  0020
   Y  0014  0040
   X  0014  0080
  dU  0014  0100
  dD  0014  0200
  dL  0014  0400
  dR  0014  0800
 Sta  0014  1000
 Sel  0014  2000
  LH  0014  4000
  RH  0014  8000
  L2  0014  0000  ff
  R2  0014  0000  00  ff
LX L  0014  0000  00  00  00fa
LX R  0014  0000  00  00  ff10 
LY U  0014  0000  00  00  ff7f ff18
LY D  0014  0000  00  00  ff7f 00ec
RX L  0014  0000  00  00  0000 0000  00f2
RX R  0014  0000  00  00  0000 0000  ff0e
RY U  0014  0000  00  00  0000 0000  ff7f ff11
RY D  0014  0000  00  00  0000 0000  ff7f 00fa
"""

print("Looking for USB gamepads...")
idle_adapter = core.find(idVendor=0x2dc8, idProduct=0x3107)
gamepad = core.find(idVendor=0x045e, idProduct=0x028e)
if idle_adapter:
    print("\nFound an 8BitDo Adapter in idle mode (2dc8:3107)")
if gamepad:
    print("\nFound an XInput gamepad (045e:028e)")
    start_xpad(gamepad)
else:
    print("\nIt seems no gamepads are currently connected")
