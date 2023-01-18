/*
 * Copyright © 2022 Samuel Holland <samuel@sholland.org>
 * SPDX-License-Identifier: GPL-2.0-only
 */

#define BIT(n)				(1 << (n))

#define GLB_BASE			0x20000000

#define GLB_UART_CFG0_OFFSET		0x150
#define GLB_UART_CFG1_OFFSET		0x154

#define GLB_SWRST_CFG2_OFFSET		0x548

#define GLB_GPIO_CFG0_OFFSET		0x8c4
#define GLB_GPIO_CFG11_OFFSET		0x8f0
#define GLB_GPIO_CFG12_OFFSET		0x8f4
#define GLB_GPIO_CFG13_OFFSET		0x8f8

#define GPIO_BASE			(GLB_BASE + GLB_GPIO_CFG0_OFFSET)
#define GPIO_CFG0_OFFSET		(GLB_GPIO_CFG0_OFFSET  - GLB_GPIO_CFG0_OFFSET)
#define GPIO_CFG11_OFFSET		(GLB_GPIO_CFG11_OFFSET - GLB_GPIO_CFG0_OFFSET)
#define GPIO_CFG12_OFFSET		(GLB_GPIO_CFG12_OFFSET - GLB_GPIO_CFG0_OFFSET)
#define GPIO_CFG13_OFFSET		(GLB_GPIO_CFG13_OFFSET - GLB_GPIO_CFG0_OFFSET)

	.section .text
	.global start
start:
#ifdef CONFIG_XIP
	la	a0, __data_start
	la	a1, __data_end
	la	a3, __data_flash
1:	lw	a2, 0(a3)
	sw	a2, 0(a0)
	addi	a0, a0, 4
	addi	a3, a3, 4
	blt	a0, a1, 1b
#endif

	la	a0, __bss_start
	la	a1, __bss_end
1:	sw	zero, 0(a0)
	addi	a0, a0, 4
	blt	a0, a1, 1b

	li	a0, GPIO_BASE

#if 0
	// Set GPIO11-13 function to GPIO and enable output
	li	a1, (11 << 8) | BIT(6)
	sw	a1, GPIO_CFG11_OFFSET(a0)
	sw	a1, GPIO_CFG12_OFFSET(a0)
	sw	a1, GPIO_CFG13_OFFSET(a0)

	li	a3, BIT(24)
	xori	a4, a3, -1

	// Send a counter pattern out on GPIO11-13
	li	a6, -100

2:
	slli	a2, a6, 24
	and	a2, a2, a3
	lw	a1, GPIO_CFG11_OFFSET(a0)
	and	a1, a1, a4
	or	a1, a1, a2
	sw	a1, GPIO_CFG11_OFFSET(a0)

	slli	a2, a6, 23
	and	a2, a2, a3
	lw	a1, GPIO_CFG12_OFFSET(a0)
	and	a1, a1, a4
	or	a1, a1, a2
	sw	a1, GPIO_CFG12_OFFSET(a0)

	slli	a2, a6, 22
	and	a2, a2, a3
	lw	a1, GPIO_CFG13_OFFSET(a0)
	and	a1, a1, a4
	or	a1, a1, a2
	sw	a1, GPIO_CFG13_OFFSET(a0)

	li	a5, 5708 // 1ms
1:
	addi	a5, a5, -1
	bnez	a5, 1b

	addi	a6, a6, 1
	bnez	a6, 2b
#endif

#if 1
	// Set GPIO12 function to UART0, output enable
	li      a1, (7 << 8) | BIT(6)
	sw	a1, GPIO_CFG12_OFFSET(a0)

	// Set GPIO13 function to UART0, input and pull up enable
	li      a1, (7 << 8) | BIT(4) | BIT(0)
	sw	a1, GPIO_CFG12_OFFSET(a0)

	// Enable UART clock
	li	a0, GLB_BASE
	lw	a1, GLB_UART_CFG0_OFFSET(a0)
	ori	a1, a1, BIT(4)
	sw	a1, GLB_UART_CFG0_OFFSET(a0)

	// Mux GPIO12 to UART0 TXD, GPIO13 to UART0 RXD
	li	a1, (3 << 4) | (2 << 0)
	sw	a1, GLB_UART_CFG1_OFFSET(a0)

#endif

	la	sp, __stack_end
	jal	main

	// Reset the MCU
	li	a0, GLB_BASE
	lw	a1, GLB_SWRST_CFG2_OFFSET(a0)
	ori	a1, a1, 1
	sw	a1, GLB_SWRST_CFG2_OFFSET(a0)
	j	.
