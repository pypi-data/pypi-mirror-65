from fruit.modules.target import FruitError
from fruit.modules.step import SkipStepSignal
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
    FruitError
        Error signal for target make 
    """
    raise FruitError(reason)

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