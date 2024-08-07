# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny

.PHONY: help bundle sync tty clean run dump

help:
	@echo "linux gamepad decoder:        make run"
	@echo "linux /dev/input/js0 dumper:  make dump"
	@echo "build project bundle:         make bundle"
	@echo "sync code to CIRCUITPY:       make sync"
	@echo "open serial terminal:         make tty"

# This is for use by .github/workflows/buildbundle.yml GitHub Actions workflow
bundle:
	@mkdir -p build
	python3 bundle_builder.py

# Sync current code and libraries to CIRCUITPY drive on macOS.
sync: bundle
	xattr -cr build
	rsync -rcvO 'build/usbgamepad/CircuitPython 9.x/' /Volumes/CIRCUITPY
	sync

# Start serial terminal at fast baud rate with no flow control (-fn)
tty:
	screen -fn /dev/tty.usbmodem* 115200

clean:
	rm -rf build

run:
	python3 usbgamepad.py

# dump /dev/input/js0 events
dump:
	python3 dump.py
