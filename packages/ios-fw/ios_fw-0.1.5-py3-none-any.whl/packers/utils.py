import logging

from construct import *

from simpleelf.elf_structs import ElfStructs
from simpleelf.elf_builder import ElfBuilder
from simpleelf import elf_consts

CRASH_MAGIC = b'\xDE\xAD\x12\x34'

crashinfo_external = Struct(
    'magic' / Const(CRASH_MAGIC),

    'version' / Int32ub,
    'reason' / Int32ub,
    'cpu_vector' / Int32ub,
    'registers' / Int32ub,
    'rambase' / Int32ub,

    'textbase' / Hex(Int32ub),
    'database' / Hex(Int32ub),
    'bssbase' / Hex(Int32ub),
    'heapbase' / Hex(Int32ub),

)

def guess_machine_type(code):
    # assuming cisco only uses mips and ppc cpus,
    # check for: isync; sync; should be enough to 
    # determine the cpu type
    if b'\x4C\x00\x01\x2C\x7C\x00\x04\xAC' in code:
        return elf_consts.EM_PPC
    else:
        return elf_consts.EM_MIPS

def get_elf_from_code(main_image, entry=None):
    e = ElfBuilder()
    e.set_endianity('>')

    crashinfo_external_offset = main_image.find(CRASH_MAGIC)
    if -1 == crashinfo_external_offset:
        logging.warning("failed to locate regions magic. using single .text section")
        if entry is None:
            entry = 0
        e.add_segment(entry, main_image, 
            elf_consts.PF_R | elf_consts.PF_W | elf_consts.PF_X)
        e.add_code_section('.text', entry, len(main_image))
    else:
        regions = crashinfo_external.parse(main_image[crashinfo_external_offset:
            crashinfo_external_offset+crashinfo_external.sizeof()])

        if entry is None:
            entry = regions.textbase & 0xfffff000

        e.add_segment(entry, main_image, 
            elf_consts.PF_R | elf_consts.PF_W | elf_consts.PF_X)
        
        e.add_code_section('.text', regions.textbase, len(main_image) - (regions.textbase - entry))
        e.add_empty_data_section('.data', regions.database, regions.bssbase - regions.database)
        e.add_empty_data_section('.bss', regions.bssbase, regions.heapbase - regions.bssbase)

    e.set_entry(entry)
    e.set_machine(guess_machine_type(main_image))

    return e
