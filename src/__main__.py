#!/usr/bin/python3


try:
    import argparse
    from src.misc import printerr, load_json, \
        printgreen, printyellow
    from llm_sdk import Small_LLM_Model
    from .validation import get_function_data, \
        generate_function, generate_args
    import json
    import os
except Exception as e:
    print(f"Could not import a module: {e}")
    print('Have you tried installing the env with "make install"?')
    exit(1)


def get_parsed_args() -> dict[str, str]:
    """Get the arguments from the user's prompt

    Returns:
        dict[str, str]: Arguments (arg, value)
    """
    parser = argparse.ArgumentParser(
        description="gtourdia's call_me_maybe project (from school 42). "
        "Usage : uv run python -m src [--input <input_file>] \
[--output <output_file>]"
    )
    parser.add_argument(
        # Input arg
        "--input",
        required=False,
        help="input file path -> containing the prompts to convert",
        default='data/input/function_calling_tests.json'
    )
    parser.add_argument(
        # Output arg
        "--output",
        required=False,
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
    """Run the main process :
    - Loading LLM

    For each prompt in the provided input :
    - Creating prompt to get the function
    - Get the function
    - Create the prompt to get the args
    - Get the args

    - Save everything in output file as json
    """
    # ? ===== Loading LLM ======
    llm = Small_LLM_Model()

    # ? ===== Parsing =====
    args = get_parsed_args()

    # ? ===== Opening input file ======
    try:
        prompts = load_json(args['input'])
    except FileNotFoundError:
        raise FileNotFoundError('Your prompt (input) file was not ' +
                                f'found ({args['input']})')
    except Exception:
        raise Exception(f'There was an error while loading \
{args['input']}. Please provide a non-corrupted file.')
    # Final json will be the content saved in the output path
    final_json = []
    try:
        json_data_ft = load_json(args['functions_definitions'])
    except FileNotFoundError:
        raise FileNotFoundError('Your functions_definitions file was not ' +
                                f'found ({args['functions_definitions']})')
    except Exception:
        raise Exception(f'There was an error while loading \
{args['functions_definitions']}. Please provide a non-corrupted file.')
    available_functions = list(map(lambda ft: ft['fn_name'], json_data_ft))
    if (args['verbose']):
        print('===== Verbose ON ======')
        print(f'Available functions: {available_functions}')
        print(f'Input path: {args['input']}')
        print(f'Output path: {args['output']}')
        print('')

    # ! ===== Processing start ======
    for prompt in prompts:
        # ! ===== Generating function ======
        # ? ===== Prompt creation ======
        try:
            user_prompt = prompt['prompt']
        except Exception:
            raise Exception('Corrupted json. Please check your json')
        instructions = '''<|im_start|>system
{"available_functions": ''' + str(available_functions) + ''',\
"goal": "Select the correct function to execute the user's prompt"}<|im_end|>
<|im_start|>user
''' + user_prompt + '''<|im_end|>
<|im_start|>assistant
'''
        # ? ===== Preparing result =====
        llm_result = {
            'prompt': user_prompt
        }

        # ? ===== Generate function =====
        output = generate_function(available_functions,
                                   instructions, prompt, llm, args)
        llm_result['fn_name'] = output
        # llm_result['args'] = {}
        if args['verbose']:
            printgreen(f'✅ Function found: {output}')

        # ! ===== Generating arguments ======
        # ? ===== Getting function args ======
        function_data = get_function_data(output,
                                          args['functions_definitions'])
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
        llm_result['args'] = generate_args(args, function_data,
                                           instructions, llm)
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
        exit(0)
    except Exception as e:
        printerr(f'Caught an error: {e}')
        exit(1)
