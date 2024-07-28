<!-- SPDX-License-Identifier: MIT -->
<!-- SPDX-FileCopyrightText: Copyright 2024 Sam Blenny -->
# Wireshark USB Capture

Goal: See what the Linux kernel gamepad driver does on the USB bus when I
connect a gamepad then open /dev/input/js0 to read some input events.


## Reference Links

- https://wiki.wireshark.org/CaptureSetup/USB
- https://gitlab.com/wireshark/wireshark/-/raw/master/packaging/debian/README.Debian
- https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html


## Debian Bookworm Wireshark Setup

1. `sudo apt install wireshark`        (answer yes to non-root capture option)
2. `sudo adduser $USER wireshark`
3. `sudo modprobe usbmon`                     (not loaded by default)
4. `sudo apt install acl`                     (provides setfacl)
5. `sudo setfacl -m u:$USER:r /dev/usbmon*`   (grant access to usbmon devices)

According to `lsusb -v`, my adapter is plugged into bus 1, of the 3 bus options
on my debian box. So, of the 3 options in Wireshark, I will open usbmon1.


## Capture Procedure

1. Make sure adapter is plugged in and controller is turned off
2. Start wireshark and open usbmon1
3. Turn on controller (which was previously paired with adapter). The adapter
   will switch vid:pid from idle (`2dc8:3107`) to XInput (`045e:028e`)
4. Start dump.py script to connect to /dev/input/js0 and read input events
5. Press some controller buttons
6. Stop script
7. Stop capture
8. Filter out hub packets: `!(usb.addr matches "1\\.[10]\\.[10]")`


## Reading the results

This part happened over about a 1.25 second period after I turned on my
controller so it could pair with the adapter (which had been in idle mode):

1. Host starts by requesting device descriptor, qualifier (no response), and
   configuration. There is 1 configuration which contains 4 interfaces. The
   first interface has an IN endpoint (`0x81`) and an OUT endpoint (`0x02`).
2. After the configuration response, host requests some descriptor strings
3. Host sends a set configuration
4. Host writes to endpoint `0x02` with 3 bytes of data, `0x010302`. This seems
   to be setting the player LEDs status. If I connect additional gamepads, the
   data bytes for this part of the handshake will be `0x010303` for player 2 or
   `0x010304` for player 3. I didn't test what happens for a fourth gamepad.
5. Host reads from endpoint `0x81` (IN), and gamepad responds about 1 ms later
   with URB status `-75` (EOVERFLOW, value too large for defined data type)
6. Host immediately reads again from endpoint `0x81` (IN), and gamepad responds
   about 4 ms later with URB status `0` (Success) and 20 bytes of data:
   `0x0014000000000000000000000000000000000000`
7. This exchange repeats 3 times at the same pace: host reads `0x81`
   immediately after the gamepad's previous response, then gamepand responds
   after 4 ms with 20 bytes of `0x001700...`
8. Then, the host reads one last time from `0x81`, but the gamepad this time
   responds with URB Status `-2` (ENOENT, no such file or directory) and 0
   bytes of data
9. Host writes 3 bytes of data to endpoint `0x02` (OUT): `0x010306`. Then
   gamepad responds about 1 ms later with URB Status `0` (Success). When I add
   additional gamepads, the data bytes at this point in the handshake change to
   `0x010307` for player 2 and `0x010308` for player 3. I did not test what
   happens for a fourth gamepad. This is probably setting the player LEDs to
   a different state than the earlier write to endpoint `0x02`.


This part happened after I started my `dump.py` script to open /dev/input/js0:

1. Host read from endpoint 0x81 (IN) with 0 bytes of data and gamepad responded
   after about 1 ms with URB status -75 (EOVERFLOW)
2. Host immediately read again from endpoint 0x81 (IN) with 0 bytes of data,
   then gamepad responded 4 ms later with URB status 0 (Success) and 20 bytes
   of data: 0x0014000000000000000000000000000000000000
3. Host continues reading from endpoint 0x81 at the 4 ms pace set by the
   gamepad's responses
4. Eventually the gamepad's response data changed as I mashed buttons.

With a filter for
`usb.capdata != 00:14:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00:00`,
I found the following additional response values:
- 0x0014002000000000000000000000000000000000
- 0x0014001000000000000000000000000000000000
- 0x0014008000000000000000000000000000000000
- 0x0014004000000000000000000000000000000000
- 0x0014000400000000000000000000000000000000
