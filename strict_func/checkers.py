# The class to aid the checking of more complex types

import abc
from types import UnionType

if __name__ == '__main__':
    from exceptions import InvalidDictionaryCheckerError , ParamsDoesNotMatchError, InvalidListCheckerError

else:
    from .exceptions import InvalidDictionaryCheckerError , ParamsDoesNotMatchError, InvalidListCheckerError

class Checker(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, value):
        pass

    @abc.abstractmethod
    def confirm_type(self, arg):
        pass

    def is_type(self, arg):
        try:
            self.confirm_type(arg)
            return True
        except:
            return False


class DictChecker(Checker):
    '''
    This is the class checker is for the dictionaries
    This dict checker can be used in different modes

    MODE 1 : Dict => The arguement must be a dictionary

    MODE 2 : Dict[type1, type2] => The arguement must have the key to 
    '''
    main_type = dict

    def __init__(self, *types) -> None:
        if types :
            if len(types) == 2:
                _key, _value = types
                if _key not in ( bool ,  int ,  str ,  float, tuple):
                    msg = f'The key "{_key}" is not a valid key type'
                    raise InvalidDictionaryCheckerError(msg)

                if type(_value) not in [type, UnionType, DictChecker, ListChecker]:
                    msg = f'The value "{_value}" is not a valid key type'
                    raise InvalidDictionaryCheckerError(msg)

                self.sub_types = types

            elif (len(types) == 1 and (type(types[0]) == dict)):
                for value in types[0].values():
                    if type(value) not in [type, UnionType, DictChecker, ListChecker]: # the allowed types for checking
                        msg = f'The value "{value}" is not supported by this dict checker'
                        raise InvalidDictionaryCheckerError(msg)

                self.sub_types = types[0]
                
            else:
                msg = f'The checking values {types} are not supported for the dict checker'
                raise InvalidDictionaryCheckerError(msg)
    
    def __getitem__(self, value):
        if type(value) == tuple:
            return DictChecker(*value)
        else:
            return DictChecker(value)

    def __str__(self) -> str:
        # The string display of the project
        # if type(self.sub_types) == tuple:
        #     return 'Dict []'
        return 'Dict'

    def confirm_type(self, arg : dict, arg_name : str | None):
        
        if type(arg) == self.main_type:

            if type(self.sub_types) == dict:

                for key, value in arg.items():
                    try:
                        type_to_check = self.sub_types[key]

                        if type(type_to_check) == type:
                            if type(value) != type_to_check:
                                msg = f'Error at arg => "{arg_name}" : the value "{value}" of key "{key}" is not of type "{type_to_check}" '
                                raise ParamsDoesNotMatchError(msg)

                        elif type(type_to_check) == UnionType:
                            if not isinstance(value, type_to_check):
                                msg = f'Error at arg => "{arg_name}" : the value "{value}" of key "{key}" is not of type "{type_to_check}" '
                                raise ParamsDoesNotMatchError(msg)
                                
                        elif type(type_to_check) in [DictChecker, ListChecker]:
                            try:
                                type_to_check.confirm_type(value)
                            except ParamsDoesNotMatchError:
                                msg = f'Error at arg => "{arg_name}" : the value "{value}" of key "{key}" is not of type "{type_to_check}" '
                                raise ParamsDoesNotMatchError(msg)

                    except KeyError:
                        msg = f'Error at arg => "{arg_name}" : The key "{key}" was not found in the dictionary checker'
                        raise ParamsDoesNotMatchError(msg)

            else:
                key_type ,value_type = self.sub_types

                for key, value in arg.items():
                    if type(key) != key_type:
                        msg = f'Error at arg => "{arg_name}" : The key "{key}" is not of type {key_type}'
                        raise ParamsDoesNotMatchError(msg)
                    
                    if type(value_type) == type:
                        if type(value) != value_type:
                            msg = f'Error at arg => "{arg_name}" : The value "{value} is not of type "{value_type}"'
                            raise ParamsDoesNotMatchError(msg)
                    
                    elif type(value_type) == UnionType:
                        if not isinstance(value, value_type):
                            msg = f'Error at arg => "{arg_name}" : The value "{value} is not of type "{value_type}"'
                            raise ParamsDoesNotMatchError(msg)

                    elif type(value_type) == DictChecker:
                        try:
                            value_type.confirm_type(value)
                        except ParamsDoesNotMatchError:
                            msg = f'Error at arg => "{arg_name}" : the value "{value}" of key "{key}" is not of type "{type_to_check}" '
                            raise ParamsDoesNotMatchError(msg)
        
        else:
            msg = f'Error at arg => "{arg_name}" : The argunemt {arg} is not of type dict'
            raise ParamsDoesNotMatchError(msg)


class ListChecker(Checker):
    '''
    This is a List Class checker
    '''
    main_type = list

    def __init__(self, *types) -> None:
        for type_item in types:
            if type(type_item) not in [type, UnionType, DictChecker, ListChecker, type(...)]:
                msg = f'The checking value {type_item} is not supported'
                raise InvalidListCheckerError(msg)

            if type(type_item) == type(...):
                if types.index(type_item) != (len(types) - 1):
                    msg  = 'A ellipsis can only be the last item in the list checker'
                    raise InvalidListCheckerError(msg)
        
        self.sub_types = types


    def __getitem__(self, value): 
        if type(value) != tuple:
            return ListChecker(value)
        return ListChecker(*value)

    @staticmethod
    def confirm_item(value, type_check, error_func):
        if type(type_check) == type:

            if type(value) != type_check:
                msg = error_func(value, type_check)
                raise ParamsDoesNotMatchError(msg)

        elif type(type_check) == UnionType:

            if not isinstance(value):
                msg = error_func(value, type_check)
                raise ParamsDoesNotMatchError(msg)

        elif type(type_check) in [DictChecker, ListChecker]:

            if not type_check.is_type(value):
                msg = error_func(value, type_check)
                raise ParamsDoesNotMatchError(msg)
                


    def confirm_type(self, arg : list, arg_name : str | None):
        if type(arg) == self.main_type:
            if len(self.sub_types) == 1:
                type_to_check = self.sub_types[0]
                for item in arg:
                    self.confirm_item(item, type_to_check, 
                                lambda _val, _type : f'Error at arg => "{arg_name}" : The value "{_val}" is not part of the type {_type}' )

            else:
                for item in arg:
                    ind = arg.index(item)
                        
                    try:
                        self.confirm_item(item, self.sub_types[ind], 
                                    lambda _val, _type : f'Error at arg => "{arg_name}" : The value "{_val}"  at index "{ind}" is not of the type {_type}')
                    except IndexError:
                        if type(self.sub_types[-1]) != type(...):
                            msg = f'Error at arg => "{arg_name}" : The List does not match the length of the Checker. Try putting "..." at the end'
                            raise ParamsDoesNotMatchError(msg)
        
        else:
            msg = f'Error at arg => "{arg_name}" : The value of this argument "{arg}" is not of type list'
            raise ParamsDoesNotMatchError(msg)


                    
                        
                        
                    

Dict = DictChecker()
List = ListChecker()

if __name__ == '__main__':

    List[int, str, ...].confirm_type([1,2,'pols'])
    # f = Dict[{
    #     'pol' : int,
    #     "polas" : str | int
    # }]

    # f.confirm_type({'polas' : 'polas', 'pol' : 1})


