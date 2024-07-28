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


# This calls usb.core.find() in a way that only works correctly if you have
# just one connected gamepad (for more, it needs a find_all=True argument)
print("Looking for USB gamepads...")
idle_adapter = core.find(idVendor=0x2dc8, idProduct=0x3107)
gamepad = core.find(idVendor=0x045e, idProduct=0x028e)
if idle_adapter:
    print("\nFound an 8BitDo Adapter in idle mode (2dc8:3107)\n")
    print(idle_adapter)
if gamepad:
    print("\nFound an XInput gamepad (045e:028e)")
    print(gamepad)
else:
    print("\nIt seems no gamepads are currently connected")
