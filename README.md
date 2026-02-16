*This project has been created as part of the 42 curriculum by gtourdia.*

# Description

Call_Me_Maybe is a project part of the 42 curriculum that aims to learn to generate content using text-based generative AI, also known as LLM (Large Language Model).

Given a certaing JSON file containing prompts and another file containing function definitions :
```
[
  {
    "prompt": "What is the square root of 16?"
  },
  ...
]
```
and
```
[
  {
    "fn_name": "fn_add_numbers",
    "args_names": [
      "a",
      "b"
    ],
    "args_types": {
      "a": "float",
      "b": "float"
    },
    "return_type": "float"
  },
  ...
]
```

We are expected to output a JSON file containing for each prompt its original prompt, the function choosen by the LLM to resolve the prompt, and the arguments given for this function :
```
[
  {
  "prompt": "What is the sum of 2 and 3?",
  "fn_name": "fn_add_numbers",
  "args": {"a": 2.0, "b": 3.0}
  },
  ...
]
```
This output file needs to be 100% valid JSON. Since we are working on a very small LLM, its output doesn't absolutely have to be valid, as long as it is mostly choosing the good functions. To get better results, we would have to use a better model.
To make the LLM output an available function every time, we are expected to use *constained decoding*, which is the concept of selecting the highest probability token generated, checking if it matches our expectations (a function name, arg type, etc.) and add its decoded value to our current text output.

# Given instructions

**[ Makefile & Execution ]**

The project uses uv for dependency management and a Makefile to automate core tasks.

-  `make install`: Install all project dependencies using `uv`, `pip`, or your preferred package manager.

-  `make run`: Execute the main function calling script.

-  `make debug`: Run the script using the built-in Python debugger (`pdb`) for troubleshooting.

-  `make lint`: Run code quality checks using `flake8` and `mypy` to ensure compliance with project standards.

-  `make lint-strict`: Run enhanced static analysis using `mypy --strict`.

-  `make clean`: Remove temporary files and caches, such as `__pycache__` and `mypy_cache`.


# Resources

- My knowledge since I've worked with LLM's before
- [Qwenn control tokens & chat template](https://qwen.readthedocs.io/en/latest/getting_started/concepts.html)
- Google Gemini was used for questions related to understanding constained decoding

# Algorithms explanation

The algorithm is quite simple:
A parsing is done on the JSON inputs using the built-in python module `json`. With this, we created a base prompt containing the functions list using a JSON format since LLMs work well with JSON understanding. Constained decoding was first applied to the function generation to generate the function name, then the args of this function were generated one-by-one using many specialized functions (one function for all data types of arg: bool, str, float and int).
The script then saves the result for each prompt in a list, that is outputted in the JSON output file, using `json.dump`.

# Performace analysis

Since this project uses Qwenn, I managed to reach very good result for simple function (that expect int/floats in input), but the nature of the LLM makes it unpredictable in generating good output for strings generation. The output quality depends on the difficulty of understanding the function.
For instance, the LLM will easily find the arguments for `"What is the sum of 1 and 3?"`, but will struggle a lot on questions like `"Replace every 'i' in 'I want an icecream' with the name of the current president of France"`.
This could have beed supervised if we had predictable function in input, but since the evaluator can make up any function he want, we cannot easily solve this problem, unless we use another more powerful LLM.

# Challenges faced
# Testing strategy
# Example usage


**[ OVERVIEW ]**

You can compile the bonus part using "make bonus". It generates a checker that behaves like the one given in the subject.

Give numbers as parameters to the checker, and send instructions to it using the standard input.

Example : `./push_swap 5 6 8 9 4 | ./checker 5 6 8 9 4`.

**[ RETURN VALUES ]**

- **OK** if the stack A is successfully sorted and the stack B is empty
- **KO** if the stack A is not sorted, or if the stack B is not empty
- **Error** if an invalid argument is given (as a parameter, or from the standard input)

## Authors

- [@sousampere](https://github.com/sousampere) - 42 login : **gtourdia** -> _parsing, bench, complex & medium algorithms, push & reverse_rotate moves_
- [@kletsol](https://github.com/kletsol) - 42 login : **lbonnet** -> _makefile, readme, swap & rotate moves, simple and medium algorithm._
- The rest of the work was done by the two of us.


## 🚀 About Me
I am a student at the 42 Mulhouse school. Most of my public projects will be from this school, while I will keep private most of my other projects.
## Contact me !

 - [LinkedIn](https://fr.linkedin.com/in/gaspardtourdiat)
 - [My website](https://gaspardtourdiat.fr/)
 - [For 42 students (my intra profile)](https://profile.intra.42.fr/users/gtourdia)


![Logo](https://assets.km0.omerloclients.com/community/cfbe5a0b-7637-43a0-94f9-7df2fc288c1d.jpg)
