#!/usr/bin/python3

from src.misc import printerr

# try:

# except Exception as e:
#     printerr("validation.py:", e)


# [
#     {
#         "prompt": "What is the sum of 2 and 3?",
#         "fn_name": "fn_add_numbers",
#         "args": {"a": 2.0, "b": 3.0}
#     },
#     {
#         "prompt": "Reverse the string 'hello'",
#         "fn_name": "fn_reverse_string",
#         "args": {"s": "hello"}
#     }
# ]

def check_generated(output: str) -> bool:
    if not (output.startswith('{"prompt": "')):
        return False

