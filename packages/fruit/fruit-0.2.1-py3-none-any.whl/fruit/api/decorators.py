
from fruit.modules.garden import Garden
from fruit.modules.target import Target
from fruit.modules.step   import Step

def target(func):
    garden = Garden()
    def wrapper():
        func()
    
    garden.add_target(Target(wrapper, func.__name__, func.__doc__))
    return wrapper

def step(func):
    def wrapper(*args, **kwargs):
        garden = Garden()
        next_nr = garden.active_target().count_steps() + 1
        new_step = Step(func.__name__, func.__doc__, next_nr)
        garden.active_target().add_step(new_step)
        # TODO: Maybe a context manager?
        new_step.print_stephead()
        func(*args, **kwargs)
    return wrapper
