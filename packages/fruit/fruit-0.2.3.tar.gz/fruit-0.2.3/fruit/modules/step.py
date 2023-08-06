"""
Module for implementing the inner steps of a target
"""
import fruit.modules.console as console
from fruit.globals import FMT_STEPHEADER
import time


STATUS_OK = 0
STATUS_ERR = 1
STATUS_SKIPPED = -1

class SkipStepSignal(Exception):
    """Signal to indicate, whenever a step shall be skipped"""
    pass


class Step(object):
    name: str = ""  # Name of the step
    desc: str = ""  # Description of the step
    number: int = 0
    status: int = 1  # Error by default
    
    __timer0 : float = .0  # Start execution time of the step
    __elapsed_time : float = .0  # Measured elapsed time spent in the current step

    def __init__(self, name: str, desc: str, number: int):
        if type(name) is not str:
            raise TypeError("The step name must be a string!")
        if type(desc) is not str:
            raise TypeError("The step description bust be a string!")
        
        if type(number) is not int:
            raise TypeError("The step number must be an integer!")

        self.name = name
        self.desc = desc
        self.number = number
    
    def __tic(self):
        """
        Start measuring the execution time and store it in `__timer0`.
        """
        self.__timer0 = time.clock()
    
    def __toc(self) -> float:
        """
        Stop measuring the execution time and set the elapsed time.
        """
        # Set the active step
        self.__elapsed_time = time.clock() - self.__timer0
    
    def __enter__(self):
        """
        Enter the context of the current step.
        """
        # Print the step header
        self.print_stephead()

        # Start measuring the execution time
        self.__tic()

        # Return the object, to use it directly as a context manager
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Leave the context of the current step. Stop the time measurements and perform post
        step actions.
        """
        self.__toc()
        
        if exc_type is SkipStepSignal:
            self.status = STATUS_SKIPPED
            print(str(exc_value) + self.name)
        elif exc_type is not None:
            self.status = STATUS_ERR
        else:
            self.status = STATUS_OK

    def setstatus(self, value: int):
        """
        Set the status of the step to True (successful).
        """
        self.status = value
    
    def get_elapsed_time(self) -> float:
        """
        Get the execution time in seconds of the step, when it was already executed.
        
        Returns
        -------
        float
            Execution time

        Note
        ----
        When the step was not executed yet, the value will default back to 0.0
        """
        return self.__elapsed_time
    
    def getstatus(self) -> int:
        return self.status
    
    def print_stephead(self):
        """
        Print a formatted step header to the console to separate steps from each other.
        """
        console.echo(FMT_STEPHEADER.format(number=self.number, name=self.name))

    
