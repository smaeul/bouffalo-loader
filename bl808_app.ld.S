/*
 * Copyright © 2022 Samuel Holland <samuel@sholland.org>
 * SPDX-License-Identifier: GPL-2.0-only
 */

OUTPUT_ARCH(riscv)
OUTPUT_FORMAT(elf32-littleriscv)

ENTRY (start)

MEMORY {
  RAM (rwx): ORIGIN = 0x22020000, LENGTH = 0x38000
}

SECTIONS {
  . = ORIGIN(RAM);

  .text . : ALIGN(16) {
    KEEP(*(.text.start))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.text*)))
    . = ALIGN(16);
  } > RAM

  .rodata . : ALIGN(16) {
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.rodata*)))
    . = ALIGN(16);
  } > RAM

  .data . : ALIGN(16) {
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.data*)))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.sdata*)))
    . = ALIGN(16);
  } > RAM

  .bss . : ALIGN(16) {
    __bss_start = .;
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.sbss*)))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.bss*)))
    . = ALIGN(16);
    __bss_end = .;
  } > RAM

  __stack_start = .;
  . += 0x1000;
  __stack_end = .;
}
