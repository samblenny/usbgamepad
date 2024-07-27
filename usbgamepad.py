# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# usb-gamepad
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
devices = usb.core.find()
for d in devices:
    print("====================================================")
    names = [n for n in dir(d) if not n.startswith("_")]
    for n in names:
        val = getattr(d, n)
        T = type(val)
        if T in [int, list]:
            print("[%s]:" % n, val)
        elif T == usb.core.Device:
            print("[%s]:\n" % n, val)
        elif callable(val):
            print("[%s]: <callable>" % n)
        else:
            print("[%s, %s]:" % (n, T), val)
