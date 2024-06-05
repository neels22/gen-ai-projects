is_hungry: bool = True

# comparison operators
1 == 1 # T 
1 == "1" # F
1 == False # F
0 == False # T
1 == True # T
5 == True # F
1 == [] # F
"" == 0 # F
arr1 = []
arr2 = []
 # T 
isEq = id(arr1) == id(arr2) # F
print(id([]))
print(id([1, 2])) # figure this out
print(isEq)


print(0 < True)
# print(1 < "abcd") # ERROR

# logical operators
# AND OR NOT
# AND and
True and True # T
True and False # F
False and False # F
False and True # F

True or True # T
True or False # T
False or False # F
False or True # T

not True # F
not False # T

input_age = 18
legal_age = 25
adult_age = 18

if input_age >= legal_age:
    print("3rd floor")
elif input_age >= adult_age:
    print("2nd floor")
else:
    print("1st floor")

# ternary => AVOID THIS
is_legal = True if input_age > adult_age else False


# Falsy & truthy
# 0, "", False, None, [], {}, ()
# print(bool([]))
if bool([]) == False:
    print("should not print")

# or => first truthy value
# or => last falsy value
name = "a" or "abcd"
print(name)

# and => first falsy value
# and => last truthy value
name = "" and "abcd"
print(name)

if "" and 0 or "abcd" and False:
    print("true")

