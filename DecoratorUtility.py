import time
import functools
import logging
from threading import Lock
from typing import get_type_hints


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
    
    @staticmethod
    def validate_arguments(func):
        @functools.wraps(func)
        def wrapper_validate_arguments(*args, **kwargs):
            type_hints = get_type_hints(func)
            for arg, hint in zip(args, type_hints.values()):
                if not isinstance(arg, hint):
                    raise TypeError(f"Argument {arg} is not of type {hint}")
                
            for kwarg, value in kwargs.items():
                if kwarg in type_hints and not isinstance(value, type_hints[kwarg]):
                    raise TypeError(f"Argument {kwarg}={value} is not of type {type_hints[kwarg]}")
                
            return func(*args, **kwargs)
        return wrapper_validate_arguments


    @staticmethod
    def format_output_for_logging(report_format):
        def decorator_format_output(func):
            @functools.wraps(func)
            def wrapper_format_output(*args, **kwargs):
                result = func(*args, **kwargs)
                args_str = ', '.join(map(str, args))
                kwargs_str = ', '.join(f"{k}={v}" for k,v in kwargs.items())
                all_args_str = ', '.join(filter(None, [args_str, kwargs_str]))
                log_message = report_format.format(
                    func_name=func.__name__,
                    result=result,
                    args=all_args_str
                )

                logging.info(log_message)

                return result
            return wrapper_format_output
        return decorator_format_output
