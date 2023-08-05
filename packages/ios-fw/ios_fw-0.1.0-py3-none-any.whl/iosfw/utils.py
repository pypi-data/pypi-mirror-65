from simpleelf import elf_consts

def guess_machine_type(code):
    # assuming cisco only uses mips and ppc cpus,
    # check for: isync; sync; should be enough to 
    # determine the cpu type
    if b'\x4C\x00\x01\x2C\x7C\x00\x04\xAC' in code:
        return elf_consts.EM_PPC
    else:
        return elf_consts.EM_MIPS
