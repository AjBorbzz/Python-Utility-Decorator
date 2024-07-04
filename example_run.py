from DecoratorUtility import DecoratorUtility
import logging

@DecoratorUtility.timer
def run_timer_decorator(run_times):
    for _ in range(run_times):
        sum([i**2 for i in range(10000)])


@DecoratorUtility.debug
def make_greeting(name, age=None):
    greeting = f"Hello {name}"
    if age:
        greeting += f", you are {age} years old."
    return greeting

@DecoratorUtility.cache_results
def some_computation(*args):
    print(f"computing with args: {args}")
    return sum(args)


@DecoratorUtility.validate_arguments
def process_data(name: str, age: int, height: float):
    print(f"Name: {name}, Age: {age}, Height: {height}")



@DecoratorUtility.format_output_for_logging(report_format="{func_name} called with {args} returned {result}")
def calculate_sum(*numbers):
    return sum(numbers)


@DecoratorUtility.retry(exceptions=(ValueError, KeyError),
                        max_attempts=5,
                        delay=2,
                        logger=logging.getLogger(__name__))
def test_retry_func(param):
    if param == 1:
        raise ValueError("Invavlid Value")
    elif param ==2:
        raise KeyError("Invalid Key")
    return "Success"

try:
    result = test_retry_func(1)
    print(result)
except Exception as e:
    print("Function failed after retries: {e}")


@DecoratorUtility.profile(output_file='profile_stats.txt', lines_to_print=10,
                        strip_drirs=True)
def function_to_profile():
    # some process here
    print("Hello")

# function_to_profile()
# Tests
# run_timer_decorator(100)
# print(make_greeting('AJ', age=37))
# print(some_computation(1,2,3,4,5,6,7,8))
# print(some_computation(1,2,3,4,5,6,7,8,9)) # This will use the cached result
# process_data("Aj", 37, 5.5)
# process_data("Bob", "Thirty Eight", 6.2)
# calculate_sum(1,2,3,4,5,6,7,8)

