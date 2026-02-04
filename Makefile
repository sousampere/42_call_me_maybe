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

# export HF_HOME=
# export UV_CACHE_DIR=


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

sync:
	uv sync

run:
	uv run python3.14 -m src --input $(DEFAULT_INPUT) --output $(DEFAULT_OUTPUT)

run-verbose:
	uv run python3.14 -m src --input $(DEFAULT_INPUT) --output $(DEFAULT_OUTPUT) --verbose=true

flake8: sync
	uv run python3.14 -m flake8 ./src

mypy: sync
	uv run python3.14 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

mypy-strict: sync
	uv run python3.14 -m mypy . --strict

lint: flake8 mypy

lint-strict: flake8 mypy-strict

debug:
	python -m pdb -m src --input $(DEFAULT_INPUT) --output $(DEFAULT_OUTPUT)

debug-verbose:
	python -m pdb -m src --input $(DEFAULT_INPUT) --output $(DEFAULT_OUTPUT) --verbose=true

clean:
	rm -rf data/output
	rm -rf .venv
	rm -rf .mypy_cache
# 	rm -rf llm
	rm -rf __pycache__
	rm -rf .pytest_cache

re: clean install

test: sync
	uv run python3.14 -m pytest tester/run_test.py