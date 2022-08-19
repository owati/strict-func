# strict-func
### A python package to make a function strictly apply the parameters it receives
---

## Example
```
from strict_func.core import strict_func

@strict_func
def foo(a : int, b : str):
    # do something


foo('foo', 'bar') # raises an error 
```
---
## Supported Annotations for checking
### Currently, **strict-func** cannot check for all possible annotations. The table below shows the current possible types

|Annotation types | Descriptions| Examples |
|--------- | ------------| ------------|
|Standard types| `type(annot) == type` | int, str, list, dict, classes etc...
|Union types| `type(annot) == UnionType` | `int \| str`
|Checker types | `strict_func.checkers` | Dict, List

---
## Using Standard types
### **strict_func** supports standard types annotations. You can use custom python types and other types as annotation for the function.
## Example
```
class Bar:
    pass

class Foo:
    pass

@strict_func
def fooBar(foo : Foo, bar : Bar):
    # do something

fooBar(Bar(), Foo()) # raises an error
```
---
## Using Union Types
### **strict_func** also supports union types annotations. These are used when a parameter can be either of the union.
```

@strict_func
def fooBar(foo : int | str, bar : list | str):
    # do something

fooBar('foo', 'bar') #  no error
```
---
## Using Checker Types
### **strict_func** currently has two checker types *Dict* and *List* for the dictionaries and lists respectively. They are used to further check not only only the list and dictionaries but the items the contain

```
from strict_func.checkers import List, Dict
```
## List 
### For a list with only type of items `List[type]`,  or a union of types `List[type1 | type2]`
```
@strict_func
def foo(a : List[int]):
    # do something


foo([1,3,4,5,6]) # no error
foo([1,2,3,'foo']) # raises an error
```
### For a list with specific sequence of items `List[type1, type2, type3]`
```
@strict_func
def foo(a : List[int, str, list]):
    # do something


foo([1,'foo', [1,2]]) # no error
foo([1,2,3]) # raises an error
```
>### Note : The number of types must the length of the list parameter.
> To resolve this add `...` at the end of the type list.  `List[type1, type2, ...]`

## Dict 
### For a dictionary with only one type of key - value pair  `Dict[keyType, valueType]`
```
@strict_func
def foo(a : Dict[str, int]):
    # do something


foo({'age' : 2}) # no error
foo({'name' : 'foo'}) # raises an error
```
### For a dictionary with specific keys and corresponding value type `Dict[{keyName : valueType}]`
```
@strict_func

checker = Dict[{
    'name' : str,
    'age' : int, 
    'scores' : list
}]
def foo(a : checker):
    # do something


foo({
    'name' : 'foo',
    'age' : 9, 
    'scores' : [10, 9, 10]
}) # no error

foo({'name' : 21}) # raises an error
```
>### Note : All keys in the dictionary parameter must match the dict checker
---








