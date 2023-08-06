"""
Fruit garden is the master collection singleton of the application
"""
from .patterns import SingletonMeta
from .target   import Target, FruitError
from .step     import Step, SkipStepSignal, FailStepSignal, AbortStepSignal
from .provider import Provider
import fruit.modules.console as console
import fruit.modules.printing as printing

from typing import List
import os

class Garden(metaclass=SingletonMeta):

    __targets : list = None
    __providers: list = None

    __steps : list = None
    __target_stack: List[Target] = None
    __step_stack : List[Step] = None
    # Overall returncode of the file. Each target call resets it
    __returncode: int = 1

    def __init__(self):

        # Initialize the collection the first time
        if self.__targets is None:
            self.__targets = []

        if self.__target_stack is None:
            self.__target_stack = []
        
        if self.__step_stack is None:
            self.__step_stack = []

        if self.__steps is None:
            self.__steps = list() # Initialize a new list for the steps

        # Initialize the provider list
        if self.__providers is None:
            self.__providers = []
    
    def getcwd(self) -> str:
        """
        Get the absolute path of the current working directory.
        
        Returns
        -------
        str
            Current path
        """
        return os.getcwd()

    def add_provider(self, provider: Provider) -> None:
        """
        Append an information provider to the global collection of providers.

        Parameters
        ----------
        `provider` : Provider
            Provider object to append

        Raises
        ------
        TypeError
            Raised, when the passed object is not a provider.
        """
        if isinstance(provider, Provider):
            self.__providers.append(provider)
        else:
            raise TypeError("The given object is not an information provider!")

    def run_provider(self, name: str) -> str:
        """
        Execute an information provider to objtain the requested values.

        Parameters
        ----------
        `name` : str
            Name of the provider to get.

        Returns
        -------
        str
            Provided value.
        """
        # TODO: Add argument propagation!!!
        flt = list(filter(lambda p: p.name == name, self.__providers))

        if len(flt) < 1:
            raise ValueError(f"There is no provider found for '{name}'!")
        else:
            prov, = flt
            return prov()

    def get_providers(self):
        """
        Get the list of registered providers.

        Yields
        -------
        Provider
            All registered providers.
        """
        for each_provider in self.__providers:
            yield each_provider

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
            cl()

    def make_multiple(self, *targets):
        """
        Make every listed target. When a target is not found the make process will be
        aborted.
        """
        try:
            # Call the make command on each passed target
            for each_targetname in targets:
                self.make_target(each_targetname)
        except AbortStepSignal as aerr:
            console.error("The make process was aborted! Reason: {}".format(str(aerr)))
            # Try to print the summary
            printing.print_summary_abort(self.__target_stack[0], self.__steps)
        except SkipStepSignal:
            console.error("fruit.skip() may only be called from inside of a step!")
        except FailStepSignal:
            console.error("fruit.fail() may only be called from inside of a step!")

    def delegate_OnTargetActivate(self, sender: Target) -> None:
        """
        Event handler for handling target activation events.

        Parameters
        ----------
        `caller` : Target
            Target, that has been activated via a function call.
        """
        self.__target_stack.append(sender) # Add the target to the stack
        printing.print_target_head(target=sender)
    
    def delegate_OnTargetDeactivate(self, sender: Target) -> None:
        """
        Event handler for target deactivation. Will be called, when a target finished executing.

        Parameters
        ----------
        `sender` : Target
            Target, that triggered the event.
        """
        # Pop the target from the stack
        last_trg = self.__target_stack.pop()
        printing.print_target_foot(target=sender)

        # Only print the summary, if there are no more targets left!
        if len(self.__target_stack) == 0:
            printing.print_summary(last_trg, self.__steps)
        else:
            pass # Print a middle-summary
    
    def get_curr_step_nr(self):
        return len(self.__steps)
    
    def __get_step_prefix_trg(self) -> str:
        """
        Get the name prefix of the steps based on the target stack. Prefix will only
        be added in case of nested targets.

        Returns
        -------
        str
            Name prefix of the step
        """
        if len(self.__target_stack) > 1:
            namestack = [trg.name for trg in self.__target_stack[1:]]
            return " / ".join(namestack) + " / "
        else:
            return ""
    
    def __get_step_prefix_step(self) -> str:
        """
        Get the step prefix from the nested steps. If steps are called from each other, then
        they will be shown as nested steps!
        
        Returns
        -------
        str
            Step name prefix
        """
        if len(self.__step_stack) > 1:
            namestack = [step.name for step in self.__step_stack[:-1]]
            return " :: ".join(namestack) + " :: "
        else:
            return ""

    def __add_step_name_prefix(self, name:str) -> str:
        """
        Add all of the name prefixes to a given step name

        Returns
        -------
        str
            Step name with name prefixes
        """
        return self.__get_step_prefix_trg() + self.__get_step_prefix_step() +  name

    def delegate_OnStepActivate(self, sender: Step) -> None:
        """Add the step to the list of executed steps, when it is activated"""
        self.__steps.append(sender)
        self.__step_stack.append(sender)

        # Name prefix is added ONLY for the full name! DON'T INHERIT IT
        sender.fullname = self.__add_step_name_prefix(sender.name)

        printing.print_step_head(step=sender, number=self.get_curr_step_nr())
    
    def delegate_OnStepSkipped(self, sender: Step, exception: SkipStepSignal) -> None:
        printing.print_step_skip(step=sender, reason=str(exception))

    def delegate_OnStepFailed(self, sender: Step, exception: FailStepSignal) -> None:
        printing.print_step_fail(step=sender, reason=str(exception))
    
    def delegate_OnStepAborted(self, sender: Step, exception: AbortStepSignal) -> None:
        pass
    
    def delegate_OnStepDeactivate(self, sender: Step) -> None:
        __ = self.__step_stack.pop()

    def get_targets(self):
        for each_target in self.__targets:
            yield each_target

    @property
    def returncode(self) -> int:
        """Return code of the application"""
        return self.__returncode
