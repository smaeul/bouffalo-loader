/*
 * Copyright © 2022 Samuel Holland <samuel@sholland.org>
 * SPDX-License-Identifier: GPL-2.0-only
 */

	.section .text
	.global start
start:
	la	sp, __stack_end
	jal	main

	la	a0, 0x40000000
	lw	a1, 0x18(a0)
	ori	a1, a1, 1
	sw	a1, 0x18(a0)
	j	.
