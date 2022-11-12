#
# Copyright © 2022 Samuel Holland <samuel@sholland.org>
# SPDX-License-Identifier: MIT
#

CROSS_COMPILE = riscv32-linux-musl-
CC = $(CROSS_COMPILE)cc
LD = $(CROSS_COMPILE)ld

CHIP = bl602
PORT = /dev/ttyUSB0

all: $(CHIP)_app.elf

clean:
	rm -f *.elf *.o

%_app.elf: %_app.ld %_app.o
	$(LD) -o $@ -T $^

%_app.o: %_app.S
	$(CC) -o $@ -c $< -fno-pic -mabi=ilp32 -march=rv32i

run: $(CHIP)_header_cfg.conf $(CHIP)_app.elf
	python loader.py -c $(CHIP) -p $(PORT) -C $^

.PHONY: all clean run
.SECONDARY:
