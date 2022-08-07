from core.strict_func import Strict_func
from core.checkers import Dict, List

@Strict_func
def test_func(p : int, g : Dict[str,int | str], *args):
    print(p)
    

test_func(2,{'st' :  'str'},12,123,123)
