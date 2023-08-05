import click
import os
import fruit.config as config
from tabulate import tabulate
from fruit.modules.finder import find_fruit
from fruit.modules.target import Target, JobNotFoundError

@click.group()
def cli():
    """
    List and execute command 'jobs' from fruit.yaml configuration files.
    """
    pass

@cli.command()
@click.argument('path', required=False)
def list(path: str = None):
    r"""
    List all available jobs
    """
    if path is None:
        path = '.'

    try:
        # Find the fruit configuraiton file to execute
        fruit_yaml = find_fruit(path)

        # Parse the fruit target
        target = Target(fruit_yaml)

        try:
            tbllist = []
            # List the available jobs
            for each_job in target.jobs:
                tbllist.append((each_job.name, each_job.desc))
            
            # Print the name and the description of the project
            click.echo()
            click.echo("Target name: {name}".format(name=target.name))
            click.echo("Description: {desc}".format(desc=target.desc))
            click.echo()

            click.echo(tabulate(tbllist, ('Job', 'Description'), tablefmt="simple"))

        except JobNotFoundError as exc:
            click.secho(str(exc), fg='red')

    except FileNotFoundError as exc:
        # The fruit configuration is not found
        click.secho(str(exc), fg='red')

@cli.command()
@click.argument('args', nargs=-1, required=True)
def run(args: list):
    """
    Execute an available job.

    Examples::
    
    \b
        fruit run [JOB]
        fruit run [PATH] [JOB]
    
    PATH - Path (directory) of the configuration file
    JOB  - Name of the job (Use 'all' to run all jobs)
    """

    if len(args) == 1:
        path = '.' # Set the local path
        job  = args[0] # Set the job from argument
    elif len(args) == 2:
        path = args[0] # Set the path from argument
        job = args[1]  # Set the job from the second argument

    # TODO: Add command options for output hiding, etc...

    try:
        # Find the fruit configuraiton file to execute
        fruit_yaml = find_fruit(path)

        # Parse the fruit target
        target = Target(fruit_yaml)

        try:
            target.execute(job=job)
        except JobNotFoundError as exc:
            click.secho(str(exc), fg='red')

    except FileNotFoundError as exc:
        # The fruit configuration is not found
        click.secho(str(exc), fg='red')

@cli.command()
@click.argument('path', required=False)
def edit(path: str):
    r"""Edit the fruit.yaml configuration"""
    if path is None:
        path = "./fruit.yaml"

    if os.path.exists(path) and os.path.isfile(path):
        click.edit(filename=path)
    else:
        click.secho("There is no build configuration to be found. Please create a fruit.yaml file.", fg='red')

if __name__ == '__main__':
    cli()
    