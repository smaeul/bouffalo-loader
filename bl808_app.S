/*
 * Copyright © 2022 Samuel Holland <samuel@sholland.org>
 * SPDX-License-Identifier: GPL-2.0-only
 */

#define BIT(n)				(1 << (n))

#define GLB_BASE			0x20000000
#define UART0_BASE			0x2000a000

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

	// Disable UART0 interrupts
	la	a0, UART0_BASE
	sw	zero, 0x2c(a0)

	// Clear UART0 FIFOs and disable DMA
	li	a1, BIT(3) | BIT(2)
	sw	a1, 0x80(a0)

	// Configure UART0 for free running mode
	lw	a2, 0(a0)
	ori	a2, a2, 0x3
	xori	a2, a2, 0x2
	sw	a2, 0(a0)

	// Send a message out on UART0
	li	a6, -10

3:
	la	a2, message

2:
	lbu	a1, 0(a2)
	beqz	a1, 9f

1:
	lw	a3, 0x84(a0)
	andi	a3, a3, 0x3f
	beqz	a3, 1b

	sw	a1, 0x88(a0)
	addi	a2, a2, 1
	j	2b

9:
	addi	a6, a6, 1
	bnez	a6, 3b
#endif

	// Reset the MCU
	li	a0, GLB_BASE
	lw	a1, GLB_SWRST_CFG2_OFFSET(a0)
	ori	a1, a1, 1
	sw	a1, GLB_SWRST_CFG2_OFFSET(a0)
	j	.

	.section .rodata
message:
	.asciz "Hello, world!\r\n"
