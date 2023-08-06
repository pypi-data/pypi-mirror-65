"""
Fruit garden is the master collection singleton of the application
"""
from .patterns import SingletonMeta
from .target   import Target, FruitError
import fruit.modules.console as console

class Garden(metaclass=SingletonMeta):

    __targets : list = None
    __active_target : Target = None

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
                self.__active_target = cl  # Set the currently active target
                cl()
            except FruitError as ferr:
                # Log the error message
                console.error("The make process was aborted. Reason:")
                console.error(str(ferr))
            finally:
                self.__active_target = None
    
    def active_target(self) -> Target:
        return self.__active_target


    def get_targets(self):
        for each_target in self.__targets:
            yield each_target