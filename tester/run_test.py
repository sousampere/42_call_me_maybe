#!/usr/bin/python3

import json
import subprocess
import os
import pytest

FILES = [
        'tester/ft1.json',
        'tester/ft2.json',
        'tester/ft3.json',
        'tester/ft4.json',
        'tester/ft5.json',
        'tester/ft6.json'
    ]

@pytest.mark.parametrize("file", FILES)
def test_file_generation(file):
    # Remove json file
    output = 'tester/result.json'
    if os.path.exists(output):
        os.remove(output)

    # Run process and create the output json
    result = subprocess.run(
        ['uv', 'run', 'python3.14',
         '-m', 'src',
         '--input', file,
         '--output', output,
         '--functions_definition', 'tester/functions_definition.json'])

    # Try to load the json
    try:
        with open(output, 'r') as f:
            json.load(f)
        data_ok = True
    except Exception:
        data_ok = False

    # If everything is OK, test is passed ✅
    assert result.returncode == 0 and os.path.exists(output) and data_ok

def main():
    for file in FILES:
        test_file_generation(file)

if __name__ == '__main__':
    print('This program must be run in a folder next to the src folder.')
    main()
