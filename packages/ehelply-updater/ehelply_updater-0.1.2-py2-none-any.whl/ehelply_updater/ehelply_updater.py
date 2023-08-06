import click
from pathlib import Path
import json
import subprocess
import sys

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def ehelplyupdater():
    pass


@ehelplyupdater.command()
@click.argument('input', required=True)
@click.argument('output', required=True)
def update(input=None, output=None):
    structure_path: Path = Path(input)
    output_path: Path = Path(output)


if __name__ == '__main__':
    ehelplyupdater()

