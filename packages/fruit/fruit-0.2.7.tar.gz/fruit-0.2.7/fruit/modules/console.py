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

def echo_green(obj: any):
    """
    Write a string to the console with green color
    
    Parameters
    ----------
    `obj` : any
        Any object, that is compatible with print
    
    Note
    ----
    The green color usually means success, however it is not a standard definitions as 
    yellow = warning and red = error. This is the reason why the function is simply called 
    `echo_green`.
    """
    click.secho(obj, fg='green')

def warning(obj: any):
    click.secho(obj, fg='yellow')

def error(obj: any):
    click.secho(obj, fg='red')