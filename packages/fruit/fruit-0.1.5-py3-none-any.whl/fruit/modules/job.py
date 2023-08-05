"""
Implementations of multiple jobs in a yaml file
"""

import fruit.modules.step as step
import click
import fruit.config as config

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

    def __init__(self, name: str, yaml_dict: dict):
        self.name = name
        self.desc = yaml_dict['desc']
        self.steps = []

        for each_step in yaml_dict['steps']:
            # Fetch the pipeline steps
            self.steps.append(step.create(yaml_dict=each_step))

    def execute(self):
        """
        Execute all pipeline steps in the given job. Execution policy may differ by step
        implementation.
        """
        number = 0
        for each_step in self.steps:
            # Log execution
            number += 1
            click.secho(config.ICON_FRUIT + " Step {number}: Executing {name}".format(number=number,name=each_step.name), fg="yellow")
            click.secho(config.LINE_SEP)
            
            each_step.execute()
        
        # Print the results after execution
        self.print_results()
    
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




def create(name: str, yaml_dict: dict) -> Job:
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

    return Job(name=name, yaml_dict=yaml_dict)