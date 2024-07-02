from DecoratorUtility import DecoratorUtility

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

# Tests
# run_timer_decorator(100)
# print(make_greeting('AJ', age=37))
print(some_computation(1,2,3,4,5,6,7,8))
print(some_computation(1,2,3,4,5,6,7,8,9)) # This will use the cached result