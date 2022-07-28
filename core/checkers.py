# The class to aid the checking of more complex types

import abc
from types import GenericAlias, UnionType
from exceptions import InvalidDictionaryCheckerError, ParamsDoesNotMatchError


class Checker(abc.ABC):
    @abc.abstractmethod
    def __getitem__(self, value):
        pass

    @abc.abstractmethod
    def confirm_type(self, arg):
        pass


class DictChecker(Checker):
    main_type = dict

    def __init__(self, *types) -> None:
        if types :
            if len(types) == 2:
                self.sub_types = types
                for value in types:
                    if type(value) not in [type, UnionType, DictChecker]: # the allowed types for checking
                        msg = f'The value "{value}" is not supported by this dict checker'
                        raise InvalidDictionaryCheckerError(msg)

                self.sub_types = types

            elif (len(types) == 1 and (type(types[0]) == dict)):
                for value in types[0].values():
                    if type(value) not in [type, UnionType, DictChecker]: # the allowed types for checking
                        msg = f'The value "{value}" is not supported by this dict checker'
                        raise InvalidDictionaryCheckerError(msg)

                self.sub_types = types[0]
                
            else:
                msg = f'The checking values {types} are wrong are not supported for the dict checker'
                raise InvalidDictionaryCheckerError(msg)
    
    def __getitem__(self, value):
        if type(value) == tuple:
            return DictChecker(*value)
        else:
            return DictChecker(value)

    def confirm_type(self, arg : dict):
        if type(arg) == self.main_type:

            if type(self.sub_types) == dict:

                for key, value in arg.items():
                    try:
                        type_to_check = self.sub_types[key]

                        if type(type_to_check) == type:
                            if type(value) != type_to_check:
                                msg = f"the value '{value}' of key '{key}' is not of type '{type_to_check}' "
                                raise ParamsDoesNotMatchError(msg)
                    except KeyError:
                        msg = f'The key "{key}" was not found in the dictinary checker'
                        raise ParamsDoesNotMatchError(msg)
            else:
                pass



if __name__ == '__main__':
    Dict = DictChecker()

    f = Dict[{'pol' : int}]

    f.confirm_type({'polas' : 1})
