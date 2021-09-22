from decimal import Decimal
from enum import Enum
from typing import Union


class PrintColor(Enum):
    PINK = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def cprint(color: PrintColor, *args):
    print(f'{color.value}', *args, PrintColor.ENDC.value, sep='')


def print_func_with_kwargs(func):
    def wrapper(*args, **kwargs):
        cprint(PrintColor.PINK, f'Executing {func.__name__}')
        for k, v in kwargs.items():
            cprint(PrintColor.CYAN, f'    {k} = {v}')
        print()
        return func(*args, **kwargs)

    return wrapper


def printable_float(number: Union[Decimal, float]) -> str:
    return '{0:.10f}'.format(number)
