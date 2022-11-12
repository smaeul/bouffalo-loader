#
# Copyright © 2022 Samuel Holland <samuel@sholland.org>
# SPDX-License-Identifier: MIT
#

import logging
import sys
import time

from argparse               import ArgumentParser
from binascii               import crc32
from configparser           import ConfigParser
from ctypes                 import *
from enum                   import Enum
from hashlib                import sha256
from pathlib                import Path
from typing                 import Optional, Sequence, Tuple

from elftools.elf.elffile   import ELFFile
from elftools.elf.segments  import Segment
from serial                 import Serial

sys.path.append(str(Path(__file__).with_name('bflb-mcu-tool')))

import bflb_mcu_tool.libs.bl602.bootheader_cfg_keys
import bflb_mcu_tool.libs.bl808.bootheader_cfg_keys

logger = logging.getLogger('loader')


class Chip(Enum):
    BL602 = 'bl602'
    BL808 = 'bl808'

    def __str__(self) -> str:
        return self.value


def make_boot_header_fields(chip: Chip):
    def keys_to_tuples() -> Sequence[Tuple[int, int, int, str]]:
        '''
        Convert the dictionary to a sortable sequence of offset/size/name tuples.
        '''
        raw_cfg_keys = {
            Chip.BL602: bflb_mcu_tool.libs.bl602.bootheader_cfg_keys.bootheader_cfg_keys,
            Chip.BL808: bflb_mcu_tool.libs.bl808.bootheader_cfg_keys.bootheader_cfg_keys,
        }

        for name, cfg in raw_cfg_keys[chip].items():
            yield int(cfg['offset']), int(cfg['pos']), int(cfg['bitlen']), name

    def pad_name(bit_start: int, byte_start: int) -> str:
        '''
        Generate a name for a padding field.
        '''
        return f'rsvd_{bit_start}_{byte_start}'

    def tuples_to_fields() -> Sequence[Tuple]:
        '''
        Convert the sorted offset/size/name tuples to a ctypes field list.
        '''
        last_byte_end = 0
        last_bit_end = 0
        for byte_start, bit_start, bit_length, name in sorted(keys_to_tuples()):
            if last_byte_end != byte_start:
                logger.debug(f'{chip.name}: {byte_start - last_byte_end:2d} byte gap before {name}')
                if last_bit_end != 0:
                    pad_length = 32 - last_bit_end
                    yield pad_name(last_byte_end, last_bit_end), c_uint32, pad_length
                    last_byte_end += 4
                    last_bit_end = 0
                while last_byte_end < byte_start:
                    yield pad_name(last_byte_end, last_bit_end), c_uint32
                    last_byte_end += 4
                if last_byte_end != byte_start:
                    logger.error(f'{chip}: byte alignment error at {name}!')
            if last_bit_end < bit_start:
                logger.debug(f'{chip.name}: {bit_start - last_bit_end:2d} bit gap before {name}')
                pad_length = bit_start - last_bit_end
                yield pad_name(last_byte_end, last_bit_end), c_uint32, pad_length
                last_bit_end = bit_start
            if last_bit_end != bit_start:
                logger.error(f'{chip.name}: bit alignment error at {name}!')
            if bit_length < 32:
                yield name, c_uint32, bit_length
            else:
                yield name, c_uint32
            last_bit_end += bit_length
            if last_bit_end > 32:
                logger.error(f'{chip.name}: bit count error at {name}!')
            elif last_bit_end == 32:
                last_byte_end += 4
                last_bit_end = 0

    return tuple(tuples_to_fields())


class BootHeader(Structure):
    @classmethod
    def from_config(cls, path: Path, section: str):
        config = ConfigParser()
        config.read(path)
        h = cls()
        for field, value in config.items(section):
            setattr(h, field, int(value, 0))
        return h

    def __repr__(self) -> str:
        values = ', '.join(f'{f}={v:#x}' for f, v in self._asdict().items())
        return f'{self.__class__.__name__}({values})'

    def _asdict(self) -> dict:
        return {field[0]: getattr(self, field[0]) for field in self._fields_}

    def _pretty_print(self) -> str:
        print(self.__class__.__name__ + ':')
        for field, value in self._asdict().items():
            print(f' {field:30s} = {value:#10x}')

    def check_crc32(self) -> bool:
        return self.crc32 == crc32(bytes(self)[:-4])

    def update_crc32(self):
        cls = type(self)

        start = cls.flashcfg_magic_code.offset + 4
        end = cls.flashcfg_crc32.offset
        self.flashcfg_crc32 = crc32(bytes(self)[start:end])

        start = cls.clkcfg_magic_code.offset + 4
        end = cls.clkcfg_crc32.offset
        self.clkcfg_crc32 = crc32(bytes(self)[start:end])

        self.crc32 = crc32(bytes(self)[:-4])

    def update_hash(self, hash: bytes):
        memmove(byref(self, type(self).hash_0.offset), hash, len(hash))


class BL602BootHeader(BootHeader):
    _fields_ = make_boot_header_fields(Chip.BL602)


class BL808BootHeader(BootHeader):
    _fields_ = make_boot_header_fields(Chip.BL808)


class SegmentHeader(Structure):
    _fields_ = (
        ('address', c_uint32),
        ('length',  c_uint32),
        ('rsvd',    c_uint32),
        ('crc32',   c_uint32),
    )

    @classmethod
    def from_elf_segment(cls, elf_segment: Segment):
        h = cls()
        h.address = elf_segment.header.p_paddr
        h.length = elf_segment.header.p_filesz
        h.update_crc32()
        return h

    def check_crc32(self) -> bool:
        return self.crc32 == crc32(bytes(self)[:-4])

    def update_crc32(self) -> bool:
        self.crc32 = crc32(bytes(self)[:-4])


class ISPCommand(Structure):
    _fields_ = (
        ('cmd',     c_uint8),
        ('rsvd',    c_uint8),
        ('length',  c_uint16),
    )

boot_header_classes = {
    Chip.BL602: BL602BootHeader,
    Chip.BL808: BL808BootHeader,
}

boot_header_sections = {
    Chip.BL602: 'BOOTHEADER_CFG',
    Chip.BL808: 'BOOTHEADER_GROUP0_CFG',
}

MAX_CHUNK_SIZE = 4096


def load_elf_file(chip: Chip, cfg_path: Optional[Path], elf_path: Path, serial_port: Path):
    boot_header_class = boot_header_classes[chip]
    if cfg_path:
        cfg_section = boot_header_sections[chip]
        boot_header = boot_header_class.from_config(cfg_path, cfg_section)
    else:
        boot_header = boot_header_class()

    # Extract the segments from the ELF file.
    with ELFFile(elf_path.open('rb')) as elf_file:
        segments = []
        for elf_segment in elf_file.iter_segments():
            # Skip non-loadable segments.
            if elf_segment.header.p_filesz == 0:
                continue
            segments.append((
                SegmentHeader.from_elf_segment(elf_segment),
                elf_segment.data(),
            ))

        # Generate the SHA-256 hash for the entire loaded image.
        image_hash = sha256()
        for segment_header, data in segments:
            image_hash.update(segment_header)
            image_hash.update(data)

        # Update the boot header from the ELF file.
        if chip == Chip.BL808:
            boot_header.img_len_cnt = len(segments)
            boot_header.m0_boot_entry = elf_file.header.e_entry
        else:
            boot_header.img_len = len(segments)
            boot_header.img_start = elf_file.header.e_entry
        boot_header.update_hash(image_hash.digest())
        boot_header.update_crc32()

    with Serial(str(serial_port), 115200) as serial:
        def send_command(cmd: int, data: bytes):
            serial.write(ISPCommand(cmd=cmd, length=len(data)))
            serial.write(data)
            status = serial.read(2)
            if status != b'OK':
                err = int.from_bytes(serial.read(2), 'little')
                raise Exception(f'Command {cmd:#x} failed: {err:#06x}')
            # Some commands produce a response that must be handled.
            if cmd == 0x17:
                length = int.from_bytes(serial.read(2), 'little')
                if serial.read(length) != data:
                    raise Exception('Unexpected response')

        logger.info('Sending handshake...')
        serial.write(b'U' * 32)
        if chip == Chip.BL808:
            time.sleep(0.1)
            serial.write(bytes.fromhex('5000080038F0002000000018'))
        time.sleep(0.1)
        if serial.read(2) != b'OK':
            raise Exception('Handshake failed')

        logger.info('Sending boot header...')
        send_command(0x11, bytes(boot_header))
        for segment_header, data in segments:
            logger.info(f'Sending segment {segment_header.address:08x}+{segment_header.length:08x}')
            send_command(0x17, bytes(segment_header))
            while data:
                chunk, data = data[:MAX_CHUNK_SIZE], data[MAX_CHUNK_SIZE:]
                send_command(0x18, chunk)

        logger.info('Checking image...')
        send_command(0x19, b'')

        logger.info('Running image...')
        send_command(0x1a, b'')


def main():
    parser = ArgumentParser(prog='loader',
                            description="Load an ELF to the MCU's RAM and execute it.")
    parser.add_argument('-C', '--cfg',
                        help='Config file with values for boot header fields',
                        type=Path)
    parser.add_argument('-c', '--chip',
                        help='MCU variant connected to the serial port',
                        default=Chip.BL808, type=Chip, choices=tuple(Chip))
    parser.add_argument('-p', '--port',
                        help='Serial port device path',
                        default=Path('/dev/ttyS0'), type=Path)
    parser.add_argument('firmware',
                        help='ELF executable file path',
                        type=Path)
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    try:
        load_elf_file(args.chip, args.cfg, args.firmware, args.port)
    except Exception as e:
        logger.exception('Failed to communicate with the MCU')

if __name__ == '__main__':
    main()
