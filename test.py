from core.strict_func import strict_func

@strict_func
def test_func(p : int, g : str, *args : int):
    print(p)
    

test_func(2,3,12,123,123)