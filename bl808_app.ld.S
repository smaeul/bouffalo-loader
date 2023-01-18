/*
 * Copyright © 2022 Samuel Holland <samuel@sholland.org>
 * SPDX-License-Identifier: GPL-2.0-only
 */

OUTPUT_ARCH(riscv)
OUTPUT_FORMAT(elf32-littleriscv)

ENTRY (start)

MEMORY {
#ifdef CONFIG_XIP
  RAM (rw): ORIGIN = 0x22020000, LENGTH = 0x00038000
  XIP (rx): ORIGIN = 0x58000000, LENGTH = 0x00100000
#else
  RAM (rwx): ORIGIN = 0x22020000, LENGTH = 0x00038000
#define XIP RAM
#endif
}

SECTIONS {
  .text : ALIGN(16) {
    KEEP(*(.text.start))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.text*)))
  } > XIP

  .rodata : ALIGN(16) {
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.rodata*)))
  } > XIP

  .data : ALIGN(16) {
    __data_flash = LOADADDR(.data);
    __data_start = .;
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.data*)))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.sdata*)))
    __data_end = .;
  } > RAM AT> XIP

  .bss : ALIGN(16) {
    __bss_start = .;
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.sbss*)))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.bss*)))
    __bss_end = .;
  } > RAM

  __stack_start = .;
  . += 0x1000;
  __stack_end = .;
}
