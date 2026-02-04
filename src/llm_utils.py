#!/usr/bin/python3


try:
    import json
    from src.misc import printerr
    from llm_sdk import torch
    import math
    from typing import Any
except Exception as e:
    print("Import error:", e)


def tensor_to_list(input: torch.Tensor) -> Any:
    """Transforms the given tensors in a list

    Args:
        input (torch.Tensor): Tensors to convert

    Returns:
        List of tensors
    """
    try:
        return input.tolist()[0]
    except Exception as e:
        printerr(f"Tensor conversion error: {e}")


def translate_token_from_int(wordlist_path: str, token: int) -> str:
    """Returns the corresponding string value for the given token

    Args:
        wordlist_path (str): path to the wordlist for conversion
        token (int): token to translate : int->str

    Raises:
        ValueError: Token not found

    Returns:
        str: Translated token
    """
    # Opens the wordlist and loads it as a python object
    with open(wordlist_path, "r") as wordlist_file:
        wordlist = json.load(wordlist_file)
        # Scan each token for the one we want
        for current_token in wordlist:
            if wordlist[current_token] == token:
                # Token found, returning its string value
                return str(current_token)
    raise ValueError(f"The given token ({token}) was not found")


def get_highest_str_token_from_logits(logits: list[float],
                                      wordlist_path: str) -> str:
    """Returns the (str) highest token from the given logits

    Args:
        logits (list[float]): Logits list to analyze
        wordlist_path (str): Path to the wordlist (for translation)

    Returns:
        str: string value of the highest-value token
    """
    # Gets the highest token's index from the logits
    highest_token_index = logits.index(max(logits))
    # Translates the token's index to its corresponding string value
    highest_token_str = translate_token_from_int(wordlist_path,
                                                 highest_token_index)
    # Returning the string token
    return highest_token_str


def set_null_highest_token(logits: list[float]) -> list[float]:
    """Returns logits with the highest token neutralized

    Args:
        logits (list[float]): Original logits

    Returns:
        list[float]: New logits (with highest token to -inf)
    """
    logits[logits.index(max(logits))] = -math.inf
    # Returning the new logits
    return logits
