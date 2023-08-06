"""
Module for implementing the inner steps of a target
"""
import fruit.modules.console as console
from fruit.globals import FMT_STEPHEADER


class Step(object):
    name: str = ""  # Name of the step
    desc: str = ""  # Description of the step
    number: int = 0
    status: int = 1  # Error by default

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
    
    def setstatus(self, value: int):
        """
        Set the status of the step to True (successful).
        """
        self.status = value
    
    def getstatus(self) -> int:
        return self.status
    
    def print_stephead(self):
        """
        Print a formatted step header to the console to separate steps from each other.
        """
        console.echo(FMT_STEPHEADER.format(number=self.number, name=self.name))

    
