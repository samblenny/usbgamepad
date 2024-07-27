# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Sam Blenny

.PHONY: help run dump

help:
	@echo "run the module: make run"

run:
	python3 usbgamepad.py

# dump /dev/input/js0 events
dump:
	python3 dump.py
