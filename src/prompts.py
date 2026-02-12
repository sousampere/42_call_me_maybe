#!/usr/bin/python3

from typing import Any


def get_function_instructions(
        available_functions: list[Any],
        user_prompt: str) -> str:
    instructions = '''<|im_start|>system
{"available_functions": ''' + str(available_functions) + ''',\
"goal": "Select the correct function to execute the user's prompt"}<|im_end|>
<|im_start|>user
''' + user_prompt + '''<|im_end|>
<|im_start|>assistant
'''
    return instructions


def get_args_instructions(
        function_data: list[Any],
        user_prompt: str) -> str:
    output = '<|im_start|>system {"goal": "Select '\
    'the arguments for the following function,'\
    'according to the user\'s prompt, followed by a \n character."}'\
    f' {str(function_data)} ''{"particularity": "For negative '\
    'numbers, include a - character at the start"}<|im_end|>'\
    f'<|im_start|>user {user_prompt} <|im_end|>'\
    '<|im_start|>assistant\n'
    return output
