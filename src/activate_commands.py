"""Module in charge of triggering CL commands."""

import pygame

from src.command_definition import commands
from src.events_definition import CMD_FULL_SCREEN, CMD_REGULAR_SIZE


def activate_cl_commands(event, cmd_line):
    """Activate CL commands coming from events."""
    # Enter CL full screen mode
    if event.type == CMD_FULL_SCREEN:
        cmd_line.maximize()

    # Return to regular CL view
    if event.type == CMD_REGULAR_SIZE:
        cmd_line.minimize()


def post_events_from_cl_inputs(cmd_line):
    """Post user defined events coming from CL."""
    if cmd_line.user_input == "max":
        pygame.event.post(pygame.event.Event(CMD_FULL_SCREEN))
    elif cmd_line.user_input == "min":
        pygame.event.post(pygame.event.Event(CMD_REGULAR_SIZE))


def trigger_commands_that_print_output(cmd_line):
    """Capture user inputs that require a response message in the CL."""
    cmd = commands.get(cmd_line.user_input)
    input = cmd_line.input

    if cmd == None:
        input.value = f"{cmd} is not a valid command. Please use `help` to \
            see all the available commands."
    else:
        if cmd == "help":
            input.value = f"{cmd.arguments}"
    input.prompt = " "
    cmd_line.reset_after_enter(input.value)
    input.prompt = "> "
