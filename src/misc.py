#!/usr/bin/python3

from src.constants import Colors


def printerr(*args) -> None:
    """ Print a red message """
    print(f"{Colors.RED}", end='')
    print(*args, end=f'{Colors.END}\n')



if __name__ == '__main__':
    pass
