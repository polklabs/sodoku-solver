# Making decorator to log time processed
import time 

def calculate_time(func): 
    def inner1(*args, **kwargs): 
        begin = time.time() 
        returned_value = func(*args, **kwargs) 
        end = time.time()
        print("##################################################")
        print("Total time taken in : ", func.__name__, "{:.4f}".format(end - begin), " seconds")
        print("##################################################")
        return returned_value
    return inner1 

def memoize(func): 
    cache = dict()
    def inner1(*args): 
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    return inner1 