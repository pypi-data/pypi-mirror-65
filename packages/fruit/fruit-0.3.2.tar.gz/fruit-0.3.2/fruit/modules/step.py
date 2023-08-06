"""
Module for implementing the inner steps of a target
"""
import fruit.modules.console as console
from fruit.globals import FMT_STEPHEADER, FMT_SKIPMESSAGE, FMT_FAILMESSAGE
import time
from typing import Callable, Any
from .event import Event


STATUS_OK = 0
STATUS_ERR = 1
STATUS_SKIPPED = -1
STATUS_UNKNOWN = -2

class SkipStepSignal(Exception):
    """Signal to indicate, whenever a step shall be skipped"""
    pass

class AbortStepSignal(Exception):
    """Signal to indicate, when a target make has to be stopped
    because of a step error."""
    pass

class FailStepSignal(Exception):
    """Signal to indicate that a step is failed but the make process
    may continue."""
    pass

class Step(object):
    """
    Step object for handling and registering make steps.

    Attributes
    ----------
    name : str
        Step name
    fullname : str
        Full name of the step indicating its execution place
    help : str
        Help text (description) of the step
    status : int
        Status code of the current step. Possible values: `STATUS_UNKNOWN`, `STATUS_SKIPPED`,
        `STATUS_OK`, `STATUS_ERR`.
    time : float
        Measured execution time in seconds

    Events
    ------
    OnActivate : Event(sender=self)
        Called when the step execution begins
    OnDeactivate: Event(sender=self)
        Called whe the step execution finished
    OnSkipped : Event(sender=self, exception=SkipStepSignal())
        Called when `fruit.skip()` is called inside of the step
    OnFailed : Event(sender=self, exception=FailStepSignal())
        Called when `fruit.fail()` is called inside of the step
    OnAborted : Event(sender=self, exception=AbortStepSignal())
        Called when `fruit.abort()` is called inside of the step
    """

    name: str = ""
    fullname: str = ""
    help: str = ""
    status: int = STATUS_UNKNOWN
    time: float = .0

    OnActivate: Event = None
    OnDeactivate: Event = None
    OnSkipped: Event = None
    OnFailed: Event = None
    OnAborted: Event = None
    __func: Callable[[any], any] = None

    def __init__(self, func: Callable[[any], any], name:str, help:str=""):
        
        if callable(func):
            self.__func = func
        else:
            raise TypeError("The given function is not callable!")
        
        if type(name) is str:
            if len(name) > 0:
                self.name = name
                self.fullname = name
            else:
                raise ValueError("The given name cannot be empty!")
        else:
            raise TypeError("The step name must be a string!")
        
        if type(help) is str:
            self.help = help
        else:
            raise TypeError("The step help must be a string!")

        # Create the class events (with an example call)
        self.OnActivate   = Event(sender=self)
        self.OnDeactivate = Event(sender=self)

        # Create event handlers for the exception based status changes
        self.OnSkipped    = Event(sender=self, exception=None)
        self.OnFailed     = Event(sender=self, exception=None)
        self.OnAborted    = Event(sender=self, exception=None)

    def __call__(self, *args, **kwargs) -> Any:
        """
        Function encapsulation of the step call with added event triggers.
        
        Returns
        -------
        Any
            Original return value of the function
        """
        self.OnActivate(sender=self)
        tic = time.time()
        retval = None
        try:
            retval = self.__func(*args, **kwargs)
            self.status = STATUS_OK
            self.time = time.time() - tic
            self.OnDeactivate(sender=self)
            return retval
        except SkipStepSignal as serr:
            self.status = STATUS_SKIPPED
            self.OnSkipped(sender=self, exception=serr)
            self.time = time.time() - tic
            self.OnDeactivate(sender=self)
        except FailStepSignal as ferr:
            self.status = STATUS_ERR
            self.OnFailed(sender=self, exception=ferr)
            self.time = time.time() - tic
            self.OnDeactivate(sender=self)
        except AbortStepSignal:
            self.status = STATUS_ERR
            self.time = time.time() - tic
            raise

        # NOTE: The fianlly: cannot be used as AbortStepSignal has to propagate
