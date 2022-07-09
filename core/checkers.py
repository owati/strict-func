# The class to aid the checking of more complex types

import abc
from types import GenericAlias

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

        print(self.main_type, self.other_types), len
        if ('[' in self.other_types):
            error_msg = 'The generic alias cannot contain another generic alias'
            raise InvalidGenericAliasError(error_msg)

        if (self.main_type == 'dict'):
            if (len(self.other_types.split(',')) != 2):
                error_msg = f'The type {gen_type} is invalid as the dict needs only a key type and a value type'
                raise InvalidGenericAliasError(error_msg)
            else:
                pass


    def is_type(value) -> bool:
        return True


if __name__ == '__main__':
    check = GenericAliasChecker(dict[str, int | list[int]])