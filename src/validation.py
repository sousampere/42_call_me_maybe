#!/usr/bin/python3

from llm_sdk import Small_LLM_Model
from src.misc import printblue, printerr, load_json
from .llm_utils import translate_token_from_int, tensor_to_list, generate_next_word, get_highest_str_token_from_logits, set_null_highest_token

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

# "{"prompt":"<prompt>","fn_name":"fn_add_numbers","args": {"a": 2.0, "b": 3.0}}"


def get_available_functions() -> list[str]:
    json_data = load_json('data/input/functions_definition.json')
    functions = list(map(lambda ft: ft['fn_name'], json_data))
    return functions


def get_function_data(function_name: str) -> dict:
    json_data = load_json('data/input/functions_definition.json')
    ft = list(filter(lambda ft: ft['fn_name'] == function_name, json_data))
    print(ft[0])
    return ft[0]

def check_generated(output: str) -> bool:
    """ Verify if the current output is as expected """
    # ? The output (12 first chars) needs to start with {"prompt":"
    print(f'Check_generated original: {output}')
    if not 'fn_add_numbers'.startswith(output[:14]):
        # Doesn't match. Returning False
        printerr('Didn\'t pass the prompt check (1)')
        printerr(output[:14])
        printerr('fn_add_numbers')
        return False
    return True

def generate_int(instructions: str, llm: Small_LLM_Model):
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while logits.index(max(logits)) != 151645:
        print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        for character in current_token:
            valid_token = True
            # If the generated tokens are not ints, or the first token is not a - for a negative number
            if character not in '1234567890' and (output == '' and current_token != '-'):
                valid_token = False
        if valid_token:
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
        else:
            logits = set_null_highest_token(logits)
    printblue(output)



    # ? Compare with '",fn_name":"'

    # ? For each next generated token
    # ? Compare it with every functions
    # ? If one of the function starts with the tokens, True

    # ? 
    
    return True


