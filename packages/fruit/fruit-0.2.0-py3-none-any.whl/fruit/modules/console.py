import click

def echo(obj: any=None):
    """
    Write a string to the console.
    
    Parameters
    ----------
    `obj` : any
        Any object, that is compatible with the `print()` function.
    """
    if obj is not None:
        click.echo(obj)
    else:
        click.echo()

def warning(obj: any):
    click.secho(obj, fg='yellow')

def error(obj: any):
    click.secho(obj, fg='red')