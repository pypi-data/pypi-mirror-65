from zipfile import ZipFile
from io import BytesIO
import logging

from construct import *
from simpleelf.elf_structs import ElfStructs
from simpleelf import elf_consts

from iosfw.utils import guess_machine_type

COMPRESSED_SECTION_MAGIC = b'\xfe\xed\xfa\xce'

elf_compressed_section = Struct(
    '_start' / Tell,
    'magic' / Const(COMPRESSED_SECTION_MAGIC),
    'unknown0' / Int32ub,
    'size' / Hex(Int32ub),
    'unknown2' / Int32ub,
    'unknown3' / Int32ub,
    'data' / Bytes(this.size),
)

elf_structs = ElfStructs('>')

def extract_elf(fw):
    header_magic = elf_consts.ELFMAG
    is_elf = header_magic == fw.read(len(header_magic))
    fw.seek(0)

    if not is_elf:
        return None

    parsed_elf = elf_structs.Elf32.parse_stream(fw)
    for s in parsed_elf.sections:
        if s.data is None:
            continue

        if not s.data.startswith(COMPRESSED_SECTION_MAGIC):
            continue

        compressed_elf = elf_compressed_section.parse(s.data)
        with ZipFile(BytesIO(compressed_elf.data)) as z:
            entries = z.namelist()

            if len(entries) != 1:
                raise Exception("invalid zip archive entry")

            return z.open(entries[0]).read()


def unpack(fw, out):
    logging.debug('attempting ELF packer')

    raw_elf = extract_elf(fw)

    if raw_elf is None:
        logging.debug('failed to extract ELF')
        return False

    logging.info('ELF image format. extracting...')

    uncompressed_elf = elf_structs.Elf32.parse(raw_elf)
    uncompressed_elf.header.e_machine = guess_machine_type(uncompressed_elf)
    out.write(elf_structs.Elf32.build(uncompressed_elf))

    logging.info('extracted successfully')
    return True
