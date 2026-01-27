#!/usr/bin/python3

try:
    import argparse
    from src.misc import printerr
    import json
    from ..llm_sdk import Small_LLM_Model
except Exception as e:
    print(f"Could not import a module: {e}")
    print('Have you tried installing the env with "make install"?')
    exit(1)


def load_json(json_file_path: str) -> list:
    """ Loads the given json file as a list object """
    try:
        with open(json_file_path, 'r') as input_file:
            loaded_json = json.load(input_file)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'Your input file was not found. {e}')
    except Exception as e:
        raise Exception(e)
    return loaded_json


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
    for prompt in json_data:
        print(prompt)

    # ? ===== Calling LLM ======

    return None


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        printerr(f'Caught an error: {e}')
