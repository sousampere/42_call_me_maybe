#!/usr/bin/python3
try:
    import json
    from src.misc import printerr
    from src import Small_LLM_Model
except Exception as e:
    print('Import error:', e)


def tensor_to_list(input: Tensor) -> list[int]:
    """ Transforms a list of tensors into a python list """
    try:
        return input.tolist()[0]
    except Exception as e:
        printerr(f'Tensor conversion error: {e}')
        exit(1)


def translate_token_from_int(wordlist_path: str, token: int):
    with open(wordlist_path, 'r') as wordlist_file:
        wordlist = json.load(wordlist_file)
        for current_token in wordlist:
            if wordlist[current_token] == token:
                return current_token
        raise ValueError(f'The given token ({token}) was not found')


def generate_next_word(last_output: str, llm: Small_LLM_Model) -> str:
    #* Encoding tokens (tensor([[4913,  606,  788,  330,   32]], ...)
    encoded = llm._encode(last_output)
    #* Processing probabilities
    probabilities = llm.get_logits_from_input_ids(tensor_to_list(encoded))
    #* Handling highest rate token
    generated_word = translate_token_from_int(
        wordlist_path = llm.get_path_to_vocabulary_json(),
        token=probabilities.index(max(probabilities)))
    #* Returning result
    return generated_word
