	.section .text
	.global start
start:
	la	a0, 0x20000000
	lw	a1, 0x548(a0)
	ori	a1, a1, 1
	sw	a1, 0x548(a0)
	j	.
