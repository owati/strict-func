# The class to aid the checking of more complex types

import abc
from types import GenericAlias
from core.exceptions import ParamsDoesNotMatchError

from exceptions import InvalidGenericAliasError

class Checker(abc.ABC):
    @abc.abstractmethod
    def is_type(value) -> bool:
        pass


class GenericAliasChecker(Checker):
    '''
    Checks the values of the generic alias
    This check will throw an error when a generic alias 
    contains another generic alis
    '''

    def __init__(self, gen_type : GenericAlias) -> None:
        split_list = str(gen_type).split('[', maxsplit=1)
        self.main_type = split_list[0]
        self.other_types = split_list[1][:-1]

        print(self.main_type, self.other_types)
        if ('[' in self.other_types):
            error_msg = 'The generic alias cannot contain another generic alias'
            raise InvalidGenericAliasError(error_msg)

        if (self.main_type == 'dict'):
            if (len(self.other_types.split(',')) != 2):
                error_msg = f'The type {gen_type} is invalid as the dict needs only a key type and a value type'
                raise InvalidGenericAliasError(error_msg)
            else:
                pass


    def is_type(self,value) -> bool | None:
        if str(type(value)) == self.main_type:
            types_list = self.other_types.split(' ,')

            if self.main_type == 'list':
                # when the value is of type list
                if len(types_list) == 1:
                    # when the parametized types of the list is just one
                    for _value in value:
                        if type(_value) != types_list[0]:
                            error_msg = f''

                if (len(value) != len(types_list)):
                    error_msg = 'The length of the value does not match the length of the type specified'
                    raise ParamsDoesNotMatchError(error_msg)

            for types in self.other_types.split(','):
                pass
        else:
            error_msg = f'the value is not of type {self.main_type}'
            raise ParamsDoesNotMatchError(error_msg)


if __name__ == '__main__':
    check = GenericAliasChecker(list[int, str, int])