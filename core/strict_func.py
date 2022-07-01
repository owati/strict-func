import inspect
from types import UnionType, GenericAlias
from .exceptions import ParamsDoesNotMatchError

class Strict_func:
    '''
    Ensures that a function parameters match the typings specified 
    by the under
    '''
    def __init__(self, func) -> None:
        self.func = func
        self.annot = func.__annotations__

    def __call__(self, *args, **kwargs):

        params_map = inspect.getcallargs(self.func, *args, **kwargs)

        print(params_map, self.annot)
        if self.annot:
            for arg, param in params_map.items():
                arg_type = None
                try:
                    arg_type = self.annot[arg]
                except KeyError:
                    pass

                if arg_type:
                    if type(arg_type) == type: # for customed types in python
                        self.handle_normal_type(arg ,arg_type, param)

                    elif type(arg_type) == UnionType: # for union types 
                        self.handle_union_type(arg, arg_type, param)

                    elif type(arg_type) == GenericAlias:
                        print(str(arg_type))

                    else:
                        print(type(param).__name__, arg_type)


        value = self.func(*args, **kwargs)

        return value


    def handle_normal_type(self, arg: str, arg_type : type, param):
        '''
        This function helps to check the normal python types of class types

        int, str, set, list, dict, and custom built classes
        '''
        if type(param) != arg_type:
            error_msg = f'The value of "{arg}" is not of type {arg_type}'
            raise ParamsDoesNotMatchError(error_msg)


    def handle_union_type(self, arg : str, arg_type : UnionType, param):
        '''
        This function helps to check for union types

        int | str and so on
        '''
        is_type = None
        try:
            is_type = isinstance(param, arg_type)
            if not is_type:
                error_msg = f'The value of "{arg}" is not of types {arg_type}'
                raise ParamsDoesNotMatchError(error_msg)
        except TypeError: # one of the types in the union is a parametized generic
            pass

        if not is_type:
            pass

    
    def handle_general_alias(self, arg : str, arg_type : type, param):
        pass

