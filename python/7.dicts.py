dynamic_key = "is_hungry"

chess_player = {
    "name": "magnus carlson",
    'age': 32,
    """did_lose""": False,
    f"{dynamic_key}": True,
    "plays_cricket": None,
    "trophies": ["A", "B", "C"],
    "address": {
        "country": "Norway"
    },
    # dynamic_key,
}

# access values
chess_player["name"] # "magnus carlson"
chess_player[dynamic_key] # True
# chess_player["abcd"] => ERROR

# modify values
chess_player["age"] += 1

# add key value pairs
chess_player["abcd"] = "kjsa"
print(chess_player["abcd"])

del chess_player["""did_lose"""]
chess_player.pop("abcd")

chess_player.popitem() # DO NOT USE
print(chess_player)

chess_player.keys() # -> dict_keys of list of keys
print(chess_player.values()) # -> dict_values of list of values
chess_player.items()    # -> dict_items of list of tuples

# *
product = { 
    "name": "bottle",
    "price": 500
}

name = [*product]

# ** is the spread operator for dicts
spread = {**product}
print(name, spread)

