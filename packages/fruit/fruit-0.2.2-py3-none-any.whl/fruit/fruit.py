"""
Tratatata...
"""

import click
from tabulate import tabulate
from fruit.modules.fruitloader import load
from fruit.modules.garden import Garden
import fruit.modules.console as console

@click.group()
def cli():
    pass

@cli.command()
@click.argument('path', default='.')
def collect(path:str):
    """
    List the fruit targets in the given path.
    \b

    PATH (default: .) - Path of the directory or .py file to scan.
    """
    try:
        # Load the config file
        load(path)

        # List the targets
        tbl = []

        for trg in Garden().get_targets():
            tbl.append((trg.name, trg.desc))
        
        console.echo(tabulate(tbl, headers=['Target', 'Description']), )

    except Exception as err:
        console.error(str(err))



@cli.command()
@click.argument('target', required=True)
def make(target: str):
    """
    Make a fruit target from the parsed fruitconfig.py file.
    """
    try:
        console.echo()
        console.echo("🍓 Making target '{}'... ".format(target))
        console.echo()
        load('.')

        Garden().make_target(target)
    except Exception as err:
        console.error(str(err))