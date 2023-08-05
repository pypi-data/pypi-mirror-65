import logging
import os

import coloredlogs
import click

coloredlogs.install(level=logging.DEBUG)

from iosfw import mzip_packer
from iosfw import elf_packer

PACKERS = [elf_packer, mzip_packer]


@click.command()
@click.argument('fw', type=click.File('rb'))
@click.option('--out', type=click.File('wb'), default=None)
def unpack(fw, out=None):
    if out is None:
        out_filename = os.path.splitext(fw.name)[0] + '.elf'
        logging.info('out filename: {}'.format(out_filename))
        out = open(out_filename, 'wb')

    for p in PACKERS:
        if p.unpack(fw, out):
            return


@click.group()
def cli():
    pass


def main():
    cli.add_command(unpack)
    cli()


if __name__ == '__main__':
    main()
