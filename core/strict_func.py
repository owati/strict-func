import inspect
from .exceptions import ParamsDoesNotMatchError

def strict_func(func):
    '''
    Ensures that a function parameters match the typings specified 
    by the uder
    '''

    def inner(*args, **kwargs):

        annot : dict= func.__annotations__
        arguements = inspect.getfullargspec(func).args

        #print(annot, inspect.getargvalues(func))
        if annot:
            for i in range(len(args)):
                param = args[i]
                arg = arguements[i]

                annot_type = None
                try:
                    annot_type = annot[arg]
                except KeyError:
                    pass

                if (annot_type): # if typing was allocated to the arguement
                    if(type(param) != annot_type):
                        error_msg = f"the parameter '{arg}' is not of {annot_type} "
                        raise ParamsDoesNotMatchError(error_msg)

        value = func(*args, **kwargs)

        return value
    return inner
