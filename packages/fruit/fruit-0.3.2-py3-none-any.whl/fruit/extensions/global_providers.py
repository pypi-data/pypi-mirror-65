"""
Module to add global provider objects to the fruit cli. The naming convention of global
object is: @<name>. This convention allows all global objects to be identified easily even
when external configuration files will be added to the fruit automatic load path.
"""
from fruit import provider # Import the provider decorator to define global providers
from fruit.modules.garden import Garden

import os

@provider(name='@path', help='Absolute path of the current directory')
def gl_path() -> str:
    return Garden().getcwd()