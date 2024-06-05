message: str = "this is a message for"
# idx        012345678
name: str = "aniruddha"
# idx -     -987654321        

# access elements (char)

name[0] # a
# name[10] # ERROR
name[-9] # a
# name[-10] # ERROR

# name[0] = "p" # ERROR => IMMUTABILITY

# concat
# +
concat_message = message + " " + name
print(concat_message)

# {} => f
message = f"{message} {name}"
print(message)

# len
sentence = "this is a sentence"
length = len(sentence)
print(length)

length = sentence.__len__()
print(length)

length = str.__len__(sentence)
print(length)

# slicing => substrings
# [1:2:3]
# 1 => starting index (optional)
# 2 => ending index (excluding)(optional)
# 3 => step (optional)

#       012345
word = "bottle"
#      -654321
word[::] # bottle
print(word[0:10]) # bottle
print(word[0:5]) # bottl
print(word[2:5]) # ttl
print(word[:3]) # bot
print(word[-1:10]) # e
print(word[-1:0:-1]) # e 
# btl
print(word[0:5:2])
print(word[-6:-1:2])
print(word[0:-1:2])
print(word[-6:5:2])
# tle
word[3:]
# ltb
word[-2::-2]
print(word[4:-7:-2])
print(word[4::-2])
print(word[-2:-7:-2])