""" This module demonstrates a decorator which adds support for traditional function/method overloading in Python. """

import time
from typing import Callable, Any, Union, get_args
import inspect


def overload(func: Callable, /, _function_cache={}) -> Callable:
    """
    Decorator which adds support for traditional function overloading.
    :param func: Function which should be overloadable.
    """

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

        try:  # Attempt to find and run an exact match for the overload.
            return _function_cache[func.__qualname__][params](*args, **kwargs)
        except KeyError:  # Search for an acceptable signature when a exact match can't be found.
            #  This might sound like a bad idea, but one has to consider the fact that Python supports optional
            #  arguments. These mean that the provided arguments needn't match the signature.

            for signature, function in _function_cache[func.__qualname__].items():

                # Signatures with fewer parameters than passed arguments are discarded.
                if len(params) > len(signature):  # TODO Kevin: How will this work with **kwargs?
                    continue  # Check the signature of the next function.

                # Iterate over the signature and arguments simultaneously to check that their types are compatible
                for param1, param2 in zip(signature, params):
                    # Ignore the type of the argument, if the parameter accepts any type.
                    # Otherwise; check that they match. If they don't, the parameter may be a Union,
                    # in which case we check if it contains the type of the argument.
                    if not (param1 is Any or (param1 is param2 or param2 in get_args(param1))):
                        break  # Break and check the signature of the next function.
                else:  # Will run when the loop finished without hitting break; meaning we found a compatible signature.
                    return function(*args, **kwargs)

            # Inform the user when this fails.
            raise KeyError(f"Cannot find a matching overload for function '{func.__qualname__}' with parameters {params}")

    return wrapper


@overload
def uniontest(*args):
    pass


if __name__ == '__main__':

    #test = tuple(inspect.signature(uniontest).parameters.values())

    before = time.time()

    for _ in range(1000000):
        uniontest(3.3, 'a', 3)

    print(f"Took: {time.time() - before}")
