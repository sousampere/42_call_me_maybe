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

AND

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

# Given instructions

**[ Makefile & Execution ]**

The project uses uv for dependency management and a Makefile to automate core tasks.

-  `make install`: Install all project dependencies using `uv`, `pip`, or your preferred package manager.

-  `make run`: Execute the main function calling script.

-  `make debug`: Run the script using the built-in Python debugger (`pdb`) for troubleshooting.

-  `make lint`: Run code quality checks using `flake8` and `mypy` to ensure compliance with project standards.

-  `make lint-strict`: Run enhanced static analysis using `mypy --strict`.

-  `make clean`: Remove temporary files and caches, such as `__pycache__` and `mypy_cache`.

**[ EXECUTION ]**



**[ ERRORS ]**



# Resources



# Algorithms choices



**[ SIMPLE ]**

For simple complexity, we choosed a rather easy "minimum extraction method".

- The algorithm processes the whole stack "a", looking for the smallest integer, and pushes it in stack
		"b".

-  It then searches for the next smallest integer in what's remaining in stack "a", rotating or reverse rotating depending on what is the most efficient method to get to it in a minimal number of rotations.

-  It pushes it to "b" so it's placed above the previous one.

-  Once stack "a" is empty, all integers are sorted in "b" in descending order.

-  The algorithm then pushes back all "b" in "a", one interger at a time.

-  Result : "a" is correctly sorted in ascending order, from top to bottom, and "b" is empty.

We chose this solution because, after trying multiple other sorting methods like bubble sort and insertion sort, it appeared it was the most efficient and optimizable one to reach the subjects requirements, even if it requires a lot of utility functions. This algorithm was made by lbonnet.

**[ MEDIUM ]**

The chosen medium algorithm is the chunk sort algorithm.

How it works :

-  We create √n (times 1.72 to get a better result) chunks of numbers (n being the number of integers in the stack).

-  Each number being in the range of the first √n numbers is sent to the stack "b".

-  We repeat this step for each chunk, one by one.

-  At the end, the integers are all sent back to the stack "a", and then sorted using a stable algorithm (the simple one).

We chose it because it was the easier to implement when being restricted by the push_swap moves.
The algorithm was build by lbonnet and gtourdia simultaneously, until gtourdia managed to succeed in its implementation first.

**[ COMPLEX ]**

The chosen complex algorithm (with a complexity of O(n log n)) is the binary radix sort.

How it works :

-  The Radix LSB sort (Least significant bit) is checking the least significant bit of a number.

-  If the bit is 0, it pushes the number to the stack "b", else it keeps it in "a" and check the next number until the whole stack "a" is analysed.

-  All numbers in the stack "b" are then sent back to the original stack "a"

-  The algorithm then checks the next least significant bit and does the same

-  We repeat these steps until the whole stack is sorted.

-  To make this even faster, we don't check the actual value, but rather the rank of this value in the sorted stack (example : if the stack is 1664, 42, 1337, 5, the ranks are 4, 2, 3, 1).

We chose this algorithm due to its interesting sorting strategy, and because it was aligned with the project's requirements. This algorithm was made by gtourdia.

# Bonus

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
