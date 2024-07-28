<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2024 Sam Blenny -->
# USB Gamepad

This reads input from an Xinput gamepad (045e:028e) using PyUSB on Debian
Bookworm. The point is to prepare for porting to CircuitPython's
[usb](https://docs.circuitpython.org/en/latest/shared-bindings/usb/index.html)
package using the
[max3421e](https://docs.circuitpython.org/en/latest/shared-bindings/max3421e/index.html)
back end.


## Hardware

- PC running Debian Bookworm
- USB gamepad ([XInput](https://en.wikipedia.org/wiki/DirectInput#XInput),
  045e:028e)


## Install PyUSB on Debian Bookworm

```
sudo apt install python3-usb
```

## Run the Gamepad Event Decoder

```
sudo make run
```

To avoid the sudo above, the solution would be to add a udev rule to grant r/w
permissions based on USB vendor and product ID.


## Example Output

```
$ sudo make run
python3 usbgamepad.py
Looking for USB gamepads...

Found an XInput gamepad (045e:028e)...
configuration already set
(     0,     0)  (     0,     0)
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
( -9472,     0)  (     0,     0)
(-32768, 10240)  (     0,     0)
(-25856, 22528)  (     0,     0)
( 10496, 32256)  (     0,     0)
( 31744, 10240)  (     0,     0)
(     0,     0)  (     0,     0)
(     0,     0)  (     0,-32768)
(     0,     0)  ( -3584,-32768)
(     0,     0)  (-24320,-23808)
(     0,     0)  (-30464, 18688)
(     0,     0)  ( -8192, 32767)
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  L R L2 R2
(     0,     0)  (     0,     0)  L L2
(     0,     0)  (     0,     0)  L2
(     0,     0)  (     0,     0)
(     0,     0)  (     0,     0)  Home
```


## References

- https://github.com/pyusb/pyusb
- https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
- https://github.com/pyusb/pyusb/blob/master/docs/faq.rst
- https://docs.circuitpython.org/en/latest/shared-bindings/usb/index.html
- https://docs.circuitpython.org/en/latest/shared-bindings/max3421e/index.html
