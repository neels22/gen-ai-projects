num1: int = 10
num2: int = 2

addition: int = num1 + num2
difference: int = num1 - num2
product: int = num2 * num1
division: float = num1 / num2
print(division)
division: int = num1 // num2 
print(division)
remainder = num1 % num2 
power = num1 ** num2
print(power)

number = 0
number += 1
print(number)

from random import random
import math

random()
print(math.floor(3.1)) # 3
math.ceil(3.1) # 4

num = -3
print(abs(num)) # 3
# DUNDER METHODS => SPECIAL METHODS
print(num.__abs__()) # 3
print(int.__abs__(num)) # 3