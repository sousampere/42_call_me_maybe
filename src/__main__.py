#!/usr/bin/python3


try:
    import argparse
    from src.misc import printerr, load_json, printblue
    from llm_sdk import Small_LLM_Model
    from .llm_utils import translate_token_from_int, tensor_to_list, generate_next_word, get_highest_str_token_from_logits, set_null_highest_token
    from .validation import check_generated, get_available_functions, get_function_data, generate_int, generate_float, generate_bool, generate_str
    import json
    import math
except Exception as e:
    print(f"Could not import a module: {e}")
    print('Have you tried installing the env with "make install"?')
    exit(1)


def get_parsed_args() -> dict[str, str]:
    """ Initialize argparse settings and returns input and output args """
    parser = argparse.ArgumentParser(
        description="gtourdia's call_me_maybe project (from school 42). "
        "Usage : uv run python -m src [--input <input_file>] [--output <output_file>]"
    )
    parser.add_argument(
        # Input arg
        "--input",
        required=True,
        help="input file path -> containing the prompts to test",
        default='data/input/function_calling_tests.json'
    )
    parser.add_argument(
        # Output arg
        "--output",
        required=True,
        help="output file path -> to store llm's results",
        default='data/output/function_calling_result.json'
    )
    args = parser.parse_args()
    arguments_dict = {'input': args.input, 'output': args.output}
    return arguments_dict


def main() -> None:
    """
    Main function
    - Getting input/output files (from args)
    - Open input file
    """    
    # ? ===== Parsing =====
    args = get_parsed_args()

    # ? ===== Opening input file ======
    json_data = load_json(args['input'])
    # for prompt in json_data:
        # print(prompt['prompt'])

    json_data_ft = load_json('data/input/functions_definition.json')
    # for ft in json_data_ft:
        # print(ft)
    avaiable_functions = list(map(lambda ft: ft['fn_name'], json_data_ft))
    print(avaiable_functions)

    # ? ===== Prompt ======
    user_prompt = 'Substitute the string "Hello world", by replacing "Hello" by "Goodbye".'
    instructions = '''<|im_start|>system
{"available_functions": ''' + str(avaiable_functions) + ''',\
"goal": "Select the correct function to execute the user's prompt"}<|im_end|>
<|im_start|>user
''' + user_prompt + '''<|im_end|>
<|im_start|>assistant
'''
    output = 'fn_'
    printblue(instructions + output)
    # ? ===== Preparing result =====
    llm_result = {
        'prompt': user_prompt
    }

    # ? ===== Loading LLM ======
    llm = Small_LLM_Model(device='mps')

    # ? ===== Tokenization ======
    # Encoding the tokens
    encoded_text = llm._encode(instructions + output)
    encoded_text = tensor_to_list(encoded_text)

    # ? ===== Calculating logits ======
    logits = llm.get_logits_from_input_ids(encoded_text)
    wordlist = llm.get_path_to_vocabulary_json()
    print(wordlist)

    # ? ===== Generate valid token, one by one ======
    while (output not in avaiable_functions):
        print(output)

        ft_list = []
        for function in avaiable_functions:
            if function.startswith(output):
                ft_list.append(function)
        if len(ft_list) == 1:
            output = ft_list[0]
            break
        try:
            # Getting highest token
            current_token = get_highest_str_token_from_logits(logits, wordlist)
            print(output+current_token)
            valid_token = False
            for function in avaiable_functions:
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
    llm_result['fn_name'] = output
    llm_result['args'] = {}

    # ? ===== Getting function args ======
    function_data = get_function_data(output)
    instructions = '''<|im_start|>system
{"goal": "Select the arguments for the following function, according to the user's prompt, followed by a \n character."},\
''' + str(function_data) + '''
{"particularity": "For negative numbers, include a - character at the start"}<|im_end|>
<|im_start|>user
''' + user_prompt + '''<|im_end|>
<|im_start|>assistant
'''
    # exit()
    for arg in function_data['args_names']:
        print(arg)
        instructions = instructions + f'{arg}='
        if function_data['args_types'][arg] == 'int':
            print(f"{arg} is an int")
            value = generate_int(instructions, llm)
            llm_result['args'][arg] = value
            instructions += str(value) + '\n'
        if function_data['args_types'][arg] == 'float':
            print(f"{arg} is a float")
            value = generate_float(instructions, llm)
            llm_result['args'][arg] = value
            instructions += str(value) + '\n'
        if function_data['args_types'][arg] == 'bool':
            print(f"{arg} is a bool")
            value = generate_bool(instructions, llm)
            llm_result['args'][arg] = value
            instructions += str(value) + '\n'
        if function_data['args_types'][arg] == 'str':
            print(f"{arg} is a str")
            value = generate_str(instructions, llm)
            llm_result['args'][arg] = value
            instructions += str(value) + '\n'
    print(llm_result)
    return None


if __name__ == "__main__":
    # try:
    #     main()
    # except Exception as e:
    #     printerr(f'Caught an error: {e}')
    main()