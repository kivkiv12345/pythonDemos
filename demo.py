import sys


class ExampleCls1:

    def __init__(self, **kwargs) -> None:
        super().__init__()

        for field, value in kwargs.items():
            setattr(self, field, value)


def main():

    input('Press enter to continue...')

    # Walrus operator | command line arguments.
    print(arguments := sys.argv[1:])

    input('Press enter to continue...')

    for arg in arguments:
        print(arg*2)

    input('Press enter to continue...')

    # Dictionary comprehension | Power of | enumerate.
    dictcomp = {arg: i**i for i, arg in enumerate(arguments)}

    input('Press enter to continue...')

    # Running code with import.
    import super_cool_module

    input('Press enter to continue...')

    # Unpacking dictionaries | Programmatically setting attributes of a class.
    exampleinstance = ExampleCls1(**dictcomp)

    input('Press enter to continue...')

    # Programmatically creating a class
    ExampleCls2 = type('ExampleCls2', (ExampleCls1,), dictcomp)

    input('Press enter to continue...')

    # Range | Instantiating programmatic class.
    for i in range(5):
        exampleinstance2 = ExampleCls2(testattribute=i)

    input('Press enter to continue...')


if __name__ == '__main__':
    main()
