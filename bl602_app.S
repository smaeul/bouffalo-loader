	.section .text
	.global start
start:
	la	a0, 0x40000000
	lw	a1, 0x18(a0)
	ori	a1, a1, 1
	sw	a1, 0x18(a0)
	j	.
