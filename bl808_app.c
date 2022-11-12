/*
 * Copyright © 2022 Samuel Holland <samuel@sholland.org>
 * SPDX-License-Identifier: GPL-2.0-only
 */

#include <stdbool.h>
#include <linux/errno.h>

#define BIT(n)				(1 << (n))
#define GENMASK(h, l)			((0xffffffffU << (l)) & (0xffffffffU >> (31 - (h))))

#define __bf_shf(x)			(__builtin_ffsll(x) - 1)
#define FIELD_GET(_mask, _reg)		(typeof(_mask))(((_reg) & (_mask)) >> __bf_shf(_mask))
#define FIELD_PREP(_mask, _val)		(((typeof(_mask))(_val) << __bf_shf(_mask)) & (_mask))

typedef unsigned int u32;

static inline u32
readl(void *addr)
{
	volatile u32 *ptr = addr;

	return *ptr;
}

static inline void
writel(u32 val, void *addr)
{
	volatile u32 *ptr = addr;

	*ptr = val;
}

struct udevice {
	void *plat_;
};

void *dev_get_plat(const struct udevice *dev)
{
	return dev->plat_;
}

#define GLB_UART_CFG0_OFFSET		0x150
#define GLB_UART_CFG1_OFFSET		0x154

#define GLB_SWRST_CFG2_OFFSET		0x548

#define GLB_GPIO_CFG0_OFFSET		0x8c4
#define GLB_GPIO_CFG11_OFFSET		0x8f0
#define GLB_GPIO_CFG12_OFFSET		0x8f4
#define GLB_GPIO_CFG13_OFFSET		0x8f8

struct bflb_gpio_plat {
	void *base;
};

static struct bflb_gpio_plat gpio_plat = {
	.base = (void *)0x20000000,
};

static struct udevice gpio = {
	.plat_ = &gpio_plat,
};

#define UART_TX_CFG			0x00
#define UART_TX_CFG_TX_BIT_CNT_P		GENMASK(12, 11)
#define UART_TX_CFG_TX_BIT_CNT_D		GENMASK(10,  8)
#define UART_TX_CFG_TX_FRM_EN			BIT(2)
#define UART_TX_CFG_TX_EN			BIT(0)
#define UART_RX_CFG			0x04
#define UART_RX_CFG_RX_BIT_CNT_D		GENMASK(10,  8)
#define UART_RX_CFG_RX_EN			BIT(0)
#define UART_BIT_PRD			0x08
#define UART_BIT_PRD_RX_BIT_PRD			GENMASK(31, 16)
#define UART_BIT_PRD_TX_BIT_PRD			GENMASK(15,  0)
#define UART_FIFO_CFG0			0x80
#define UART_FIFO_CFG0_RX_FIFO_CLR		BIT(3)
#define UART_FIFO_CFG0_TX_FIFO_CLR		BIT(2)
#define UART_FIFO_CFG1			0x84
#define UART_FIFO_CFG1_RX_FIFO_CNT		GENMASK(13,  8)
#define UART_FIFO_CFG1_TX_FIFO_CNT		GENMASK( 5,  0)
#define UART_FIFO_WDATA			0x88
#define UART_FIFO_RDATA			0x8c

#define UART_FIFO_SIZE			32

struct bflb_uart_plat {
	void *base;
};

static int bflb_uart_pending(struct udevice *dev, bool input);

static int bflb_uart_setbrg(struct udevice *dev, int baudrate)
{
	struct bflb_uart_plat *plat = dev_get_plat(dev);

	return -1;
}

static int bflb_uart_getc(struct udevice *dev)
{
	struct bflb_uart_plat *plat = dev_get_plat(dev);

	if (bflb_uart_pending(dev, true) == 0)
		return -EAGAIN;

	return readl(plat->base + UART_FIFO_RDATA);
}

static int bflb_uart_putc(struct udevice *dev, char c)
{
	struct bflb_uart_plat *plat = dev_get_plat(dev);

	while (bflb_uart_pending(dev, false) == UART_FIFO_SIZE)
		/* spin */;

	writel((unsigned char)c, plat->base + UART_FIFO_WDATA);

	return 0;
}

static int bflb_uart_puts(struct udevice *dev, const char *s)
{
	int ret;
	char c;

	while ((c = *s++)) {
		ret = bflb_uart_putc(dev, c);
		if (ret)
			return ret;
	}

	return 0;
}

static int bflb_uart_pending(struct udevice *dev, bool input)
{
	struct bflb_uart_plat *plat = dev_get_plat(dev);
	u32 reg;

	reg = readl(plat->base + UART_FIFO_CFG1);
	if (input)
		return FIELD_GET(UART_FIFO_CFG1_RX_FIFO_CNT, reg);
	else
		return UART_FIFO_SIZE - FIELD_GET(UART_FIFO_CFG1_TX_FIFO_CNT, reg);
}

static int bflb_uart_clear(struct udevice *dev)
{
	struct bflb_uart_plat *plat = dev_get_plat(dev);
	u32 reg;

	reg = readl(plat->base + UART_FIFO_CFG0);
	reg |= UART_FIFO_CFG0_RX_FIFO_CLR | UART_FIFO_CFG0_TX_FIFO_CLR;
	writel(reg, plat->base + UART_FIFO_CFG0);

	return 0;
}

static int bflb_uart_probe(struct udevice *dev)
{
	struct bflb_uart_plat *plat = dev_get_plat(dev);
	u32 reg;

	reg = FIELD_PREP(UART_TX_CFG_TX_BIT_CNT_P, 2) |
	      FIELD_PREP(UART_TX_CFG_TX_BIT_CNT_D, 7) |
	      UART_TX_CFG_TX_FRM_EN |
	      UART_TX_CFG_TX_EN;
	writel(reg, plat->base + UART_TX_CFG);

	reg = FIELD_PREP(UART_RX_CFG_RX_BIT_CNT_D, 7) |
	      UART_RX_CFG_RX_EN;
	writel(reg, plat->base + UART_RX_CFG);

	return 0;
}

static struct bflb_uart_plat uart0_plat = {
	.base = (void *)0x2000a000,
};

static struct udevice uart0 = {
	.plat_ = &uart0_plat,
};

void main(void)
{
	bflb_uart_probe(&uart0);
	bflb_uart_setbrg(&uart0, 115200);
	for (int i = 0; i < 10; ++i)
		bflb_uart_puts(&uart0, "Hello, world!\r\n");

	/* Flush the UART transmission. */
	while (bflb_uart_pending(&uart0, false))
		/* spin */;
}
