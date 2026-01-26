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
INTERPRETER=python3


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
	uv run python3.14 -m src --input 