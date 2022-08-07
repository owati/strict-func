import inspect
from lib2to3.pytree import type_repr
from types import UnionType, GenericAlias

if __name__ == '__main__':
    print('importing2')
    from exceptions import ParamsDoesNotMatchError
    from checkers import Checker, DictChecker, ListChecker
else:
    print('importing3')
    from .exceptions import ParamsDoesNotMatchError
    from .checkers import Checker, DictChecker, ListChecker
    f = DictChecker()

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

                    elif type(arg_type) in [DictChecker, ListChecker]:
                        self.handle_custom_checker(arg, arg_type, param)

                    else:
                        
                        print(type(arg_type))
                        print(issubclass(Checker, type(arg_type)))
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


    def handle_custom_checker(self, arg, arg_type, param):
        '''
        This is the function that handles the checking
        This the customer checker to check
        '''
        print('This using the solution in the ')
        arg_type.confirm_type(param)

