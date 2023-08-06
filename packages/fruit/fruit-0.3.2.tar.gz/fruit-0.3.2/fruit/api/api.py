from fruit.modules.target import FruitError
from fruit.modules.step import SkipStepSignal, FailStepSignal, AbortStepSignal
from fruit.modules.garden import Garden
import fruit.modules.console as console

def abort(reason: str):
    """
    Abort the target make from a step or a function
    
    Parameters
    ----------
    `reason` : str
        Abort reason
    
    Raises
    ------
    AbortStepSignal
        Error signal for target make 
    """
    raise AbortStepSignal(reason)

def fail(reason:str= None) -> None:
    """
    Send a signal that the current step is failed, BUT DO not prevent other
    steps from being executed.

    As `fruit.abort()` stops the make process, the fail function only indicates
    a step error.
    
    Parameters
    ----------
    reason : str, optional
        Reason of the error, by default None
    """
    if reason is None:
        raise  FailStepSignal()
    else:
        raise FailStepSignal(reason)

# BUG: Skip propagates...
def skip(reason: str= None):
    """
    Send a signal to the fruit step handler that the current step needs
    to be skipped.
    
    Parameters
    ----------
    `reason` : str
        Reason of the skip
    
    Raises
    ------
    SkipStepSignal
        Exception to indicate that a step is being skipped.
    """
    if reason is None:
        reason = ""

    raise SkipStepSignal(reason)

def finish(message: str = None):
    """
    Send a sign to the application, that the execution was finished successfully.
    
    Parameters
    ----------
    message : str, optional
        Message to write at application finish, by default None
    """
    # Notify the gardener of the successful finish
    Garden().set_returncode(0)

    if message is not None:
        console.echo_green(message)