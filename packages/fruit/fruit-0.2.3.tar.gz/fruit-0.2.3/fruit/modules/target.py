from fruit.modules.step import Step, STATUS_ERR, STATUS_OK, STATUS_SKIPPED
import fruit.modules.console as console
import tabulate
import fruit.globals as glb

class FruitError(Exception):
    """Error class for aborting the target make"""
    pass

class Target(object):
    name: str = ""
    desc: str = ""
    __func : callable = None

    __steps: list = None

    __active_step: Step = None # Object pointing to the currently active step

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

        # Set the active step
        self.__active_step = step
    
    def fallback_step(self, step: Step):
        """
        Set the active step back to an already existing value without appending it as a new
        step.
        
        Parameters
        ----------
        `step` : Step
            Step to fall back to.

        When calling a step inside a step and then performing other actions the context
        manager will keep track of the currently active step.
        Example::
            @fruit.step
            def step1():
                print('Step1')
            
            @fruit.step
            def step2():
                print('Step2 start')
                step1()
                print('Step2 end')
        """
        self.__active_step = step
    
    def get_active_step(self) -> Step:
        """
        Get the currently active step. When there is no active step `None` will be returned.
        
        Returns
        -------
        Step
            Currently active step or `None`
        """
        # TODO: Reset active step after target finish!
        return self.__active_step

    def count_steps(self) -> int:
        """
        Get the number of registered steps
        
        Returns
        -------
        int
            Number of steps
        """
        return len(self.__steps)
    
    def override_function(self, function:callable):
        """
        Override the callable target funcrion with a decorated function.
        
        Parameters
        ----------
        `function` : callable
            New wrapped function
        """
        self.__func = function
        
    
    def print_targethead(self, as_step:bool = False):
        """
        Print a headline to the console to incicate the the target has been
        activated.
        
        Parameters
        ----------
        as_step : bool, optional
            If true, the target will be handled as a step, by default False
        """
        if(not as_step):
            console.echo("🍓 Making '{}'".format(self.name))
        else:
            console.echo("🍋 Target sub '{}'".format(self.name))
    
    def print_results(self):
        """
        Print the list of executed steps / targets and indicate, which was
        successful.
        """
        console.echo("Results:")
        console.echo()

        results = []
        for each_step in self.__steps:
            if each_step.status == STATUS_OK:
                icon = glb.ICON_SUCC
            elif each_step.status == STATUS_SKIPPED:
                icon = glb.ICON_SKIP
            else:
                icon = glb.ICON_FAIL
            
            results.append((icon, each_step.name))
        
        console.echo(tabulate.tabulate(results, headers=['🍋', 'Step']))


    def __call__(self):
        self.__func()