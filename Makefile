CROSS_COMPILE = riscv32-linux-musl-
AS = $(CROSS_COMPILE)as
LD = $(CROSS_COMPILE)ld

CHIP = bl602

all: $(CHIP)_app.elf

clean:
	rm -f *.elf *.o

%_app.elf: %_app.ld %_app.o
	$(LD) -o $@ -T $^

%_app.o: %_app.s
	$(AS) -o $@ $<

.PHONY: all clean
.SECONDARY:
