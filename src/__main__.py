#!/usr/bin/python3


try:
    import argparse
    from src.misc import printerr, load_json, printblue, \
        printgreen, printyellow
    from llm_sdk import Small_LLM_Model
    from .llm_utils import tensor_to_list, \
        get_highest_str_token_from_logits, \
        set_null_highest_token
    from .validation import get_function_data, \
        generate_int, generate_float, \
        generate_bool, generate_str
    import json
    import os
except Exception as e:
    print(f"Could not import a module: {e}")
    print('Have you tried installing the env with "make install"?')
    exit(1)


def get_parsed_args() -> dict[str, str]:
    """Initialize argparse settings and returns input and output args"""
    parser = argparse.ArgumentParser(
        description="gtourdia's call_me_maybe project (from school 42). "
        "Usage : uv run python -m src [--input <input_file>] \
[--output <output_file>]"
    )
    parser.add_argument(
        # Input arg
        "--input",
        required=True,
        help="input file path -> containing the prompts to convert",
        default='data/input/function_calling_tests.json'
    )
    parser.add_argument(
        # Output arg
        "--output",
        required=True,
        help="output file path -> to store llm's results",
        default='data/output/function_calling_result.json'
    )
    parser.add_argument(
        # Output arg
        "--functions_definitions",
        required=False,
        help="path of the file containing the functions definitions",
        default='data/input/functions_definition.json'
    )
    parser.add_argument(
        # Output arg
        "--verbose",
        required=False,
        help="activates verbose (false/true)",
        default='false'
    )
    args = parser.parse_args()

    verbose = False
    if args.verbose == 'true':
        verbose = True

    arguments_dict = {
        'input': args.input,
        'output': args.output,
        'functions_definitions': args.functions_definitions,
        'verbose': verbose
        }
    return arguments_dict


def main() -> None:
    """Main program execution"""
    # ? ===== Loading LLM ======
    llm = Small_LLM_Model(device='mps')

    # ? ===== Parsing =====
    args = get_parsed_args()

    # ? ===== Opening input file ======
    prompts = load_json(args['input'])
    # Final json will be the content saved in the output path
    final_json = []
    json_data_ft = load_json(args['functions_definitions'])
    avaiable_functions = list(map(lambda ft: ft['fn_name'], json_data_ft))
    if (args['verbose']):
        print('===== Verbose ON ======')
        print(f'Available functions: {avaiable_functions}')
        print(f'Input path: {args['input']}')
        print(f'Output path: {args['output']}')
        print('')

    for prompt in prompts:
        # ? ===== Prompt ======
        user_prompt = prompt['prompt']
        instructions = '''<|im_start|>system
{"available_functions": ''' + str(avaiable_functions) + ''',\
"goal": "Select the correct function to execute the user's prompt"}<|im_end|>
<|im_start|>user
''' + user_prompt + '''<|im_end|>
<|im_start|>assistant
'''
        output = 'fn_'
        if args['verbose']:
            printblue('==================================================\n\n')
            printblue(f'Prompt => {instructions + output}')
        # ? ===== Preparing result =====
        llm_result = {
            'prompt': user_prompt
        }

        # ? ===== Tokenization ======
        # Encoding the tokens
        encoded_text = llm._encode(instructions + output)
        encoded_text = tensor_to_list(encoded_text)

        # ? ===== Calculating logits ======
        logits = llm.get_logits_from_input_ids(encoded_text)
        wordlist = llm.get_path_to_vocabulary_json()

        # ? ===== Generate valid token, one by one ======
        if args['verbose']:
            print(f'Calculating function for prompt: {prompt}')
        while (output not in avaiable_functions):
            ft_list = []
            for function in avaiable_functions:
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
        if args['verbose']:
            printgreen(f'✅ Function found: {output}')

        # ? ===== Getting function args ======
        function_data = get_function_data(output)
        instructions = '''<|im_start|>system
{"goal": "Select the arguments for the following function, \
according to the user's prompt, followed by a \n character."},\
''' + str(function_data) + '''
{"particularity": "For negative numbers, include\
 a - character at the start"}<|im_end|>
<|im_start|>user
''' + user_prompt + '''<|im_end|>
<|im_start|>assistant
'''
        if args['verbose']:
            print('')
            print(f'Args to get: {function_data['args_names']}')

        for arg in function_data['args_names']:
            if args['verbose']:
                print('')
                print(f'Getting arg "{arg}"...')
            instructions = instructions + f'{arg}='
            if function_data['args_types'][arg] == 'int':
                value_int = generate_int(instructions, llm)
                llm_result['args'][arg] = value_int
                instructions += str(value_int) + '\n'
            if function_data['args_types'][arg] == 'float':
                value_float = generate_float(instructions, llm)
                llm_result['args'][arg] = value_float
                instructions += str(value_float) + '\n'
            if function_data['args_types'][arg] == 'bool':
                value_bool = generate_bool(instructions, llm)
                llm_result['args'][arg] = value_bool
                instructions += str(value_bool) + '\n'
            if function_data['args_types'][arg] == 'str':
                value = generate_str(instructions, llm)
                value = value.replace('Ġ', ' ').replace('Ċ', '')
                llm_result['args'][arg] = value
                instructions += str(value) + '\n'
                if args['verbose']:
                    printgreen(f'🎯 Found arg {arg} -> '
                               f'{llm_result['args'][arg]}')
        final_json.append(llm_result)
        if args['verbose']:
            printyellow(f'Json for this prompt:\n{llm_result}')

    try:
        os.makedirs(os.path.dirname(args['output']))
    except Exception:
        pass
    with open(args['output'], 'w') as f:
        json.dump(final_json, f)
    return None


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        printerr(f'Caught an error: {e}')
