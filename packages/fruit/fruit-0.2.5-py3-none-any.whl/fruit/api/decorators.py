
from fruit.modules.garden import Garden
from fruit.modules.target import Target
from fruit.modules.step   import Step

def target(func):
    trg = Target(func, func.__name__, func.__doc__)    
    def wrapper(*args, **kwargs):
        Garden().reset_returncode() # Reset the returncode after each target call
        # TODO: next_nr shall go to the step...

        if Garden().active_target() is not None:
            next_nr = Garden().active_target().count_steps() + 1
            with Step("TARGET: "+func.__name__, func.__doc__, next_nr) as stp:
                # Get the currently active step (for nested steps)
                stp_fallback = Garden().active_target().get_active_step()
                # Update the currently active step to the new step
                Garden().active_target().add_step(stp)

                returnval = func(*args, **kwargs)

                # Return back to the caller of the nested step
                Garden().active_target().fallback_step(stp_fallback)
        else:
            Garden().activate_target(trg)
            # Call the function as a target
            returnval = func(*args, **kwargs)
        return returnval
    # TODO: This just looks horrible for now...
    trg.override_function(wrapper)
    Garden().add_target(trg)
    return wrapper


def step(func):
    def wrapper(*args, **kwargs):
        garden = Garden()
        next_nr = garden.active_target().count_steps() + 1

        returnval = None #  In case of a skip call

        with Step(func.__name__, func.__doc__, next_nr) as stp:
            # Get the currently active step (for nested steps)
            stp_fallback = Garden().active_target().get_active_step()
            # Update the currently active step to the new step
            Garden().active_target().add_step(stp)

            returnval = func(*args, **kwargs)

            # Return back to the caller of the nested step
            Garden().active_target().fallback_step(stp_fallback)

        # Return the original result of the function call
        return returnval
    return wrapper
