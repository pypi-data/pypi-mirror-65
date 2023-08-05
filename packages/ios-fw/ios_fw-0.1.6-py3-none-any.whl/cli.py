import logging
import os

import coloredlogs
import click

coloredlogs.install(level=logging.DEBUG)

from packers import elf_packer
from packers import mzip_packer
from packers import raw_packer
from packers import rv_packer

PACKERS = [elf_packer, mzip_packer, raw_packer, rv_packer]


@click.command()
@click.argument('fw', type=click.File('rb'))
@click.option('--out', type=click.File('wb'), default=None)
def unpack(fw, out=None):
    if out is None:
        out_filename = os.path.splitext(fw.name)[0] + '.elf'
        logging.info('out filename: {}'.format(out_filename))
        out = open(out_filename, 'wb')

    for p in PACKERS:
        fw.seek(0)
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
