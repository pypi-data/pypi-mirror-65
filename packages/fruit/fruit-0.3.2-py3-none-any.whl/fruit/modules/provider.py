"""
Fruit provider module to declare information provider functions.
"""
from typing import Callable, Any

class Provider(object):
    """
    Information provider object with associated callback function.

    Information providers are called with the `fruit get <name>` syntax, where <name>
    is the name of the provider function. 

    Attributes
    ----------
    `name` : str
        Name of the provider
    `help`: str
        Help text of the provider
    """

    __name: str = ""
    __help: str = ""
    __func: Callable[[any], str] = None

    def __init__(self, name: str, help: str, func: Callable[[any], str]):
        """
        Create a new information provider object
        
        Parameters
        ----------
        `name` : str
            Name of the information
        `help` : str
            Help text (description) of the information
        `func` : Callable[[any], str]:
            Information provider function, that returns the information as a string.
        """
        
        if type(name) is str:
            if len(name) > 0:
                self.__name = name
            else:
                raise ValueError("The provider name cannot be empty!")
        else:
            raise TypeError("The provider name must be a string!")
        
        if type(help) is str:
            if len(help) > 0:
                self.__help = help
            else:
                raise  ValueError("The provider help cannot be empty!")
        else:
            raise TypeError("The provider help must be a string!")
        
        if callable(func):
            self.__func = func
        else:
            raise TypeError("The provider function must be a callable!")
    
    def __call__(self, *args, **kwargs) -> str:
        """
        Call the provider function with the provided arguments. 
        
        Returns
        -------
        str
            Original return value of the provider function
        """
        return_str = self.__func(*args, **kwargs)

        if type(return_str) is not str:
            try:
                return_str = str(return_str)
            except:
                # This shouldn't be able to happen
                raise TypeError("The given provider function does not provide a string!")
        return return_str

    @property
    def name(self) -> str:
        """Provider Name"""
        return self.__name
    
    @property
    def help(self) -> str:
        """Help text of the provider"""
        return self.__help
