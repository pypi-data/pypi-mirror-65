from fruit.modules.step import Step, STATUS_ERR, STATUS_OK, STATUS_SKIPPED
import fruit.modules.console as console
import tabulate
import fruit.globals as glb

from .event import Event

from typing import Callable

class FruitError(Exception):
    """Error class for aborting the target make"""
    pass

class Target(object):
    name: str = ""
    help: str = ""
    __func: Callable[[], None] = None

    OnActivate: Event = None  # Event to call when a target is activated
    OnDeactivate: Event = None  # Event to call when a target finished executing

    def __init__(self, func:Callable[[], None], name: str, help:str=""):
        """
        Create a target object with the given target name and target function.

        Parameters
        ----------
        `func` : Callable[[], None]
            Target function to call
        `name` : str
            Target name
        `help` : str, optional
            Target help (description), by default ""

        Raises
        ------
        TypeError
            Invalid target function
        TypeError
            Invalid target name
        ValueError
            Invalid target name length
        TypeError
            Invalid target help
        """
        # Parameter validation
        if not callable(func):
            raise TypeError('The given target function is not callable!')
        else:
            self.__func = func

        if type(name) is not str:
            raise TypeError('Target name must be a string!')
        elif len(name) < 1:
            raise ValueError('Target name cannot be an empty string!')
        else:
            self.name = name

        if type(help) is not str:
            raise TypeError('Target help must be a string!')
        else:
            self.help = help

        # Create the class events with an example call signature
        self.OnActivate = Event(sender=self)
        self.OnDeactivate = Event(sender=self)

    def __call__(self):
        """Call the target function and additional events."""
        self.OnActivate(sender=self)
        self.__func()
        self.OnDeactivate(sender=self)

