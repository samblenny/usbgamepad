<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2024 Sam Blenny -->
# USB Gamepad

This demonstrates a CircuitPython driver for reading XInput USB gamepad events
using the Adafruit USB Host BFF (MAX3421E) and a QT Py ESP32-S3 dev board.

![QT Py ESP32-S3 dev board with gamepad](usbgamepad-qtpys3.jpeg)


## Hardware


### Parts

- Adafruit QT Py S3 with 2MB PSRAM
  ([product page](https://www.adafruit.com/product/5700),
  [learn guide](https://learn.adafruit.com/adafruit-qt-py-esp32-s3))

- Adafruit USB Host BFF for QT Py or Xiao with MAX3421E
  ([product page](https://www.adafruit.com/product/5956),
  [learn guide](https://learn.adafruit.com/adafruit-usb-host-bff))

- (optional) Adafruit microSD Card BFF Add-On for QT Py and Xiao
  ([product page](https://www.adafruit.com/product/5683),
  [learn guide](https://learn.adafruit.com/adafruit-microsd-card-bff))

- Adafruit Header Kit for Feather - 12-pin and 16-pin Female Header Set
  ([product page](https://www.adafruit.com/product/2886))

- Adafruit Stacking Headers for Raspberry Pi Pico - 2 x 20 Pin
  ([product page](https://www.adafruit.com/product/5582))

- Adafruit USB OTG Host Cable - MicroB OTG male to A female
  ([product page](https://www.adafruit.com/product/1099))

- 8BitDo SN30 Pro USB gamepad
  ([product page](https://www.8bitdo.com/sn30-pro-usb-gamepad/))

- Tamiya Universal Plate Set #70157
  (3mm thick, 160x60mm ABS plates with 3mm holes on 5mm grid)

- Small cable ties (zip ties)


### Tools

- Soldering iron

- Solder

- Breadboard (to help with soldering)

- Soldering Vise (Adafruit [#3197](https://www.adafruit.com/product/3197) or
  similar)

- Flush diagonal cutters
  (Adafruit [#152](https://www.adafruit.com/product/152) or similar)


### Pinouts

| ESP32-S3 | MAX3421E | microSD |
| -------- | -------- | ------- |
|       A0 |   5VEN   |         |
|       A1 |   CS     |         |
|       A2 |   IRQ    |         |
|       TX |          |   CS    |
|      SCK |   SCK    |   SCK   |
|       MI |   MISO   |   MISO  |
|       MO |   MOSI   |   MOSI  |


## Assemble the Hardware

If you are unfamiliar with soldering stacking headers, you might want to read:

- [Adafruit Guide To Excellent Soldering](https://learn.adafruit.com/adafruit-guide-excellent-soldering/tools)

- [How To Solder Headers](https://learn.adafruit.com/how-to-solder-headers)

For this build, I included an otherwise unused microSD card BFF board because
it adds some mechanical stability. Also, I might want to use SD cards later. If
you don't care about SD cards, adjust these instructions accordingly (you might
want to select different headers).


### Getting Ready

There are three mildly tricky things about assembling the hardware for this
project:

1. It's easy to assemble Qt Py boards in the wrong orientation. It will help
   to check the learn guides and pay close attention to the silk screen marks.

2. You need to carefully cut the longer header strips into pairs of headers
   that are 7 positions long. For the stacking headers and female headers, you
   can pull out one of the pins and carefully cut the plastic with your flush
   cutters. Once you separate a longer strip into two pieces, you can clean up
   the edges by nibbling away excess material with the flush cutters.

3. The USB Host BFF has a jumper on `A0` which connects to the USB host port 5V
   power enable line. To solder the jumper closed, you will need to orient your
   headers such that you don't block the jumper with plastic. I accomplished
   that by using downward-pointing female headers on my ESP32-S3 board, then
   putting stacking headers on my USB host board with the pins coming out on
   the same side as the `5VEN` jumper.


### Order of Soldering

1. Assemble the microSD BFF with male header pins on a breadboard and solder
   the headers in place

2. Remove the microSD BFF from the breadboard and put a row of stacking header
   onto each row of the microSD board's header pins

3. Being careful of board orientation, put the USB Host BFF onto the pins of
   the stacking headers. Clamp the microSD and USB Host BFF sandwich in a vise,
   then solder the USB Host board's pins. Be sure to solder the `A0` jumper
   closed, but try not to make the blob of solder taller than necessary (to
   avoid mechanical interference with the headers).

4. (optional: trim stacking header pins with flush cutters to match the length
   of regular header pins)

5. Put a row of female header onto each row of the USB Host board's stacking
   header pins

6. Being careful of board orientation, put the QT PY ESP32-S3 board on to the
   pins of the female headers and solder them in place


### Smoke Test and Final Assembly

1. Try plugging your board into a USB charger to make sure the LEDs light up

2. If the LEDs light up, unplug the USB power cable, then plug your USB OTG
   host cable into the USB Host BFF's USB port

3. Secure the QT Py board stack and otg cable to a Tamiya Universal Plate with
   cable ties. Trim the ends of the cable ties with your flush cutters.

4. Plug the USB gamepad into the otg cable's USB A port


## Updating CircuitPython

**NOTE: To update CircuitPython on the ESP32-S3 with 2MB PSRAM and 4MB Flash,
you need to use the .BIN file (combination bootloader and CircuitPython core)**

1. Download the CircuitPython 9.1.1 **.BIN** file from the
   [Adafruit QT Py ESP32-S3 4MB Flash/2MB PSRAM](https://circuitpython.org/board/adafruit_qtpy_esp32s3_4mbflash_2mbpsram/)
   page on circuitpython.org

2. Follow the instructions in the
   [Web Serial ESPTool](https://learn.adafruit.com/circuitpython-with-esp32-quick-start/web-serial-esptool)
   section of the "CircuitPython on ESP32 Quick Start" learn guide to update
   your board with CircuitPython 9.1.1. First erasing the board's contents,
   then programming it with the .BIN file. **(CAUTION: the normal UF2 file
   method does not work on this board because it does not have a large enough
   flash drive to hold the CircuitPython UF2 file)**


## Installing CircuitPython Code

To copy the project bundle files to your CIRCUITPY drive:

1. Download the project bundle .zip file using the button on the Playground
   guide or the attachment download link on the GitHub repo Releases page.

2. Expand the zip file by opening it, or use `unzip` in a Terminal. You should
   end up with a folder named prox-sensor-encoder-menu, which should contain a
   `README.txt` file and a `CircuitPython 9.x` folder.

3. Open the CircuitPython 9.x folder and copy all of its contents to your
   CIRCUITPY drive.

To learn more about copying libraries to your CIRCUITPY drive, check out the
[CircuitPython Libraries](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries)
section of the
[Welcome to CircuitPython!](https://learn.adafruit.com/welcome-to-circuitpython)
learn guide.


## Running the Gamepad Demo Code

To see output from `code.py`, you will need to
[connect to the serial console](https://learn.adafruit.com/welcome-to-circuitpython/kattni-connecting-to-the-serial-console)
of your Qt Py board.

When `code.py` starts, it takes several seconds to reset the USB port and
initialize the MAX3421E USB host controller chip. Once that's done, you should
see a message like this:

```
Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.
code.py output:
Resetting USB bus...
USB Host Ready
Looking for USB gamepads...
..
```

With a supported gamepad connected (so far 8BitDo SN30 Pro USB in xinput mode
is the only one I've confirmed to work), you should see these additional
messages, and the gamepad's LED for player 1 should light up:

```
Found an XInput gamepad (045e:028e)...
setting configuration
(     0,     0)  (     0,     0)
```

**NOTE: USB hot plugging may be unreliable. Based on my limited testing, it
seems like there may be bugs in my driver code or in the CircuitPython
`max3421e` package. I got the best results when I plugged the gamepad in before
powering up.**

If you press buttons and move the sticks, you should see additional output with
decoded USB reports for gamepad events (XInput protocol) that like this:

```
(     0,     0)  (     0,     0)  dUp
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  dUp
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  dDn
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  dDn
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  dL
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  dR
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  dL
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  dR
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  B
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  A
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  Start
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  Select
(     0,     0)  (     0,     0)
( -1792,     0)  (     0,     0)
(-22784,     0)  (     0,     0)
(-32768,  2304)  (     0,     0)
(-26624, 32767)  (     0,     0)
( -1024, 32767)  (     0,     0)
( 32767, 24832)  (     0,     0)
( 32767, -1024)  (     0,     0)
(   768,-32768)  (     0,     0)
(-15360,-29440)  (     0,     0)
(     0,     0)  (     0,     0)
(     0,     0)  (-15616,-18688)
(     0,     0)  (-32768,-32768)
(     0,     0)  (-32768,  2304)
(     0,     0)  (-19456, 32767)
(     0,     0)  ( -2560, 32767)
(     0,     0)  ( 23296, 31488)
(     0,     0)  ( 32767,-16128)
(     0,     0)  ( -2560,-32768)
(     0,     0)  (-22016,-22016)
(     0,     0)  (     0,     0)
```

The pairs of numbers in parentheses are (X, Y) coordinates for the left and
right joysticks. The text labels on the right are printed for edge-triggered
transitions (not-pressed to pressed) of the gamepad's buttons. Lines with all
zero coordinates and no button labels get printed when the last button is
released. To see how it works, check out the code and comments in `code.py`.
