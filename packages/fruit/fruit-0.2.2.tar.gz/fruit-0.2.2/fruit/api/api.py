from fruit.modules.target import FruitError

def abort(reason: str):
    """
    Abort the target make from a step or a function
    
    Parameters
    ----------
    `reason` : str
        Abort reason
    
    Raises
    ------
    FruitError
        Error signal for target make 
    """
    raise FruitError(reason)