#
# Copyright © 2022 Samuel Holland <samuel@sholland.org>
# SPDX-License-Identifier: MIT
#

CROSS_COMPILE	= riscv32-linux-musl-
CC		= $(CROSS_COMPILE)gcc
OBJCOPY		= $(CROSS_COMPILE)objcopy

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
CHIPS		= bl602 bl808
PORT		= /dev/ttyUSB0
BAUD		= 2000000

all: $(foreach chip,$(CHIPS),$(chip)_app.bin)

clean:
	rm -f *.bin *.elf *.ld *.o

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@

%.ld: %.ld.S
	$(CC) $(CFLAGS) -o $@ -E -P $^

%_app.elf: %_app.ld %_app.c %_app.S
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ -T $^

run: $(CHIP)_header_cfg.conf $(CHIP)_app.elf
	python3 loader.py -c $(CHIP) -p $(PORT) -b $(BAUD) -C $^

.PHONY: all clean run
.SECONDARY:
