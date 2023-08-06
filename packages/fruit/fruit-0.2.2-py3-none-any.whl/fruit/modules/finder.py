"""
Module for finding fruit configuration files automatically.
"""

import os

import fruit.config as config


def find_fruit(path: str) -> str:
    """
    Find the fruit.yaml in the given directory and read it's contents.
    
    Parameters
    ----------
    path : str
        Path to search
    
    Returns
    -------
    str
        Contents of the fruit.yaml file
    
    Raises
    ------
    FileNotFoundError
        The given path is not valid
    FileNotFoundError
        The given path does not contain a fruit.yaml file
    """
    if os.path.exists(path) and os.path.isdir(path):
        fruitpath = os.path.join(path, config.FRUIT_FILENAME)

        if os.path.exists(fruitpath) and os.path.isfile(fruitpath):
            
            with open(fruitpath, 'r') as fp:
                fruitfile = fp.read()
                return fruitfile
        else:
            raise FileNotFoundError("There is no build configuration to be found. Please create a fruit.yaml file.")
    else:
        raise FileNotFoundError("The given path is not valid!")
