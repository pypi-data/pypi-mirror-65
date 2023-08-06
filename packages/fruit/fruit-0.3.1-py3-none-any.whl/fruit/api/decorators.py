
from fruit.modules.garden import Garden
from fruit.modules.target import Target
from fruit.modules.step   import Step
from fruit.modules.provider import Provider

from typing import Callable, Any

def target(name:str=None, help:str=None): # TODO: Document

    def decorator(func:Callable[[], None]) -> Callable[[], None]:
        """Decorate the target function and register the target in the collection."""
        # Determine the target name and help text
        trg_name = name if name is not None else func.__name__
        trg_help = help if help is not None else ""

        new_trg = Target(func=func, name=trg_name, help=trg_help)
        new_trg.OnActivate += Garden().delegate_OnTargetActivate  # Attach the event handler
        new_trg.OnDeactivate += Garden().delegate_OnTargetDeactivate  # Attach the event handler

        # Add the target to the garden
        Garden().add_target(new_trg)

        def warpper() -> None:
            """Wrapped target function."""
            # Call the class object's __call__ function
            new_trg()

        return warpper

    return decorator


def step(name:str=None, help:str=None): # TODO: Document

    def decorator(func:Callable[[Any], Any]) -> Callable[[Any], Any]:

        def wrapper(*args, **kwargs) -> Any:
            # NOTE: Steps can be executed multiple times, the object creation belongs to the call!
            stp_name = name if name is not None else func.__name__
            stp_help = help if help is not None else ""

            new_step = Step(func, name=stp_name, help=stp_help)

            # Attach the event handlers
            new_step.OnActivate   += Garden().delegate_OnStepActivate
            new_step.OnSkipped    += Garden().delegate_OnStepSkipped
            new_step.OnFailed     += Garden().delegate_OnStepFailed
            new_step.OnAborted    += Garden().delegate_OnStepAborted
            new_step.OnDeactivate += Garden().delegate_OnStepDeactivate

            return new_step(*args, **kwargs)

        return wrapper
    return decorator

def provider(name:str=None, help:str=None) -> Callable:
    """
    Decorator function to create fruit information provider.

    Information provides are also shown with the command `fruit collect`
    and can be executed via `fruit get <name>`.

    Parameters
    ----------
    `name` : str, optional
        Name of the provider, by default None. When left empty, the function name
        will be used.
    `help` : str, optional
        Help text of the provider, by default None. When left empty, then function docstring
        will be used.

    Returns
    -------
    Callable
        Decorated information provider function.
    """


    def decorator(func):

        # Check the name and help overrides
        if name is not None:
            p_name = name
        else:
            p_name = func.__name__

        if help is not None:
            p_help = help
        else:
            p_help = func.__doc__

        obj = Provider(name=p_name, help=p_help, func=func)
        Garden().add_provider(obj)

        def wrapper(func) -> str:
            # Call the class call implementation
            return obj()

        return wrapper
    return decorator