import time
import functools
import logging
from threading import Lock
from typing import get_type_hints
import pstats
import cProfile
import io


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


    @staticmethod
    def retry(exceptions, max_attempts=3, delay=1, backoff=2, logger=None):
        def decorator_retry(func):
            @functools.wraps(func)
            def wrapper_retry(*args, **kwargs):
                nonlocal delay
                attempts = 0
                while attempts < max_attempts:
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        attempts += 1
                        if attempts < max_attempts:
                            msg = f"retrying {func.__name__} in {delay} \
                                   seconds ({attempts}/{max_attempts}), \
                                    due to {e}."
                            if logger:
                                logger.warning(msg)
                            else:
                                print(msg)
                            time.sleep(delay)
                            delay *= backoff
                        else:
                            msg = f"Max retries reached for {func.__name__}. \
                                 Function failed with {e}."
                            if logger:
                                logger.error(msg)
                            raise
            return wrapper_retry
        return decorator_retry
    

    @staticmethod
    def profile(output_file=None, sort_by='cumulative', lines_to_print=None,
                strip_drirs=False):
        def decorator_profile(func):
            @functools.wraps(func)
            def wrapper_profile(*args, **kwargs):
                profiler = cProfile.Profile()
                try:
                    profiler.enable()
                    result = func(*args, **kwargs)
                    profiler.disable()
                    return result
                finally:
                    s = pstats.Stats(profiler).sort_stats(sort_by)
                    if strip_drirs:
                        s.strip_dirs()
                    if output_file is not None:
                        with open(output_file, 'w') as f:
                            s.stream = f
                            s.print_stats(lines_to_print)
                    else:
                        s.print_stats(lines_to_print)

            return wrapper_profile
        return decorator_profile
    
    @staticmethod
    def permission_checking(required_permission):
        def decorator(func):
            def wrapper(user, *args, **kwargs):
                if required_permission not in user.permissions:
                    raise PermissionError("Insufficient Permissions")
                return func(user, *args, **kwargs)
            return wrapper
        return decorator