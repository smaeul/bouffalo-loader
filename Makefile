#
# Copyright © 2022 Samuel Holland <samuel@sholland.org>
# SPDX-License-Identifier: MIT
#

CROSS_COMPILE	= riscv32-linux-musl-
CC		= $(CROSS_COMPILE)gcc

CFLAGS		= -ffreestanding \
		  -ffunction-sections \
		  -fno-builtin \
		  -fno-common \
		  -fno-pie \
		  -mabi=ilp32 \
		  -march=rv32i \
		  -O2 \
		  -std=gnu11 \
		  -Wall \
		  -Wextra \
		  -Wno-unused
LDFLAGS		= -no-pie \
		  -nostdlib \
		  -static \
		  -Wl,-O1 \
		  -Wl,--gc-sections \
		  -Wl,--no-dynamic-linker \
		  -Wl,--no-undefined

CHIP		= bl808
PORT		= /dev/ttyUSB0

all: $(CHIP)_app.elf

clean:
	rm -f *.elf *.o

%_app.elf: %_app.ld %_app.c %_app.S
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ -T $^

run: $(CHIP)_header_cfg.conf $(CHIP)_app.elf
	python3 loader.py -c $(CHIP) -p $(PORT) -C $^

.PHONY: all clean run
.SECONDARY:
