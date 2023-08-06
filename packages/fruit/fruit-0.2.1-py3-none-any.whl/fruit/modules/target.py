from fruit.modules.step import Step

class FruitError(Exception):
    """Error class for aborting the target make"""
    pass

class Target(object):
    name: str = ""
    desc: str = ""
    __func : callable = None

    __steps: list = None

    def __init__(self, func: any, name: str, desc: str):
        """
        Initialize a new target from name description and callback
        
        Parameters
        ----------
        `func` : any
            Target function to call
        `name` : str
            Name of the target
        `desc` : str
            Description of the target
        """
        
        if type(name) is not str:
            raise TypeError("The target name must be a string!")

        if type(desc) is not str:
            raise TypeError("The target description must be a string!")
        
        if not callable(func):
            raise TypeError("The target function must be a callable!")

        self.name = name
        self.desc = desc
        self.__func = func

        self.__steps = []
    
    def add_step(self, step: Step):
        """
        Add a step, that is currently being executed to the target.
        
        Parameters
        ----------
        `step` : Step
            Step object
        """
        self.__steps.append(step)
    
    def count_steps(self) -> int:
        """
        Get the number of registered steps
        
        Returns
        -------
        int
            Number of steps
        """
        return len(self.__steps)
        

    def __call__(self):
        self.__func()