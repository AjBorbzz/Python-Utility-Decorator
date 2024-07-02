import time
import functools
import logging
from threading import Lock

class DecoratorUtility:
    @staticmethod
    def timer(func):
        """Measure the execution time of a function."""
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            start_time = time.perf_counter()
            value = func(*args, **kwargs)
            end_time = time.perf_counter()
            elapsed_time = end_time - start_time
            print(f'Function {func.__name__!r} took {elapsed_time:.4f} seconds')
            return value
        return wrapper_timer
    

    @staticmethod
    def debug(func):
        """Prints the function signature and return value"""
        @functools.wraps(func)
        def wrapper_debug(*args, **kwargs):
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k,v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)
            print(f"Calling {func.__name__}({signature})")
            value = func(*args, **kwargs)
            print(f"{func.__name__!r} returned {value!r}")
            return value
        return wrapper_debug
    

    @staticmethod
    def synchronized(lock):
        """Synchronize the decorated function using the given lock."""
        def decorator(func):
            @functools.wraps(func)
            def wrapper_synchronize(*args, **kwargs):
                with lock:
                    return func(*args, **kwargs)
            return wrapper_synchronize
        return decorator
            

    @staticmethod
    def deprecated(func):
        """Mark functions as deprecated."""
        @functools.wraps(func)
        def wrapper_deprecated(*args, **kwargs):
            print(f"Warning: Function {func.__name__} is deprecated")
            return func(*args, **kwargs)
        return wrapper_deprecated
    

    @staticmethod
    def cache_results(func):
        cache = {}
        @functools.wraps(func)
        def wrapper_cache(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return wrapper_cache