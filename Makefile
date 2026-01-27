# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: gtourdia <@student.42mulhouse.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#                                                      #+#    #+#              #
#    26/01/2026            Call me maybe              ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

# I'm starting this new project and I'm not sure that I understood the project very well. Here is what I understood :
# - I open the input json file (by default, it is data/input/function_calling_test.json)
# - For each prompt in this json file, I send it to the LLM
# - I ask the LLM to send back a json formatted output with the following entries : 
#     - original prompt ("prompt")
#     - function name to use to execute the prompt ("fn_name")
#     - arguments to send to the function selected by the LLM
# - While the LLM produces the tokens, I monitor it and apply constrained decoding to make sure that its output is respecting the json format, and that it is respecting the format of the function, defined in the function_definition.json.
# - I repeat the process for every prompt in my input


# PROJECT CONFIGURATION
AUTHOR=gtourdia
PROJECT_NAME=Call_Me_Maybe
PROJECT_START_DATE=2026-01-26
GITHUB=https://github.com/sousampere/

# COLORS
YELLOW=\033[0;33m
CYAN=\033[0;36m
GREEN=\033[0;32m
RESET=\033[0m

# MAIN VARIABLES
INTERPRETER			=	python3
DEFAULT_INPUT		=	data/input/function_calling_tests.json
DEFAULT_OUTPUT		=	data/output/function_calling_result.json


install:
	@echo "$(YELLOW)╔════════════════════════════════════════════════════════════════╗"
	@echo "$(YELLOW)║                                                                ║"
	@echo "$(YELLOW)║  44  44    2222    $(GREEN)Made by $(AUTHOR) $(YELLOW)                           ║"
	@echo "$(YELLOW)║  44  44   22  22   Project: $(CYAN)$(PROJECT_NAME) $(YELLOW)                     ║"
	@echo "$(YELLOW)║  444444      22    Started in: $(CYAN)$(PROJECT_START_DATE) $(YELLOW)                     ║"
	@echo "$(YELLOW)║      44     22     Github: $(CYAN)$(GITHUB) $(YELLOW)     ║"
	@echo "$(YELLOW)║      44   222222                                               ║"
	@echo "$(YELLOW)║                                                                ║"
	@echo "$(YELLOW)╚════════════════════════════════════════════════════════════════╝"
	@echo
	@echo "$(CYAN)[Installation]$(RESET) ➡️  Synchronizing uv"
	uv sync

run:
	uv run python3.14 -m src --input $(DEFAULT_INPUT) --output $(DEFAULT_OUTPUT)
