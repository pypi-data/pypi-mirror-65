import bz2
import logging

from construct import *

from simpleelf.elf_structs import ElfStructs
from simpleelf.elf_builder import ElfBuilder
from simpleelf import elf_consts

from packers.utils import REGIONS_MAGIC, get_elf_from_code

elf_structs = ElfStructs('>')

def unpack(fw, out):
    logging.debug('attempting RAW packer')

    main_image = fw.read()

    if REGIONS_MAGIC not in main_image:
        logging.debug('didnt find REGIONS_MAGIC')
        return False

    e = get_elf_from_code(main_image)
    out.write(e.build())

    logging.info('extracted successfully')
    return True
