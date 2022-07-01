import inspect
from types import UnionType, GenericAlias
from .exceptions import ParamsDoesNotMatchError

def strict_func(func):
    '''
    Ensures that a function parameters match the typings specified 
    by the uder
    '''

    def inner(*args, **kwargs):

        annot : dict= func.__annotations__
        params_map = inspect.getcallargs(func, *args, **kwargs)

        print(params_map, annot)
        if annot:
            for arg, param in params_map.items():
                arg_type = None
                try:
                    arg_type = annot[arg]
                except KeyError:
                    pass

                if arg_type:
                    if type(arg_type) == type: # for customed types in python
                        if type(param) != arg_type:
                            error_msg = f'The value of "{arg}" is not of type {arg_type}'
                            raise ParamsDoesNotMatchError(error_msg)

                    elif type(arg_type) == UnionType: # for union types 
                        type_list = str(arg_type).split(' | ')
                        if type(param).__name__ not in type_list:
                            error_msg = f'The value of "{arg}" is not of types {" ".join([f"<class {x}>" for x in type_list])}'
                            raise ParamsDoesNotMatchError(error_msg)

                    elif type(arg_type) == GenericAlias:
                        print(str(arg_type))

                    else:
                        print(type(param).__name__, arg_type)


        value = func(*args, **kwargs)

        return value
    return inner
