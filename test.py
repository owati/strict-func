from core.strict_func import strict_func

@strict_func
def test_func(p : int | str, g : str, *args : tuple[int , ...]):
    print(p)
    

test_func('we','9',12,123,123)