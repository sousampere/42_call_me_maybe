#!/usr/bin/python3

from src.constants import Colors
import sys


def printerr(*args) -> None:
    """ Print a red message """
    sys.stderr.write(f"{Colors.RED}")
    sys.stderr.write(*args)
    sys.stderr.write(f'{Colors.END}\n')
    # print(f"{Colors.RED}", end='')
    # print(*args, end=f'{Colors.END}\n')


if __name__ == '__main__':
    pass
