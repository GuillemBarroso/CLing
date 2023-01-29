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

    user_command, arguments = get_command_from_user_input(cmd_line.user_input)

    if user_command == help.name or user_command == help.short_name:
        if arguments:
            arg, value, message = check_arguments(arguments, help)
        else:
            input.value = f"{help.description} {help.extended_description}. Usage: {help.examples}"

    elif user_command == cl.name or user_command == cl.short_name:
        arg, value, message = check_arguments(arguments, cl)
    else:
        input.value = (
            f"'{cmd_line.user_input}' is not a valid command. Please "
            "use `help` to see all the available commands."
        )

    input.prompt = "  "
    cmd_line.reset_after_enter(input.value)
    input.prompt = "> "


def get_command_from_user_input(user_input):
    """Return main command and the arguments introduced by the user."""
    for command in COMMAND_LIST:
        index_ini = user_input.find(command)
        if not index_ini == -1:
            break
    assert index_ini == 0, "The command must be introduced in the first place"
    index_end = len(command)
    return user_input[index_ini:index_end], user_input[index_end:]


def check_arguments(arguments, cmd):
    """Return the arguments introduced by the users after the command."""
    user_args = [arg for arg in arguments.split(" ") if arg]

    arg, all_args, arg_requires_val, message = find_argument(user_args, cmd)

    if message:
        return None, None, message

    if arg_requires_val:
        if all_args:
            value, all_args, message = find_arg_value(arg, all_args, cmd)
            if message:
                return None, None, message
        else:
            return f"Missing value for argument '{arg}' in command '{cmd.name}'"
    else:
        value = None

    assert len(all_args) == 0, "Only one argument can be introduced at a time"
    return arg, value, ""


def find_argument(user_args, cmd):
    """Find argument in user input."""
    for cmd_args in cmd.arguments:
        if user_args[0] in cmd_args[0]:
            try:
                cmd_args[1]
                arg_requires_val = True
            except IndexError:
                arg_requires_val = False
            return user_args[0], user_args[1:], arg_requires_val, ""
    else:
        return None, None, f"Invalid argument '{user_args[0]}' for command '{cmd.name}'"


def find_arg_value(arg, all_args, cmd):
    """Find value for a particular argument in user input."""
    for cmd_args in cmd.arguments:
        if arg in cmd_args[0]:
            if all_args[0] in cmd_args[1]:
                return all_args[0], all_args[1:], ""
            else:
                message = f"Invalid value '{all_args[0]}' for argument `{arg}`"
                " in ocmmand `{cmd.name}`"
                return None, None, message
