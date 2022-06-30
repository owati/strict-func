import inspect

def strict_func(func):

    def inner(*args, **kwargs):

        annot : dict= func.__annotations__
        arguements = inspect.getfullargspec(func)
        print(annot, arguements)
        if annot:
            annot_items = list(annot.items())
            for i in range(len(args)):
                param = args[i]
                
                if(type(param) != annot_items[i][1]):
                    raise ValueError('The value does not the type')

        value = func(*args, **kwargs)

        return value
    return inner
