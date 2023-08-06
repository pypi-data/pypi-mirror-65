"""
Printing module to print logs and results
"""

from .target import Target
from .provider import Provider
from .step import Step, STATUS_ERR, STATUS_OK, STATUS_SKIPPED, STATUS_UNKNOWN
import fruit.modules.console as console
import click
import tabulate
from typing import List
import time

WIDTH = (click.get_terminal_size()[0] - 10)

# Define ICONS
ICON_TARGET = "🌳🍎"
ICON_STEP   = "🥝"
ICON_OK     = "✅"
ICON_SKIP   = "⏩"
ICON_ERR    = "❌"
ICON_UNKNOWN = "❔"

def print_target_list(targets: List[Target]) -> None:
    """
    Print the list of targets in tabular format to the console.
    
    Parameters
    ----------
    targets : List[Target]
        List of target objects
    """
    table = [(t.name, t.help) for t in targets]
    if len(table) > 0:
        console.echo()
        console.echo("List of available targets:")
        console.echo(tabulate.tabulate(table, headers=['Target', 'Description']))
    else:
        console.echo()
        console.echo("No targets found!")

def print_provider_list(providers: List[Provider]) -> None:
    """
    Print the list of providers in tabular format to the console.
    
    Parameters
    ----------
    providers : List[Provider]
        List of provider objects
    """
    table = [(p.name, p.help) for p in providers]
    if len(table) > 0:
        console.echo()
        console.echo("List of available providers:")
        console.echo(tabulate.tabulate(table, headers=['Provider', 'Description']))
    else:
        console.echo()
        console.echo("No providers found!")

def print_target_head(target: Target) -> None:
    """
    Print the target header when a target make starts
    
    Parameters
    ----------
    target : Target
        Target object
    """
    console.echo()
    console.echo(f"{ICON_TARGET} Making '{target.name}' ...")
    console.echo("="*WIDTH)

def print_target_foot(target: Target) -> None:
    """
    Print the footer line when a target execution finished.
    
    Parameters
    ----------
    target : Target
        Target object
    """
    console.echo("="*WIDTH)

def print_step_head(step: Step, number: int) -> None:
    """
    Print the header line of a step, when the step is activated.
    
    Parameters
    ----------
    step : Step
        Step object
    """
    mstring = f"{ICON_STEP} Step {number} : {step.fullname}"
    if len(mstring) < WIDTH:
        mstring += " " + "-"*(WIDTH -len(mstring)-2)
    console.echo()
    console.echo(mstring)
    console.echo()

def print_step_foot(step: Step, number: int) -> None:
    pass

def print_step_fail(step: Step, reason: str) -> None:
    """
    Print a diagnostic message to the console when a step failed.
    
    Parameters
    ----------
    step : Step
        Step that caused the fail.
    """
    if reason is None or reason is "":
        reason = ""

    console.error(f"{ICON_ERR} Step '{step.name}' failed! {reason}")

def print_step_skip(step: Step, reason: str) -> None:
    """
    Print a diagnostic message to the console when a step was skipped.
    
    Parameters
    ----------
    step : Step
        Step that was skipped.
    """
    if reason is None or reason is "":
        reason = ""

    console.warning(f"{ICON_SKIP} Step '{step.name}' was skipped! {reason}")

def print_summary(last_target:Target, steps:List[Step]) -> None:
    """
    Print the summarized results as a table to the console. All run steps & substeps and targets
    will be summarized.
    
    Parameters
    ----------
    last_target : Target
        Target that the summary belonds to

    steps : List[Step]
        List of executed steps
    """
    table = []
    for each_step in steps:
        # Determine the status icon
        if each_step.status == STATUS_OK:
            icon = ICON_OK
            status = "OK"
        elif each_step.status == STATUS_SKIPPED:
            icon = ICON_SKIP
            status = "Skipped"
        elif  each_step.status == STATUS_ERR:
            icon = ICON_ERR
            status = "Failed"
        else:
            icon = ICON_UNKNOWN
            status = "Unknown"
        
        name = each_step.fullname
        xtime = "%.3f" % each_step.time
        table.append((icon, status, xtime, name))

    console.echo()
    console.echo(f"Summary of target '{last_target.name}':")
    console.echo()
    console.echo(tabulate.tabulate(table, headers=('', 'Status', 'Time', 'Name')))
    console.echo()
    console.echo_green(f"{ICON_OK} Target '{last_target.name}' was succesful!")

def print_summary_abort(last_target:Target, steps:List[Step]) -> None:
    """
    Print the summarized results of an aborted target as a table to the console. 
    All run steps & substeps and targets will be summarized.

    Parameters
    ----------

    last_target : Target
        Target that the summary belonds to

    steps : List[Step]
        List of executed steps
    """
    table = []
    for each_step in steps:
        # Determine the status icon
        if each_step.status == STATUS_OK:
            icon = ICON_OK
            status = "OK"
        elif each_step.status == STATUS_SKIPPED:
            icon = ICON_SKIP
            status = "Skipped"
        elif  each_step.status == STATUS_ERR:
            icon = ICON_ERR
            status = "Failed"
        else:
            icon = ICON_UNKNOWN
            status = "Unknown"
        
        name = each_step.fullname
        xtime = "%.3f" % each_step.time
        table.append((icon, status, xtime, name))

    console.echo()
    console.echo(f"Summary of target '{last_target.name}':")
    console.echo()
    console.echo(tabulate.tabulate(table, headers=('', 'Status', 'Time', 'Name')))

    console.error(f"{ICON_ERR} Target '{last_target.name}' was unsuccessful!")