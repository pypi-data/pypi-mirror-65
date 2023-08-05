import bz2
import logging

from construct import *

MAGIC = b'RV'

rv_struct = Struct(
    'magic' / Const(MAGIC),
    Seek(0x2c),
    'elf_size' / Int32ub,

    'unknown0' / Int32ub,
    'unknown1' / Int32ub,
    'unknown2' / Int32ub,
    'unknown3' / Int32ub,

    'elf' / Bytes(this.elf_size),
)

def unpack(fw, out):
    logging.debug('attempting RV packer')
    main_image = fw.read()

    if not main_image.startswith(MAGIC):
        logging.debug('not RV image')
        return False

    rv = rv_struct.parse(main_image)
    out.write(rv.elf)

    logging.info('extracted successfully')
    return True
