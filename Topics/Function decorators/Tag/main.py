def tagged(func):
    def wrapper(arg):
        return "<title>" + func(arg) + "</title>"
    return wrapper


# @tagged
# def from_input(inp):
#     return inp.strip()
#
#
# print(from_input("Test"))
