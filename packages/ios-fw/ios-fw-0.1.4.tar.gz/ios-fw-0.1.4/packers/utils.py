from construct import *

from simpleelf.elf_structs import ElfStructs
from simpleelf.elf_builder import ElfBuilder
from simpleelf import elf_consts

REGIONS_MAGIC = b'\xDE\xAD\x12\x34'

regions_struct = Struct(
    'magic' / Const(REGIONS_MAGIC),

    'unknown0' / Int32ub,
    'unknown1' / Int32ub,
    'unknown2' / Int32ub,
    'unknown3' / Int32ub,
    'unknown4' / Int32ub,

    'text' / Hex(Int32ub),
    'data' / Hex(Int32ub),
    'bss' / Hex(Int32ub),
    'heap' / Hex(Int32ub),

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

    

    regions_struct_offset = main_image.find(REGIONS_MAGIC)
    if -1 == regions_struct_offset:
        logging.warning("failed to locate regions magic. using single .text section")
        if entry is None:
            entry = 0
        e.add_segment(entry, main_image, 
            elf_consts.PF_R | elf_consts.PF_W | elf_consts.PF_X)
        e.add_code_section('.text', entry, main_image)
    else:
        regions = regions_struct.parse(main_image[regions_struct_offset:
            regions_struct_offset+regions_struct.sizeof()])

        if entry is None:
            entry = regions.text & 0xfffff000

        e.add_segment(entry, main_image, 
            elf_consts.PF_R | elf_consts.PF_W | elf_consts.PF_X)
        
        e.add_code_section('.text', entry, len(main_image))
        e.add_empty_data_section('.data', regions.data, regions.bss - regions.data)
        e.add_empty_data_section('.bss', regions.bss, regions.heap - regions.bss)

    e.set_entry(entry)
    e.set_machine(guess_machine_type(main_image))

    return e
