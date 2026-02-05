#!/usr/bin/python3

try:
    from src.constants import Colors
    import sys
    import json
    from typing import Any
except Exception as e:
    print('Import error:', e)


def printerr(*args: Any) -> None:
    """Prints a red message"""
    sys.stderr.write(f"{Colors.RED}")
    sys.stderr.write(*args)
    sys.stderr.write(f'{Colors.END}\n')


def printblue(*args: Any) -> None:
    """Print a blue message"""
    sys.stdout.write(f"{Colors.BLUE}")
    sys.stdout.write(*args)
    sys.stdout.write(f'{Colors.END}\n')


def printgreen(*args: Any) -> None:
    """Print a blue message"""
    sys.stdout.write(f"{Colors.GREEN}")
    sys.stdout.write(*args)
    sys.stdout.write(f'{Colors.END}\n')


def printyellow(*args: Any) -> None:
    """Print a blue message"""
    sys.stdout.write(f"{Colors.YELLOW}")
    sys.stdout.write(*args)
    sys.stdout.write(f'{Colors.END}\n')


def load_json(json_file_path: str) -> Any:
    """Loads the given json file as a list object

    Args:
        json_file_path (str): Json file to load

    Raises:
        FileNotFoundError: Not found
        Exception: Any other exception

    Returns:
        Any: json data as a python list
    """
    try:
        with open(json_file_path, 'r') as input_file:
            loaded_json = json.load(input_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'The file was not found. {e}')
    except Exception as e:
        raise Exception(e)
    return loaded_json


if __name__ == '__main__':
    pass
