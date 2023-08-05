import bz2
import logging

from construct import *

from simpleelf.elf_structs import ElfStructs
from simpleelf.elf_builder import ElfBuilder
from simpleelf import elf_consts

from packers.utils import get_elf_from_code

elf_structs = ElfStructs('>')

MAGIC = b'MZIP'

mzip_struct = Struct(
    'magic' / Const(MAGIC),
    
    Seek(0x38),
    'data_offset' / Hex(Int32ub),
    'entry' / Hex(Int32ub),
    'unknown0' / Int32ub,
    'compressed_size' / Hex(Int32ub),


    Seek(this.data_offset),
    'compressed_data' / Bytes(this.compressed_size),
    'comment' / GreedyBytes,
)

def unpack(fw, out):
    logging.debug('attempting MZIP packer')

    header_magic = MAGIC
    is_mzip = header_magic == fw.read(len(header_magic))
    fw.seek(0)

    if not is_mzip:
        logging.debug('not an MZIP file')
        return False

    logging.info('extracting MZIP packed file')

    mzip = mzip_struct.parse_stream(fw)

    e = get_elf_from_code(bz2.decompress(mzip.compressed_data), mzip.entry)
    out.write(e.build())

    logging.info('extracted successfully')
    return True
