"""
Parent Interface object for pipeline steps
"""
import subprocess
import click
import fruit.config as config
import time
import os

class StepParseError(Exception):
    """Exception for showing errors when parsing steps."""
    pass

class Step(object):
    """
    Interface class for defining a pipeline step.

    Attributes
    ----------
    name: str
        Name of the pipeline step
    type: str
        Type of the pipeline step
    """

    name: str = ""  # Name of the pipeline step
    type: str = ""  # Type of the pipeline step
    __status: int = 1  # Status code of the current step
    _tictime: float = .0  # Start time of the execution
    _toctime: float = .0  # End time of the execution
    _execution_time = .0

    def __init__(self, yaml_dict: dict, exec_callback: callable):
        """
        Create a pipeline step based on a yaml dictionary.
        Parses the `name` and `type` field from the yaml directory and run type checkings.

        Parameters
        ----------
        `yaml_dict` : dict
            YAML dictionary to parse (part of a yaml file)

        `exec_callback`: callable
            Callback from the target to execute a job by name

        Raises
        ------
        NotImplementedError
            The function has to be implemented in subclasses
        """
        try:
            self.name = yaml_dict['name']
            self.type = yaml_dict['type']
        except KeyError as kerr:
            raise StepParseError("The field '{}' cannot be found!".format(str(kerr)))

        if type(self.name) is not str:
            raise StepParseError("The step name has to be a string!")

        if type(self.type) is not str:
            raise StepParseError("The step type has to be a string!")

    @property
    def status(self) -> int:
        """
        Get the execution status of the pipeline step

        Returns
        -------
        int
            Return code of the terminal command
        """
        return self.__status

    @property
    def exec_time(self) -> float:
        """
        Execution time of the current step
        """
        return self._execution_time

    def _tic(self):
        """
        Start a time measurement.
        """
        self._tictime = time.time()
    
    def _toc(self):
        """
        Stop a started time measurement.
        """
        self._toctime = time.time()
        self._execution_time = self._toctime - self._tictime

    def _setstatus(self, status: int):
        """
        Set the execution status of the step after execution
        
        Parameters
        ----------
        status : int
            Returned execution result code from the command
        """
        self.__status = status

    def execute(self) -> bool:
        """
        Execute the current pipeline step and return the result.

        Returns
        -------
        bool
            True = Execution successful; False= Execution error
        
        Raises
        ------
        NotImplementedError
            The function has to be implemented in subclasses
        """
        raise NotImplementedError


class DefaultStep(Step):

    cmd: str = "" # Command string to execute
    args: list = None

    def __init__(self, yaml_dict: dict, exec_callback: callable):
        
        # Initialize the base class for mandatory fields
        super().__init__(yaml_dict=yaml_dict, exec_callback=exec_callback)

        try:
            self.cmd  = yaml_dict['cmd']
            self.args = yaml_dict['args']
        except KeyError as kerr:
            raise StepParseError("The field '{}' cannot be found!".format(str(kerr)))

        if type(self.cmd) is not str:
            raise StepParseError("The cmd field has to be a string!")

        if type(self.args) is not list:
            raise StepParseError("The args field has to be the list!")
    
    def execute(self) -> int:
        """
        Execute the command with the default type handler (`os.system()`)

        Returns
        -------
        int
            Return code of the command execution
        
        Note
        ----
        The given commands are executed via the subprocess modules
        """
        cmdarray = [self.cmd]
        cmdarray.extend(self.args)

        cmdstr = " ".join(cmdarray)

        # Print the command
        click.echo(config.SHELLCHAR + cmdstr)

        try:
            self._tic() # Measure the execution time

            p = subprocess.Popen([cmdstr], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (child_stdout) = (p.stdout)

            # Set the returncode to 0, when no exception happened
            self._setstatus(0)
        except subprocess.CalledProcessError as cmderror:
            self._setstatus(cmderror.returncode)

        output = child_stdout.read().decode('utf-8')

        # Print the command results
        click.echo(output)

        # NOTE: The time measurement is only accurate after the buffer read!
        self._toc()  # Stop the time measurement

        return self.status

class SystemStep(Step):

    cmd: str = "" # Command string to execute
    args: list = None

    def __init__(self, yaml_dict: dict, exec_callback: callable):

        # Initialize the base class for mandatory fields
        super().__init__(yaml_dict=yaml_dict, exec_callback=exec_callback)

        try:
            self.cmd  = yaml_dict['cmd']
            self.args = yaml_dict['args']
        except KeyError as kerr:
            raise StepParseError("The field '{}' cannot be found!".format(str(kerr)))

        if type(self.cmd) is not str:
            raise StepParseError("The cmd field has to be a string!")

        if type(self.args) is not list:
            raise StepParseError("The args field has to be the list!")
    
    def execute(self) -> int:
        """
        Execute the command with the default type handler (`os.system()`)

        Returns
        -------
        int
            Return code of the command execution
        
        Note
        ----
        The given commands are executed via the subprocess modules
        """
        cmdarray = [self.cmd]
        cmdarray.extend(self.args)

        cmdstr = " ".join(cmdarray)

        # Print the command
        click.echo(config.SHELLCHAR + cmdstr)
        self._tic()
        
        # Run the command in a system subshell
        returncode = os.system(cmdstr)
        self._setstatus(returncode)

        # NOTE: The time measurement is only accurate after the buffer read!
        self._toc()  # Stop the time measurement

        return self.status

class JobStep(Step):
    """
    JobStep object for calling a job from the current yaml file.

    Arguments
    ---------
    job: str
        Name of the job to call
    """

    job: str = "" # Name of the job to call
    __exec_callback: callable = None

    def __init__(self, yaml_dict: dict, exec_callback: callable):

        super().__init__(yaml_dict=yaml_dict, exec_callback=exec_callback)
        try:
            self.job  = yaml_dict['job']

            # Set the execution callback
            self.__exec_callback = exec_callback
        except KeyError as kerr:
            raise StepParseError("The field '{field}' cannot be found".format(field=str(kerr)))

        if type(self.name) is not str:
            raise StepParseError("The step name has to be a string!")
        

    def execute(self):
        """
        Execute the command with the default type handler (`os.system()`)

        Returns
        -------
        int
            Return code of the command execution
        """
        self._tic()
        # Use the callback from the target class to execute the job
        self.__exec_callback(self.job)

        self._toc()

        # TODO: Get execution results
        return 0
        

def create(yaml_dict: dict, exec_callback: callable) -> Step:
    """
    Create a pipeline step object from the yaml dictionary. The creation uses the Factory
    pattern to create an interface typed object from the given representation
    
    Parameters
    ----------
    `yaml_dict` : dict
        YAML dictionary of the pipeline step
    
    `exec_callback`: callabke
        Execution callback from containing target object
    
    Returns
    -------
    Step
        Pipeline step as the Step interface
    """
    if yaml_dict['type'] == 'default':
        return DefaultStep(yaml_dict, exec_callback)
    elif yaml_dict['type'] == 'system':
        return SystemStep(yaml_dict, exec_callback)
    elif yaml_dict['type'] == 'job':
        return JobStep(yaml_dict, exec_callback)
    else:
        raise ValueError("The pipeline type is not available!") 