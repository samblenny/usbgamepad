# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny
#
# usbgamepad
#
# Hardware:
# - Adafruit QT Py S3 with 2MB PSRAM (#5700)
# - Adafruit USB Host BFF for QT Py or Xiao with MAX3421E (#5956)
# - Adafruit microSD Card BFF Add-On for QT Py and Xiao (#5683)
# - 8BitDo SN30 Pro USB gamepad
#
# Pinouts:
#   ESP32S3   MAX3421E   microSD
#        A0    5VEN
#        A1    CS
#        A2    IRQ
#        TX               CS
#       SCK    SCK        SCK
#        MI    MISO       MISO
#        MO    MOSI       MOSI
#
from board import A0, A1, A2, NEOPIXEL, NEOPIXEL_POWER, SPI, TX
from digitalio import DigitalInOut, Direction
import gc
from max3421e import Max3421E
from neopixel_write import neopixel_write
from struct import unpack
from sys import stdout
from time import sleep
from usb import core


# Gamepad button bitmask constants
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
    # Decode the button bitfield along with L2 and R2
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

def start_xpad(device):
    # Initialize gamepad and poll for input changes, print updates
    interface = 0
    prev14 = bytearray(14)
    buf64 = bytearray(64)
    # Make sure CircuitPython core is not claiming the device
    if device.is_kernel_driver_active(interface):
        print("detaching kernel driver")
        device.detach_kernel_driver(interface)
    # Make sure that configuration is set
    try:
        print("setting configuration")
        device.set_configuration()
    except core.USBError as e:
        print(e)
    # ==========================================================
    # == weird bug workaround: omitting this hangs the device ==
    _ = dir(device)
    # ==========================================================
    # Initial reads may give old data, so drain gamepad's buffer
    for _ in range(8):
        try:
            _ = device.read(0x81, buf64)
        except core.USBError as e:
            if e.errno != 75:
                raise e
    # Start polling for input events
    while True:
        sleep(0.025)  # aim for 30 Hz (8 ms for 2 endpoint reads)
        # For some gamepads, first read after not having polled for
        # a while will usually give a "[Errno 75] Overflow"
        # exception. But, a second read immediately after the error
        # response normally works. For other gamepads (e.g.
        # non-wireless), the first read may return a sucessful
        # response.
        try:
            n = device.read(0x81, buf64)  # type is array.array('B')
        except core.USBError as e:
            if e.errno != 75:
                raise e
            n = device.read(0x81, buf64)
        if n < 14:
            # skip unexpected responses (looking for a 20 byte report)
            continue
        buf14 = buf64[:14]
        if buf14 != prev14:
            # Unpack normal responses
            prev14[:] = buf14
            (btn, L2, R2, LX, LY, RX, RY) = unpack('<HBBhhhh', buf14[2:14])
            print("(%6d,%6d)  (%6d,%6d) " % (LX, LY, RX, RY),
                decode(btn, L2, R2))

def find_and_connect():
    # Attempt to establish a gamepad connection
    print("Looking for USB gamepads...")
    while True:
        gamepad = core.find(idVendor=0x045e, idProduct=0x028e)
        if gamepad:
            print("\nFound an XInput gamepad (045e:028e)...")
            sleep(1)  # Wait briefly to let adapter and USB bus settle
            try:
                return start_xpad(gamepad)
            except core.USBError as e:
                if e.errno == 19:
                    # 19 = "No such device (it may have been disconnected)"
                    print("[Gamepad disconnected]")
                else:
                    print(e)
                return {"lost": True}
        else:
            # If no gamepads are connected, retry at 1 s intervals
            print(".", end='')
            sleep(1)

def main():
    gc.collect()

    # Set Neopixel to dim magenta
    npx = DigitalInOut(NEOPIXEL)
    npxPow = DigitalInOut(NEOPIXEL_POWER)
    npxPow.direction = Direction.OUTPUT
    npxPow.value = True
    neopixel_write(npx, bytearray([0,1,1]))

    # Cycle MAX3421E USB port power
    print("Resetting USB bus...")
    usbEn = DigitalInOut(A0)
    usbEn.direction = Direction.OUTPUT
    usbEn.value = False
    sleep(2)
    usbEn.direction = Direction.INPUT
    sleep(0.01)
    print("Initializing MAX3421E...")
    # Initialize USB
    spi = SPI()
    usbHost = Max3421E(spi, chip_select=A1, irq=A2)
    sleep(2)
    print("USB Host Ready")

    # MAIN EVENT LOOP
    # Establish and maintain a gamepad connection
    while True:
        find_and_connect()  # only returns if connection is lost
        # Let USB bus settle for a bit after a lost connection
        sleep(1.5)
        gc.collect()


main()
