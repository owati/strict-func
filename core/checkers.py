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
                _key, _value = types
                if _key not in ( bool ,  int ,  str ,  float):
                    msg = f'The key "{_key}" is not a valid key type'
                    raise InvalidDictionaryCheckerError(msg)

                if type(_value) not in [type, UnionType, DictChecker]:
                    msg = f'The value "{_value}" is not a valid key type'
                    raise InvalidDictionaryCheckerError(msg)

                self.sub_types = types

            elif (len(types) == 1 and (type(types[0]) == dict)):
                for value in types[0].values():
                    if type(value) not in [type, UnionType, DictChecker]: # the allowed types for checking
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
        pass

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

                        elif type(type_to_check) == UnionType:
                            if not isinstance(value, type_to_check):
                                msg = f"the value '{value}' of key '{key}' is not of type '{type_to_check}' "
                                raise ParamsDoesNotMatchError(msg)
                                
                        elif type(type_to_check) == DictChecker:
                            try:
                                type_to_check.confirm_type(value)
                            except ParamsDoesNotMatchError:
                                msg = f"the value '{value}' of key '{key}' is not of type '{type_to_check}' "
                                raise ParamsDoesNotMatchError(msg)

                    except KeyError:
                        msg = f'The key "{key}" was not found in the dictinary checker'
                        raise ParamsDoesNotMatchError(msg)
            else:
                pass



if __name__ == '__main__':
    Dict = DictChecker()

    f = Dict[int, int]

    f.confirm_type({'polas' : 1})
