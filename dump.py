# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# Dump formatted events from Linux /dev/input/js0 (a USB gamepad)
#
import struct
import time


# Gamepad layout: cluster style is A on the right
digital = {
    "A": 1,
    "B": 0,
    "X": 3,
    "Y": 2,
    "Select": 6,
    "Start": 7,
    "Home": 8,
    "L": 4,
    "R": 5,
    "LHat": 9,
    "RHat": 10,
    }
digital_inv = {v: k for (k, v) in digital.items()}
analog = {    # Each analog axis is a signed 16-bit integer
    "LX": 0,     # +right -left
    "LY": 1,     # +down  -up
    "L2": 2,     # pull=-32767 release=32767
    "RX": 3,     # +right -left
    "RY": 4,     # +down  -up
    "R2": 5,     # pull=-32767 release=32767
    "dPadX": 6,  # L=-32676  R=32767  center=0
    "dPadY": 7,  # Up=-32767 Dn=32767 center=0
    }
analog_inv = {v: k for (k, v) in analog.items()}
# Event type constants for regular events (ignore 129 and 130 startup events)
DIG = 1
AN = 2

def name(val, type_, number):
    """Return the button or axis name for an event"""
    if type_ == DIG:
        return digital_inv[number]
    elif type_ ==  AN:
        axis = analog_inv[number]
        if axis == 'dPadX':
            if val < 0:
                return axis + ": Left"
            elif val > 0:
                return axis + ": Right"
        elif axis == 'dPadY':
            if val < 0:
                return axis + ": Up"
            elif val > 0:
                return axis + ": Down"
        return axis
    else:
        return '?'

def main():
    """Print events from js0 until Home button is pressed"""
    print("Opening /dev/input/js0...")
    print("press gamepad Home button to exit")
    with open("/dev/input/js0", "rb") as f:
        # discard initial values
        time.sleep(0.2)
        _ = f.read(len(f.peek()))
        # Now watch for new input
        while True:
            (time_, val, type_, number) = struct.unpack("<IhBB", f.read(8))
            print(f"{time_:10d} {val:7d} {type_:d} {number:2d}",
                name(val, type_, number))
            # stop if the home button was pressed
            if (val, type_, number) == (1, DIG, digital["Home"]):
                break

main()
