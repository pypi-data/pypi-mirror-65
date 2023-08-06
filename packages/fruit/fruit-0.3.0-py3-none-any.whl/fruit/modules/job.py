"""
Implementations of multiple jobs in a yaml file
"""

import fruit.modules.step as step
import click
import fruit.config as config

class JobParseError(Exception):
    """Exception Type for error while parsing fruit jobs"""
    pass

class Job(object):
    """
    Object representation of a job inside of a yaml file

    Attributes:
    -----------

    name: str
        Name of the job
    desc: str
        Description of the job
    steps: list
        Steps of the job
    """

    name: str = ""
    desc: str = "" 
    steps: list = None
    __exec_callback: callable = None

    def __init__(self, name: str, yaml_dict: dict, exec_callback: callable):
        """
        Initialize a job from a parsed yaml dictionary with the default parameters.
        
        Parameters
        ----------
        `name` : str
            Name of the job (parsed in target)
        `yaml_dict` : dict
            Yaml dictionary of the job
        `exec_callback` : callable
            Callback to execute job by bane (passed from `Target`)
        
        Raises
        ------
        JobParseError
            YAML syntax error or missing fields
        """
        try:
            # Fetch mandatory parameters

            self.name = name
            self.desc = yaml_dict['desc']
            self.steps = []

            # Execution callback to target
            self.__exec_callback = exec_callback;

            # Validate Types
            if type(self.name) is not str:
                raise JobParseError("The job name must be a string!")
            
            if type(self.desc) is not str:
                raise JobParseError("The job description must be a string!")

            if type(yaml_dict['steps']) is not list:
                raise JobParseError("The job steps must be formatted as a list!")

            for each_step in yaml_dict['steps']:
                # Fetch the pipeline steps
                self.steps.append(step.create(yaml_dict=each_step, exec_callback=exec_callback))

        except KeyError as kerr:
            raise JobParseError("The field '{}' cannot be found!".format(str(kerr)))
        except JobParseError: # Forward JobParseError errors
            raise
        except step.StepParseError: # Forward step parsing errors
            raise
            

    def execute(self):
        """
        Execute all pipeline steps in the given job. Execution policy may differ by step
        implementation.
        """
        # Print two line separators at each start of a job
        click.echo()
        click.secho(config.JOB_SEP)
        click.secho(config.JOB_SEP)

        number = 0
        for each_step in self.steps:
            # Log execution
            number += 1
            click.secho(config.ICON_FRUIT + " Step {number}: Executing {name} ({type})".format(number=number,name=each_step.name, type=each_step.type), fg="yellow")
            click.secho(config.LINE_SEP)
            
            each_step.execute()
        
        # Print the results after execution
        self.print_results()

        # Print two line separators after each job close
        click.secho(config.JOB_SEP)
        click.secho(config.JOB_SEP)
        click.echo()
    
    def print_results(self):
        """
        Print the results of the pipeline execution steps
        """
        fmt  = "{icon:<3}{time:<7}{name:<}"
        head = fmt.format(icon=config.ICON_QUESTION,time="Time", name="Step")
        sep  = fmt.format(icon="-"*3, time="-"*7,  name="-"*10)

        click.echo() # Make 1 row space
        click.secho(head)
        click.secho(sep)

        for each_step in self.steps:
            if each_step.status == 0:
                click.secho(fmt.format(icon=config.ICON_SUCCESS,time="{:.2f}".format(each_step.exec_time), name=each_step.name))
            else:
                click.secho(fmt.format(icon=config.ICON_ERROR,time="{:.2f}".format(each_step.exec_time), name=each_step.name))




def create(name: str, yaml_dict: dict, exec_callback: callable) -> Job:
    """
    Create a new fruit job
    
    Parameters
    ----------
    name: str
        Name of the job
    yaml_dict : dict
        Dictionary of the job
    
    Returns
    -------
    Job
        Job object
    """

    return Job(name=name, yaml_dict=yaml_dict, exec_callback=exec_callback)