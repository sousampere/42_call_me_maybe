#!/usr/bin/python3

try:
    import argparse
    from src.constants import Colors
    from src.misc import printerr
    import json
except Exception as e:
    print(f"Could not import a module: {e}")
    print('Have you tried installing the env with "make install"?')
    exit()


def main() -> None:
    # ? ===== Parsing =====
    parser = argparse.ArgumentParser(description="gtourdia's call_me_maybe project.")
    parser.add_argument(
        # Input arg
        "--input",
        required=True,
        help="input file path containing the prompts to test",
        default='data/input/function_calling_tests.json'
    )
    parser.add_argument(
        # Output arg
        "--output",
        required=True,
        help="output file path",
        default='data/output/function_calling_result.json'
    )
    args = parser.parse_args()

    # ? ===== Opening input file ======
    try:
        with open(args.input, 'r') as input_file:
            json_input = json.load(input_file)
            print(json_input)
    except FileNotFoundError as e:
        raise FileNotFoundError(f'Your input file was not found. {e}')
    except Exception as e:
        raise Exception(e)
    return None


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        printerr(f'Caught an error: {e}')
