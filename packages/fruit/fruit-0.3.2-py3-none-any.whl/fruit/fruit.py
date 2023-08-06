"""
Fruit CLI Framework for process automation.
"""

import click
import sys
from tabulate import tabulate
from fruit.modules.fruitloader import load
from fruit.modules.garden import Garden
import fruit.modules.console as console
import fruit.modules.printing as printing
from fruit.modules.pickup import pickup_path, drop_path, load_fruit_env


# Import the extensions!
import fruit.extensions.global_providers

@click.group()
def cli():
    """
    Fruit cli framework for task automation.
    """
    pass


@cli.command()
@click.option('-p', '--pickup', type=click.Path(exists=True), help='Path (relative or absolute) to add to the fruit path', required=False)
@click.option('-d', '--drop', type=click.Path(exists=True), help='Path (relative or absolute) to remove from the fruit path', required=False)
def path(pickup: click.Path, drop: click.Path):
    """
    Add/Remove folder or file path for globally available fruit configurations.

    \b
    Use `fruit path` to list all the picked up paths.
    To add a path, use the option --pickup <path>.
    To remove a path, use the option --drop <path>.
    """
    if pickup is None and drop is None:
        # Print the list of paths
        pathlist = load_fruit_env()
        if len(pathlist) > 0:
            console.echo("List of added pathes: ")
            console.echo()

            for path in pathlist:
                console.echo("  " + path)
            console.echo()
        else:
            console.echo("🍌 There are no fruits picked up!")
    else:
        if pickup is not None:
            pickup_path(pickup)

        if drop is not  None:
            drop_path(drop)

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
        # Print the list of targets
        printing.print_target_list(Garden().get_targets())

        printing.print_provider_list(Garden().get_providers())


    except Exception as err:
        console.error(str(err))

@cli.command()
@click.argument('target', required=True, nargs=-1)
def make(target: str):
    """
    Make a fruit target from the parsed fruitconfig.py file.
    """
    try:
        load('.')
        # Pass all the targets to the make function
        Garden().make_multiple(*target)
    except Exception as exc:
        console.error(str(exc))

@cli.command()
@click.argument('name', required=True)
def get(name: str):
    """Run an information provider to obtain data from the current project.
    
    \b
    Example::
        fruit get version
    
    """
    try:
        load('.')
        result = Garden().run_provider(name=name)

        console.echo(result)
    except Exception as exc:
        console.error(str(exc))


# Main application code of the project
def main():
    # Call the click handler
    cli()