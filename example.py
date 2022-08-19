from strict_func.core import strict_func
from strict_func.checkers import Dict, List


start = Dict[{
    "pols" : int,
    "polas" : str
}]

check_list = List[int, str]

@strict_func
def test_func(p : int, g : check_list, *args):
    print(p)
    

test_func(2,[9, 1],12,123,123)
