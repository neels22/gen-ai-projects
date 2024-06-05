from datetime import datetime

# def log_time(cb):
#     def inner(*args, **kwargs):
#         print(datetime.now())
#         return cb(*args, **kwargs)
    
#     return inner

def log_time(config):
    # lt -> actual decorator
    def lt(cb):
        def inner(*args, **kwargs):
            if(len(config) > 3):
                print(datetime.now())
                return cb(*args, **kwargs)
            raise "INVALID CONFIG"
    
        return inner
    return lt

# @log_time
@log_time([1,2,3,4])
def save_user(user):
    # time()
    print(user)
    print("user saved")
    return True

# @log_time
@log_time([1,2,3,0])
def save_product():
    # time()
    print("product saved")
    return False

# log_time(save_user, "abcd")
# log_time(save_product)
    
# save_user = log_time(save_user)

# ref_to_lt = log_time([1, 2, 3])
# save_user => reference to inner
# save_user = ref_to_lt(save_user)

# save_user = log_time([1, 2, 3])(save_user)
save_user(1)

print(save_user(1))
print(save_user(2))

# save_product = log_time(save_product)
save_product()
