#!/usr/bin/python3

try:
    import argparse
except Exception as e:
    print(f'Could not import a module: {e}')
    print('Have you tried installing the env with "make install"?')


def main() -> None:
    # ===== Parsing =====
    parser = argparse.ArgumentParser(
        description="gtourdia's call_me_maybe project.")
    parser.add_argument('--input', required=True, help="input file path")
    parser.add_argument('--output', required=True, help="output file path")
    args = parser.parse_args()
    print('DEBUG: ARGS', args)

    return None


if __name__ == '__main__':
    main()
