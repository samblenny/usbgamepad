# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# usb-gamepad
#
# Interesting vendor:product IDs:
#  045e:028e  XInput Gamepad (*many* gamepads and adapters match this)
#  2dc8:3107  8BitDo 8BitDo USB Wireless Adapter 2 (idle, no connection)
#
# The 8BitDo adapter switches vendor and product IDs when it has a connection
# to a Bluetooth gamepad. When idle, it presents as 2dc8:3107. When connected,
# it presents as 045e:028e (unless you set it to some other mode?).
#
import usb

print("\n\n## Compare dir(usb) between Bookworm and CircuitPython\n")
print("dir(usb.core) [circuitpython usb]:")
for n in sorted(["find", "Device", "USBError", "USBTimeoutError"]):
    print("  %s" % n)
print()
print("dir(usb.core) [bookworm python3-usb]:")
names = sorted([n for n in dir(usb.core) if not n.startswith("_")])
for n in names:
    print("  %s" % n)

print("\n\n## Dump info on connected USB devices\n")
devices = list(usb.core.find(find_all=1))
skip = ["backend", "manufacturer", "product", "serial_number", "parent"]
for d in devices:
    print("\n" + "=" * 60)
    print(f"=== {d.idVendor:04x}:{d.idProduct:04x} ======" + ("=" * 40))
    print("=" * 60)
    names = [n for n in dir(d) if not (n.startswith("_") or (n in skip))]
    for n in names:
        val = ""
        try:
            val = getattr(d, n)
        except ValueError as e:
            val = e
        T = type(val)
        if T in [int, list, tuple]:
            print("[%s]:" % n, val)
        elif T == usb.core.Device:
            print("[%s]:\n" % n, val)
        elif callable(val):
            print("[%s]: <callable>" % n)
        else:
            print("[%s, %s]:" % (n, T), val)
