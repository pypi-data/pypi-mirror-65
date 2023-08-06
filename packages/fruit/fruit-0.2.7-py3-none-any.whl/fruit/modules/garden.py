"""
Fruit garden is the master collection singleton of the application
"""
from .patterns import SingletonMeta
from .target   import Target, FruitError
import fruit.modules.console as console

class Garden(metaclass=SingletonMeta):

    __targets : list = None
    __active_target : Target = None

    # Overall returncode of the file. Each target call resets it
    __returncode: int = 1

    def __init__(self):

        # Initialize the collection the first time
        if self.__targets is None:
            self.__targets = []
    
    def add_target(self, target: Target):
        """
        Add a fruit target to the collection of targets
        
        Parameters
        ----------
        `target` : Target
            Target object
        """
        self.__targets.append(target)
    
    def make_target(self, target_name: str):
        """
        Execute the target with the selected name
        
        Parameters
        ----------
        `target_name` : str
            Target name to make
        """
        flt_target = list(filter(lambda trg: trg.name == target_name, self.__targets))
        
        if len(flt_target) < 1:
            raise ValueError("The target '{}' is not found!".format(target_name))
        else:
            cl, = flt_target
            try:
                cl()
            except FruitError as ferr:
                # Log the error message
                console.error("The make process was aborted. Reason:")
                console.error(str(ferr))
            finally:
                cl.print_results()
                self.__active_target = None
    
    def activate_target(self, target: Target):
        """
        Set the currently active target
        
        Parameters
        ----------
        `target` : Target
            Target to active (activated from decorator)
        """
        self.__active_target = target

    def active_target(self) -> Target:
        """
        A target is activated, whenever the make target function is called.
        If this is the case, any other called sub-target will belong to this 
        target as a step.
        
        Returns
        -------
        Target
            Currently active targe. None if there is no running process.
        """
        return self.__active_target


    def get_targets(self):
        for each_target in self.__targets:
            yield each_target
    
    def reset_returncode(self):
        """
        Reset the returncode to 1.

        Note
        ----
        It shall be called after a target is executed
        """
        self.__returncode = 1
    
    def set_returncode(self, returncode: int):
        """
        Set the application return code.
        
        Parameters
        ----------
        `returncode` : int
            Application returncode to return after the execution was finished.
        """
        if type(returncode) is int:
            self.__returncode = returncode
        else:
            raise TypeError("The given returncode is not an integer!")

    @property
    def returncode(self) -> int:
        """Return code of the application"""
        return self.__returncode