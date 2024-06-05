#                     0  1  2  3  4
numbers: list[int] = [1, 2, 3, 4, 5]
#                    -5  4  3  2  1

# length
list.__len__(numbers)
numbers.__len__()
len(numbers)

numbers[0] # 1
# numbers[5] # error
numbers[-1] # 5

numbers[0] = 10 # lists are mutable
# [10, 2, 3, 4, 5]

numbers.append(6) # -> None
# [10, 2, 3, 4, 5, 6]

numbers.insert(0, 0) # -> None
# [0, 10, 2, 3, 4, 5, 6]

# pop accepts either nothing or an index
numbers.pop() # -> 6
# [0, 10, 2, 3, 4, 5]

numbers.pop(1) # -> 10

from typing import TypedDict

class Person(TypedDict):
    name: str

people: list[Person] = [
    { "name": "A" },
    { "name": "B" },
    { "name": "C" }
]

people.pop(1)
people.insert(1, { "name": "D" })

numbers.remove(4)
# [0, 10, 2, 3, 5]

print(numbers)

people.remove({ "name": "C" })

print(people)

shubham_friends = [
   { "name": "shreya" },
    {"name": "yashraj"}
]

# copying the reference
teja_friends = shubham_friends

print(teja_friends)
print(shubham_friends)

teja_friends.append({ "name": "divij" })

print(teja_friends)
print(shubham_friends)

# neha_friends = shubham_friends[:]
neha_friends = shubham_friends.copy()
neha_friends.append({ "name": "aniruddha" })

print(shubham_friends)
print(neha_friends)

# neha_friends[0] = { "name": "Akshaya" } 
neha_friends[0]["name"] = "akshaya" # SHALLOW

print(shubham_friends)
print(neha_friends)

# HW => deepclone

# DESTRUCTURING => unpacking

words = ["the", "bottle", "chair", "tv", "wire"]
chair, the, bottle, *r = words

# ch, the = words => MUST UNPACK ALL THE VALUES
t, _, *c = words # _ represents value is ignored

print(chair, the, bottle)

the, *rest = words

# * on left of = is rest operator of js
print(the, rest)

the, *rest, wire = words

print(the, rest, wire)

*al, wire = words

print(al, wire)

# only 1 * is allowed on left hand side
# *one, chair, *two = words

words_copy = [*words]

odd = [1, 3, 5]
even = [2, 4, 6]

odd_and_even = [*odd, *even]


# tuples
#        0         1          2
names = ([0, "a"], (1, "b"), (3, "d"))
#        -3         -2        -1
names[0] # (0, "a")
names[0][0] # 0

print(names[-1]) # 

# print(names[5]) # error

print(names[::-1])
names[1:2] # ((1, "b"))
names[1:] # ((1, "b"), (2, "c"))
names[:3] # ((0, "a"), (1, "b"), (2, "c"))
names[:4] # 

# names[0] = (5, "e") => ERROR

names[0][0] = 5

# names = names.__add__((5, "e"))

names = names + ((5, "e"), )

print(names)

names = names[0:2] + ((2, "c"),) + names[2:]

print(names)

names = names[:2] + names[3:]
print(names)

names.count((1, )) # 0
# names.index((1, "c")) # error

things = ("chair", "bottle", "TV")
bottle, chair, tv = things
print(chair, bottle, tv)

# rest of the things is going to be a list
chair, *rest_of_the_things = things

print(chair, type(rest_of_the_things))

rest_of_the_things[0] = "wire"
print(chair, rest_of_the_things)

another_tuple = (*things, )

print(another_tuple)

alphabet_map = ((0, "b"), (0, "a"), (2, "c"))

# cnt = alphabet_map.index((0, "c"))
# print(cnt)

# list methods

alphabets = ["a", "b", "c"]

alphabets.index("a") # 0
# alphabets.index("d") # error

# alphabets[::-1].index("a")

alphabets.count("a") # 7
alphabets.count("d") # 0

# map, filter, reduce only after learning lambdas