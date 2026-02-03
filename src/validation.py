#!/usr/bin/python3

try:
    from typing import Any
    from llm_sdk import Small_LLM_Model
    from src.misc import load_json
    from .llm_utils import tensor_to_list, \
        get_highest_str_token_from_logits, \
        set_null_highest_token
except Exception as e:
    print(f"Could not import something: {e}")


def get_available_functions() -> list[str]:
    """Return a list of the available functions"""
    json_data = load_json('data/input/functions_definition.json')
    functions = list(map(lambda ft: ft['fn_name'], json_data))
    if len(functions) == 0:
        raise Exception('The given function list is empty')
    return functions


def get_function_data(function_name: str) -> Any:
    """Returns the data of a given function name (data picked in fixed path)"""
    json_data = load_json('data/input/functions_definition.json')
    ft = list(filter(lambda ft: ft['fn_name'] == function_name, json_data))
    return ft[0]


def generate_int(instructions: str, llm: Small_LLM_Model) -> int:
    """ Generates an int from the given instrucitons """
    output = ''
    # Encoding string data into logits
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    # printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while current_token != 'Ċ':
        # print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        # print(f"Generated token -> {current_token}|")
        for character in current_token:
            valid_token = True
            # If the generated tokens are not ints, or the first
            # token is not a - for a negative number
            if character not in '1234567890':
                valid_token = False
            if output == '' and (current_token == '-' or
                                 current_token == 'Ġ-'):
                valid_token = True
                current_token = '-'
        if valid_token:
            # print(f"token '{current_token}' is valid, output "
            #   f"-> '{output + current_token}'")
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
            # print(f'Max next logit -> {logits.index(max(logits))}')
        else:
            logits = set_null_highest_token(logits)
    # printblue(output)
    return int(output)


def generate_float(instructions: str, llm: Small_LLM_Model) -> float:
    """ Generates a float from the given instrucitons """
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    # print(wordlist)
    # printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while current_token != 'Ċ':
        # print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        # print(f"Generated token -> {current_token}|")
        for character in current_token:
            valid_token = True
            # If the generated tokens are not ints,
            # or the first token is not a - for a negative number
            if character not in '1234567890.':
                valid_token = False
            if output == '' and (current_token == '-' or
                                 current_token == 'Ġ-'):
                valid_token = True
                current_token = '-'
        # Calculating number of '.' character
        dots = 0
        for char in output + current_token:
            if char == '.':
                dots += 1
        if valid_token and dots <= 1:
            # print(f"token '{current_token}' is valid,"
            #       f" output -> '{output + current_token}'")
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
            # print(f'Max next logit -> {logits.index(max(logits))}')
        else:
            logits = set_null_highest_token(logits)
    # printblue(output)
    return float(output)


def generate_bool(instructions: str, llm: Small_LLM_Model) -> bool:
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    # print(wordlist)
    # printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while output != 'true' or output != 'false':
        # print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        # print(f"Generated token -> {current_token}|")
        if ('true'.startswith(output + current_token)
                and len(output + current_token) <= 4):
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
        elif ('false'.startswith(output + current_token)
              and len(output + current_token) <= 5):
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
        else:
            logits = set_null_highest_token(logits)
    # printblue(output)
    return True if output == 'true' else False


def generate_str(instructions: str, llm: Small_LLM_Model) -> str:
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    # print(wordlist)
    # printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while current_token != 'Ċ':
        # print(output)
        # Validating generated token for an int
        current_token = get_highest_str_token_from_logits(logits, wordlist)
        # print(f"Generated token -> {current_token}|")
        # print(f"token '{current_token}' is valid, output -> '{output +
        #   current_token}'")
        if current_token != 'Ċ':
            output = output + current_token
            encoded_text = llm._encode(instructions + output)
            encoded_text = tensor_to_list(encoded_text)
            logits = llm.get_logits_from_input_ids(encoded_text)
            # print(f'Max next logit -> {logits.index(max(logits))}')
        else:
            break
    # printblue(output)
    return output
