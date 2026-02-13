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
    from .prompts import get_function_instructions, get_args_instructions
    from .constants import Colors
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
    # List containing the generated data (will be exported as json)
    final_json = []


    args = get_parsed_args() # Loading args


    # Loading json input (prompts)
    try:
        prompts = load_json(args['input'])
        if (args['verbose']):
            print(f'{Colors.GREEN}✅ Loaded input file (prompts){Colors.END}')
    except FileNotFoundError:
        raise FileNotFoundError('Your prompt (input) file was not ' +
                                f'found ({args['input']})')
    except Exception:
        raise Exception(f'There was an error while loading '
                        f'{args['input']}. Please provide'
                        ' a non-corrupted file.')


    # Loading json containing function definitions
    try:
        available_functions = list(map(lambda ft: ft['fn_name'],
                                       load_json(args['functions_definitions'])))
        if (args['verbose']):
            print(f'{Colors.GREEN}✅ Loaded function definitions{Colors.END}')
    except FileNotFoundError:
        raise FileNotFoundError('Your functions_definitions file was not '
                                f'found ({args['functions_definitions']})')
    except Exception:
        raise Exception(f'There was an error while loading '
                        f'{args['functions_definitions']}. '
                        'Please provide a non-corrupted file.')


    # Printing status if --verbose is activated
    if (args['verbose']):
        print(f'\n{Colors.YELLOW}===== Verbose ON ======')
        print(f'Available functions: {available_functions}')
        print(f'Input path: {args['input']}')
        print(f'Output path: {args['output']}')
        print(f'{Colors.END}')


    llm = Small_LLM_Model() # Loading LLM


    if (args['verbose']):
        print(f'{Colors.BOLD}=== 💭​ PROCESSING START ==={Colors.END}')


    # Start processing all prompts
    for prompt in prompts:

        # Generating instructions for the LLM to process
        try:
            user_prompt = prompt['prompt']
            if (args['verbose']):
                print(f'\n\n\n=== 💭​ Processing prompt "{user_prompt}"==={Colors.END}')
        except Exception:
            raise Exception('Corrupted json. Please check your json')
        instructions = get_function_instructions(available_functions, user_prompt)


        # Creating the base of the output for the current prompt
        llm_result = {
            'prompt': user_prompt
        }


        # Generating the function using constained decoding
        output = generate_function(available_functions,
                                   instructions, prompt, llm, args)
        llm_result['fn_name'] = output
        # Printing status if --verbose is activated
        if args['verbose']:
            printgreen(f'✅ Function found: {output}\033[K')
        function_data = get_function_data(output,
                                          args['functions_definitions'])


        # Generating the arguments for the function found
        instructions = get_args_instructions(function_data, user_prompt)
        llm_result['args'] = generate_args(args, function_data,
                                           instructions, llm)
        # if args['verbose']:
        #     print(f'{Colors.LIGHT_GRAY}✅ Args found: {llm_result['args']}\033[K', end='\r')


        # Appends the prompt's output to the
        # list that will be exported as json
        final_json.append(llm_result)
        # Printing status if --verbose is activated


    # Save the output in the chosen destination file
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
