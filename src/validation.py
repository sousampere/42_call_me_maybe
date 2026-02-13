#!/usr/bin/python3


try:
    from typing import Any
    from llm_sdk import Small_LLM_Model
    from src.misc import load_json, printblue, printgreen, printyellow
    from .llm_utils import tensor_to_list, \
        get_highest_str_token_from_logits, \
        set_null_highest_token
    from .constants import Colors
except Exception as e:
    print(f"Could not import something: {e}")


def get_available_functions() -> list[str]:
    """Return a list of the available functions

    Raises:
        Exception: No functions

    Returns:
        list[str]: available function (list)
    """
    json_data = load_json('data/input/functions_definition.json')
    functions = list(map(lambda ft: ft['fn_name'], json_data))
    if len(functions) == 0:
        raise Exception('The given function list is empty')
    return functions


def get_function_data(function_name: str, path: str) -> Any:
    """Returns the data of a given function name

    Args:
        function_name (str)
        path (str): path to the functions_definition

    Returns:
        Any: function data
    """
    json_data = load_json(path)
    ft = list(filter(lambda ft: ft['fn_name'] == function_name, json_data))
    if 'args_names' not in ft[0] or 'args_types' not in ft[0]:
        raise Exception('Invalid json: missing args_names or args_types\
 (in functions_definitions)')
    for arg in ft[0]['args_names']:
        if arg not in ft[0]['args_types'].keys():
            raise Exception(f'Invalid json: missing args_type\
 (for {ft[0]['fn_name']} -> arg "{arg}")')
    return ft[0]


def generate_int(instructions: str, llm: Small_LLM_Model) -> int:
    """Generates an int from the given instrucitons

    Args:
        instructions (str): instructions prompt
        llm (Small_LLM_Model): loaded llm

    Returns:
        int: int value
    """
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
    """Generates a float from the given instrucitons

    Args:
        instructions (str): instructions prompt
        llm (Small_LLM_Model): loaded llm

    Returns:
        float: float value
    """
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
    """Generates a bool from the given instrucitons

    Args:
        instructions (str): instructions prompt
        llm (Small_LLM_Model): loaded llm

    Returns:
        bool value
    """
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
    """Generates a str from the given instrucitons

    Args:
        instructions (str): instructions prompt
        llm (Small_LLM_Model): loaded llm

    Returns:
        str value
    """
    output = ''
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    # print(wordlist)
    # printblue(instructions + output)
    current_token = get_highest_str_token_from_logits(logits, wordlist)
    while current_token != 'Ċ' and len(output) < 1000:
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


def generate_function(available_functions: list[str],
                      instructions: str,
                      prompt: str,
                      llm: Small_LLM_Model,
                      args: dict[str, str]) -> str:
    """Generate a function from the given prompt using the llm

    Args:
        available_functions (list[str]): list of functions
        instructions (str): instruction prompt
        prompt (str): user's prompt
        llm (Small_LLM_Model): loaded llm
        args (dict[str, str]): args of the program

    Returns:
        str: function string
    """
    output = 'fn_'
    # if args['verbose']:
    #     printblue(f'Prompt => {instructions + output}')
    # ? ===== Tokenization ======
    # Encoding the tokens
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)

    # ? ===== Calculating logits ======
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()

    # ? ===== Generate valid token, one by one ======
    if args['verbose']:
        print(f'{Colors.LIGHT_GRAY}Calculating function for prompt: {prompt['prompt']}...', end='\r')
    while (output not in available_functions):
        ft_list = []
        for function in available_functions:
            if function.startswith(output):
                ft_list.append(function)
        if len(ft_list) == 1:
            output = ft_list[0]
            break
        try:
            # Getting highest token
            current_token = get_highest_str_token_from_logits(
                logits,
                wordlist)
            print(f'{Colors.LIGHT_GRAY}Calculating function for prompt: {prompt['prompt']}... fn_{current_token}\033[K', end='\r')
            valid_token = False
            for function in available_functions:
                if function.startswith(output + current_token):
                    # Generated token is valid
                    output = output + current_token
                    # Recalculating new logits
                    encoded_text = llm._encode(instructions + output)
                    encoded_text = tensor_to_list(encoded_text)
                    logits = llm.get_logits_from_input_ids(encoded_text)
                    valid_token = True
                    break
            if not valid_token:
                # Skipping this token
                logits = set_null_highest_token(logits)
        except Exception as e:
            print(e)
            logits = set_null_highest_token(logits)
    return output


def generate_args(args: dict[str, str], function_data: dict[str, Any],
                  instructions: str,
                  llm: Small_LLM_Model) -> Any:
    """Generate arguments for the given function using the llm

    Args:
        args (dict[str, str]): Program args
        function_data (dict[str, Any]): function data obtained
            from get_function_data
        instructions (str): instructions prompt
        llm (Small_LLM_Model): loaded llm

    Returns:
        dict[str, Any]: args for thr function
    """
    if args['verbose']:
        print(f'📝​ Getting the following args : {function_data['args_names']}')


    # Initializing the dict containing the args to return
    llm_args: dict[str, Any] = {'fn_args': {}}

    for arg in function_data['args_names']:
        if args['verbose']:
            print(f'{Colors.LIGHT_GRAY}Calculating arg: {arg}...', end='\r')
        instructions = instructions + f'{arg}='
        # Dispatch the generation to the correct generator
        if function_data['args_types'][arg] == 'int':
            # ? > For integers
            value_int = generate_int(instructions, llm)
            llm_args['fn_args'][arg] = value_int
            instructions += str(value_int) + '\n'
        if function_data['args_types'][arg] == 'float':
            # ? > For floats
            value_float = generate_float(instructions, llm)
            llm_args['fn_args'][arg] = value_float
            instructions += str(value_float) + '\n'
        if function_data['args_types'][arg] == 'bool':
            # ? > For bools
            value_bool = generate_bool(instructions, llm)
            llm_args['fn_args'][arg] = value_bool
            instructions += str(value_bool) + '\n'
        if function_data['args_types'][arg] == 'str':
            # ? > For strings
            value = generate_str(instructions, llm)
            value = value.replace('Ġ', ' ').replace('Ċ', '')
            llm_args['fn_args'][arg] = value
            instructions += str(value) + '\n'
        if args['verbose']:
            printgreen(f'🎯 Found arg {arg} -> '
                       f'{llm_args['fn_args'][arg]}\033[K')
    return llm_args['fn_args']
