""" This module demonstrates a decorator which adds support for traditional function/method overloading in Python. """

from typing import Callable, Any
import inspect


# def test(a, b):
#     pass
#
# def test2(b=2):
#     pass
#
# def test3(c: int):
#     pass
#
# def test4(d: str = None):
#     pass
#
# sig1 = tuple(inspect.signature(test).parameters.values())
# sig2 = tuple(inspect.signature(test2).parameters.values())
# sig3 = tuple(inspect.signature(test3).parameters.values())
# sig4 = tuple(inspect.signature(test4).parameters.values())


def overload(func: Callable, /, _function_cache={}) -> Callable:
    """
    Decorator which adds support for traditional function overloading.
    :param func: Function which should be overloadable.
    """

    # TODO Kevin: Perhaps use func.__qualname__ to provide support for class methods.
    # TODO Kevin: Adds support for typing typehints, such as Union.

    targets = _function_cache.get(func.__qualname__, {})

    #test = tuple(inspect.signature(func).parameters.values())

    # Constructs a tuple for the overloaded signature.
    # Prioritizes the annotated types over the types of default values.
    # 'Any' from typing will be used when both are absent.
    param_tuple = tuple(
        (arg.annotation if arg.annotation is not inspect._empty else type(arg.default) if arg.default is not inspect._empty else Any)
        for arg in inspect.signature(func).parameters.values()
    )

    if param_tuple in targets:
        # The user probably didn't provide either typehints or default values
        # for an overloaded function with an equal amount of parameters to a previous one by the same name.
        # We raise an exception in this case, instead of overriding the function, to prevent unexpected behavior.
        raise KeyError(f"Identical overloaded signature ({param_tuple}) for '{func.__qualname__}' already exists.")

    targets[param_tuple] = func
    _function_cache.update({func.__qualname__: targets})  # Merge the new overload into the function cache.

    def wrapper(*args, **kwargs):

        params = tuple(type(arg) for arg in (args + tuple(kwargs.values())))

        try:  # Attempt to find an exact match for the overload.
            runfunc = _function_cache[func.__qualname__][params]
        except KeyError:  # Inform the user when this fails.
            # TODO Kevin: We could attempt to find a satisfactory function when an exact match is absent.
            #   This might sound like a bad idea, but one has to consider the fact that Python supports optional
            #   arguments. These mean that the provided arguments needn't match the signature.
            raise KeyError(f"Cannot find a matching overload for function '{func.__qualname__}' with parameters {params}")

        runfunc(*args, **kwargs)

    return wrapper


# def overload(func: Callable, /, _function_cache={}) -> Callable:
#
#     key = (func, tuple(func.__annotations__.values()))
#
#     if key in _function_cache:
#         raise KeyError(f"Identical overloaded signature for {func.__name__} already exists")
#
#     _function_cache[key] = func
#
#     def wrapper(*args, _function=func, **kwargs):
#         key = (_function.__name__, args + tuple(type(arg) for arg in _function.__annotations__.values()))
#         _function_cache[key](*args, **kwargs)
#
#     print(test := func.__annotations__)
#     print(test2 := func.__name__)
#
#     return wrapper


class Test:

    @overload
    def test(self, a: int):
        print("Running method with int")

    @overload
    def test(self, b: str):
        print("Running method with string")


temp = Test()
temp.test(3)
temp.test('3')


@overload
def overload_test(a: int, b=''):
    print('running with int')


@overload
def overload_test(a: str):
    print('running with string')


@overload
def another_function(a: str):
    print('running another function with string')


if __name__ == '__main__':
    overload_test('hej')
    another_function('')