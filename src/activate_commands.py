"""Module in charge of triggering CL commands."""

import pygame

from src.commands import COMMAND_LIST, Cmd_line, Help
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
    input = cmd_line.input
    help = Help()
    cl = Cmd_line()
    if cmd_line.user_input == help.name or cmd_line.user_input == help.short_name:
        look_for_arguments(cmd_line.user_input, help)
        input.value = (
            f"{help.description} {help.extended_description}. Usage: {help.examples}"
        )

    elif cmd_line.user_input == cl.name or cmd_line.user_input == cl.short_name:
        look_for_arguments(cmd_line.user_input, cl)
        pass
    else:
        input.value = (
            f"'{cmd_line.user_input}' is not a valid command. Please "
            "use `help` to see all the available commands."
        )

    input.prompt = "  "
    cmd_line.reset_after_enter(input.value)
    input.prompt = "> "


def look_for_arguments(user_input, cmd):
    """Return the arguments introduced by the users after the command."""
    for command in COMMAND_LIST:
        index_ini = user_input.find(command)
        if not index_ini == -1:
            break

    assert (index_ini == 0, "The command must be introduced in the first place")
    index_end = index_ini + len(command)
    user_input[index_end:].split(" ")

    for arg in cmd.arguments:
        if arg in user_input:
            pass
    test = 1
