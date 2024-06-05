# x # ignored => no error
# print(x) # error
x = 5

number: int
# print(number) => error
number = 10

# camelCasing => underscores
teacher_name: str = "Aarti"

# datatypes are for showing intent
prime_number: int = "abcd"
prime_number = "11"

print(prime_number)