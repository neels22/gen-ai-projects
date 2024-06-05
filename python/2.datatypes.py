# int & float

integer: int = 10
decimal: float = 12.5

print(type(integer))
print(type(decimal))

# string -> str
single_quotes: str = 'this is a string'
double_quotes: str = "this is also a string"
multi_line_string: str = """ 
this is a multiline
string
"""

print(type(single_quotes))
print(type(double_quotes))
print(type(multi_line_string))

# booleans -> bool
is_python: bool = True
is_javascript: bool = False

print(type(is_python))
print(type(is_javascript))

null_value = None # NEVER DO THIS

print(type(null_value))

# collection datatypes
# list [array], dictionary [object], tuple

numbers: list[int] = [1, 2, 3, 4, 5]
strings: list[str] = ["a", "b", "c"]

from typing import Any
anything: list[Any] = [1, 1.5, "a", False, None, [1, 2, 3], { "name": "abcd" }]

numbers_tuple: tuple[int] = (1, 2, 3, 4)
names_tuple = ("aniruddha",) # remember the comma
# names_tuple = ()

print(type(names_tuple))


from typing import TypedDict

class Person(TypedDict):
    age: int
    name: str
    is_hungry: bool

# dictionary
person: Person = {
    "name": "abcd",
    "age": 20,
    "is_hungry": False
}

print(type(person))

def add():
    print('adding')

print(type(add))