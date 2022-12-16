## Overview

This is a small tool that runs an ELF executable on Bouffalo Lab SoCs without
touching the flash contents. It communicates with the boot ROM over UART. It is
mostly focused on BL808, but it uses the unmodified image header definitions
from `bflb-mcu-tool`, so it should be easy to extend to other SoCs.

## Usage

Run `loader.py`. Its inputs are the firmware file and a configuration file. The
configuration file sets fields in the boot header, such as clock and CPU setup.
Default files are provided for BL602 and BL808, but they may need to be
adjusted if your MCU has some eFuses set. Fields such as the load and entry
addresses are automatically updated from the ELF file.

The tool uses a safe, slow baud rate by default, but larger values of at least
2 Mbaud are known to work.

See below or run `python3 loader.py --help` for the full help text.

```
usage: loader [-h] [-b BAUD] [-C CFG] [-c {bl602,bl808}] [-p PORT] firmware

Load an ELF to the MCU's RAM and execute it.

positional arguments:
  firmware              ELF executable file path

options:
  -h, --help            show this help message and exit
  -b BAUD, --baud BAUD  Serial port baud rate
  -C CFG, --cfg CFG     Config file with values for boot header fields
  -c {bl602,bl808}, --chip {bl602,bl808}
                        MCU variant connected to the serial port
  -p PORT, --port PORT  Serial port device path

```

## Demo application

This repository also contains demo applications for testing the loader. They do
nothing useful on their own. See the Makefile for more details. The loader
itself is pure Python, and does not require compiling the demo applications.
