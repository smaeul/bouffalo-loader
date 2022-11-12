OUTPUT_ARCH(riscv)
OUTPUT_FORMAT(elf32-littleriscv)

ENTRY (start)

MEMORY {
  IRAM (x):  ORIGIN = 0x22008000, LENGTH = 0x28000
  DRAM (rw): ORIGIN = 0x42008000, LENGTH = 0x28000
}

SECTIONS {
  . = ORIGIN(IRAM);

  .text . : ALIGN(16) {
    KEEP(*(.text.start))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.text*)))
    . = ALIGN(16);
  } > IRAM

  . += 0x20000000;

  .rodata . : AT(. - 0x20000000) ALIGN(16) {
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.rodata*)))
    . = ALIGN(16);
  } > DRAM

  .data . : AT(. - 0x20000000) ALIGN(16) {
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.data*)))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.sdata*)))
    . = ALIGN(16);
  } > DRAM

  .bss . : AT(. - 0x20000000) ALIGN(16) {
    __bss_start = .;
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.sbss*)))
    *(SORT_BY_ALIGNMENT(SORT_BY_NAME(.bss*)))
    . = ALIGN(16);
    __bss_end = .;
  } > DRAM

  __stack_start = .;
  . += 0x1000;
  __stack_end = .;
}
