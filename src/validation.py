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

def generate_int(instructions: str, llm: Small_LLM_Model) -> int:
    """ Generates an int from the given instrucitons """
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    print(wordlist)
    printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while current_token != 'Ċ':
        print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        print(f"Generated token -> {current_token}|")
        for character in current_token:
            valid_token = True
            # If the generated tokens are not ints, or the first token is not a - for a negative number
            if character not in '1234567890':
                valid_token = False
            if output == '' and (current_token == '-' or current_token == 'Ġ-'):
                valid_token = True
                current_token = '-'
        if valid_token:
            print(f"token '{current_token}' is valid, output -> '{output + current_token}'")
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
            print(f'Max next logit -> {logits.index(max(logits))}')
        else:
            logits = set_null_highest_token(logits)
    printblue(output)
    return int(output)


def generate_float(instructions: str, llm: Small_LLM_Model) -> float:
    """ Generates a float from the given instrucitons """
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    print(wordlist)
    printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while current_token != 'Ċ':
        print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        print(f"Generated token -> {current_token}|")
        for character in current_token:
            valid_token = True
            # If the generated tokens are not ints, or the first token is not a - for a negative number
            if character not in '1234567890.':
                valid_token = False
            if output == '' and (current_token == '-' or current_token == 'Ġ-'):
                valid_token = True
                current_token = '-'
        # Calculating number of '.' character
        dots = 0
        for char in output + current_token:
            if char == '.':
                dots += 1
        if valid_token and dots <= 1:
            print(f"token '{current_token}' is valid, output -> '{output + current_token}'")
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
            print(f'Max next logit -> {logits.index(max(logits))}')
        else:
            logits = set_null_highest_token(logits)
    printblue(output)
    return float(output)

def generate_bool(instructions: str, llm: Small_LLM_Model) -> bool:
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    print(wordlist)
    printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while output != 'true' or output != 'false':
        print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        print(f"Generated token -> {current_token}|")
        if ('true'.startswith(output + current_token) and len(output + current_token) <= 4):
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
        elif ('false'.startswith(output + current_token) and len(output + current_token) <= 5):
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
        else:
            logits = set_null_highest_token(logits)
    printblue(output)
    return True if output == 'true' else False

def generate_str(instructions: str, llm: Small_LLM_Model) -> str:
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    print(wordlist)
    printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while current_token != 'Ċ':
        print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        print(f"Generated token -> {current_token}|")
        print(f"token '{current_token}' is valid, output -> '{output + current_token}'")
        if current_token != 'Ċ':
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
            print(f'Max next logit -> {logits.index(max(logits))}')
        else:
            break
    printblue(output)
    return output



    # ? Compare with '",fn_name":"'

    # ? For each next generated token
    # ? Compare it with every functions
    # ? If one of the function starts with the tokens, True

    # ? 
    
    return True


