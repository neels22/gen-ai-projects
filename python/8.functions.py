def add(n1, n2):
    return n1 + n2

addtion = add(4, 5) # 9
# add() # ERROR
# add(4) # ERROR

def subtract(n1: int, n2: int) -> int:
    return n1 - n2


# add()
# subtract()

def multiply(n1: int, n2:int) -> int:
    """
    @param n1: int
    @param n2: int

    @return int
    """
    return n1 * n2


add # => reference to the fn expression
add(2, 5) # => execute code at reference

add_fn = add

# print(add_fn(5, 4)) # 9

# lambdas
from typing import Callable

divide: Callable[[int, int], int] = lambda n1, n2: n1 / n2 
"""param: n1 int, param: n2 int"""

# divide.__doc__ = """param: n1 int, param: n2 int"""
divide(6, 3)

from typing import TypeVar

# GENERICS
T = TypeVar('T')

def find(array: list[T], elem: T) -> T | None:
    for elem_in_arr in array:
        if elem == elem_in_arr:
            return elem

elem = find([1, 2, 3, 4, "4"], 4)
elem = find(["a", "b", "c"], "c")


names = ["a", "b", "c"]

def find_name(index):
    # access names from the global scope
    # global names
    names = ["p", "q", "r"]
    return names[index]

# print(find_name(0))
# print(names)

# roi = 10

def loan_factory(rate_of_interest):
    # global roi
    roi = 8
    def calculator(p, n):
        return p * n * rate_of_interest / 100
    
    def updateRate(updatedRate):
        # nonlocal roi
        # global roi
        # roi = 7
        nonlocal rate_of_interest
        rate_of_interest = updatedRate * roi
    
    return [calculator, updateRate]


# car_emi_calc, upate_car_rate = loan_factory(8)
# home_emi_calc = loan_factory(10)
# personal_emi_calc = loan_factory(12)

# print(car_emi_calc(10000, 10))
# upate_car_rate(10)
# print(car_emi_calc(10000, 10))






def sum(*numbers: list[int]) -> int:
    addition = 0
    for number in numbers:
        addition += number

    return addition

sum(1, 2, 3, 4, 5, 6)

from typing import Callable

def validate(input, *pipeline: list[Callable]):
    
    for validator in pipeline:
        result = validator(input)
        if not result:
            return False
        
    return True

def check_type(dt):
    return lambda input: type(input) == dt

def has_length(length: int):
    return lambda input: len(input) == length

validators = {
    "is_string": check_type(str),
    "is_integer": check_type(int),
    "has_length": has_length
}

# print(type("") == "str")
# developers code
# print(validate('abcd', validators["is_string"], validators["has_length"](5)))
# print(validate(10, validators["is_integer"], lambda input: input < 15))
# print(validate({ "name": "abcd" }, lambda input: type(input) == dict))

def extract_query(url: str):
    query_strings = url.split(sep="?")[1].split("&")
    query = {}
    for query_string in query_strings:
        key = query_string.split("=")[0]
        value = query_string.split("=")[1]
        query[key] = value

    return query


def handle_user(name="", height=""):
    print("handling users...")
    print(name, height)

def handle_product(name, color, size, price):
    print("handling users...")
    print(name, color, size, price)

handler_map = {
    "user": handle_user,
    "product": handle_product
}

def handle_request(url: str) -> None:
    query = extract_query(url)
    endpoint = url.split("/")[1].split("?")[0]
    handler_map[endpoint](**query)

# handle_request("www.example.com/user?name=ani&height=2.7")

# positional arguments
# args => *args 
# keyword arguments => kwargs => **kwargs

def handler(*args, **kwargs):
    print(args)
    print(kwargs)

# handler(
#     1, "a", False, None, [1, 2, 4], (1, 2, 3), { "name": "a" }, # => ARGS
#     name="abcd", space="4", sep="asd"
# )


# def authorize(roles):
#     def inner(incoming_role, func):
#         if(incoming_role in roles):
#             return func
        
#         return lambda: "abcd"
        
#     return inner

# @authorize([])
# def delete_profile():
#     print("deleting profile")

# @authorize(['admin', 'hr'])
# def delete_documents():
#     print("deleting document")

# delete_profile = authorize(['admin', 'hr'], delete_profile)
# delete_documents = authorize(['hr'], delete_documents)


# delete_profile("admin")

def log(to_print):
    def inner_log(func):
        if(to_print):
            print("function called")
        return func
    
    return inner_log

# @log(True)
# def message():
#     print("this is a message")

@log(False)
def message2(name):
    print("this is a message2", name)

# message()
# message2("abcd")


def logger(permission):
    def actual_decorator(func):
        print("actual decorator")
        def duplicate_message(role, *args, **kwargs):
            if(role in permission):
                func(*args, *kwargs)
            else:
                print("not authorized")
            print("this is not original")
            
        return duplicate_message
    
    return actual_decorator


@logger(["admin"])
def message(name, age):
    print("this is a message", name, age)

# message = logger()(message)

message("admin")
# message()




