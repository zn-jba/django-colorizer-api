# both approaches work

# def do_twice(function):
#     def wrapper(args_for_function):
#         return function(args_for_function), function(args_for_function)
#     return wrapper

def do_twice(function):
    def wrapper(args_for_function):
        function(args_for_function)
        return function(args_for_function)
    return wrapper


@do_twice
def print_message(message: str) -> None:
    print(message)
