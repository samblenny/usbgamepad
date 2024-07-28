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


def start_xpad(device):
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
        sleep(0.030)  # aim for about 30 Hz
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
                print(' '.join(['%02x' % b for b in data]))
                prev = data
            # Stop if home button pressed
            if data[3] & 0x04 != 0:
                return
        except core.USBError as e:
            print(e)

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
