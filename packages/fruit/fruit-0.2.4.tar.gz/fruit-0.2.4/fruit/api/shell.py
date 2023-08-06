"""
Module for implementing shell interactions within fruit
"""
import os
import fruit.modules.console as console
from fruit.globals import SHELLCHAR

def shell(cmd: str) -> int:
    """
    Execute the given shell string 
    
    Parameters
    ----------
    `cmd` : str
        Command string to execute
    
    Returns
    -------
    int
        Returncode of the shell
    """
    # Print the string to the console
    console.echo(SHELLCHAR + cmd)
    return os.system(cmd)
