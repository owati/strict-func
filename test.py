from core.strict_func import Strict_func

@Strict_func
def test_func(p : int, g : str, *args):
    print(p)
    

test_func('we','9',12,123,123)
