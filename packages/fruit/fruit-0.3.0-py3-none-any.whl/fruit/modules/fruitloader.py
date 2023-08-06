"""
This module implements the scan, loading and compiling of fruitconfig.py files.
"""

import os
import fruit.globals as glb

def obtain_config(path: str) -> str:
    """
    Get the full path an existing fruitconfig.py file
    
    Parameters
    ----------
    `path` : str
        Directory path to a containing directory or file path
    
    Returns
    -------
    str
        Full path of the config.py
    
    Raises
    ------
    FileNotFoundError
        The fruitconfig.py file is not found in the current directory
    FileNotFoundError
        The given path is invalid
    """
    if os.path.exists(path):
        if os.path.isdir(path):
            filepath = os.path.join(path, glb.FRUITCONFIG_NAME)
        else:
            filepath = path
        
        if os.path.exists(filepath) and os.path.isfile(filepath):
            return filepath
        else:
            raise FileNotFoundError("There is no fruitconfig.py in the current directory")
    else:
        raise FileNotFoundError("The given path is invalid!")

def compile_config(path: str):
    
    # Read the source code
    with open(path, 'r') as fp:
        source = fp.read()
    
    filename = os.path.basename(path)
    # Create a global namespace for the execution
    namespace = {}
    pyobj = compile(source=source, filename=filename, mode='exec')
    exec(pyobj, namespace, namespace)

def load(path: str):

    configpath = obtain_config(path)
    compile_config(configpath)