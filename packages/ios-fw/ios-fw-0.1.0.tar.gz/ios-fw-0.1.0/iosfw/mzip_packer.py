import bz2
import logging

from construct import *

from simpleelf.elf_structs import ElfStructs
from simpleelf.elf_builder import ElfBuilder
from simpleelf import elf_consts

from iosfw.utils import guess_machine_type

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

REGIONS_MAGIC = b'\xDE\xAD\x12\x34'

regions_struct = Struct(
    'magic' / Const(REGIONS_MAGIC),

    'unknown0' / Int32ub,
    'unknown1' / Int32ub,
    'unknown2' / Int32ub,
    'unknown3' / Int32ub,
    'unknown4' / Int32ub,

    'text' / Int32ub,
    'data' / Int32ub,
    'bss' / Int32ub,
    'heap' / Int32ub,

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

    e = ElfBuilder()
    e.set_endianity('>')

    main_image = bz2.decompress(mzip.compressed_data)

    regions_struct_offset = main_image.find(REGIONS_MAGIC)
    if -1 == regions_struct_offset:
        logging.warning("failed to locate regions magic. using single .text section")
        e.add_code_section('.text', mzip.entry, main_image)
    else:
        regions = regions_struct.parse(main_image[regions_struct_offset:
            regions_struct_offset+regions_struct.sizeof()])

        e.add_segment(mzip.entry, 
            elf_consts.PF_R | elf_consts.PF_W | elf_consts.PF_X, 
            len(main_image))

        e.add_code_section('.text', regions.text, main_image)
        e.add_empty_data_section('.data', regions.data, regions.bss - regions.data)
        e.add_empty_data_section('.bss', regions.bss, regions.heap - regions.bss)

    e.set_entry(mzip.entry)
    e.set_machine(guess_machine_type(main_image))

    out.write(e.build())

    logging.info('extracted successfully')
    return True
