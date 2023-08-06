from . import __version__
import click

@click.group()
@click.version_option(__version__)
def main():
  pass

import loo.commands