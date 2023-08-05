import logging
from pathlib import Path

import click

from . import main


VERSION = '0.0.1'
_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=False)
_dir_optional = click.Path(exists=False)
_file_existing = click.Path(exists=True, dir_okay=False, file_okay=True)
verbose_help = 'Enable verbose output.'


@click.group()
@click.version_option(VERSION, '-V', '--version', prog_name='talqual')
@click.option('-v', '--verbose', is_flag=True, help=verbose_help)
def cli(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)


@cli.command()
@click.argument('src', type=_dir_existing, required=True)
@click.argument('dst', type=_dir_optional, required=False)
@click.option('--data', type=_file_existing, required=False,
              help='defaults to src/_data.yaml', metavar='data.yaml')
def build(src, dst, data):
    """Builds SRC to DST

    SRC is a directory of templates

    DST defaults to SRC/_build
    """
    src = Path(src)
    if dst is None:
        dst = src / '_build'
    else:
        dst = Path(dst)
    if data is None:
        data = src / '_data.yaml'
    else:
        data = Path(data)

    main.build(src, dst, data)
