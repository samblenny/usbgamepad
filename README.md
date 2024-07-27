<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2024 Sam Blenny -->
# USB Gamepad

**work in progress (alpha)**

Goal: Implement an Xinput gamepad interface using PyUSB on Debian Bookworm to
prepare for porting to CircuitPython's
[usb](https://docs.circuitpython.org/en/latest/shared-bindings/usb/index.html)
package using the
[max3421e](https://docs.circuitpython.org/en/latest/shared-bindings/max3421e/index.html)
back end.


## Hardware

- PC running Debian Bookworm
- USB gamepad ([XInput](https://en.wikipedia.org/wiki/DirectInput#XInput))


## Install PyUSB on Debian Bookworm

```
sudo apt install python3-usb
```


## References

- https://github.com/pyusb/pyusb
- https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
- https://github.com/pyusb/pyusb/blob/master/docs/faq.rst
- https://docs.circuitpython.org/en/latest/shared-bindings/usb/index.html
- https://docs.circuitpython.org/en/latest/shared-bindings/max3421e/index.html
