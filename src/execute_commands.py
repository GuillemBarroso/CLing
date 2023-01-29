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


def trigger_user_commands(cmd_line):
    """Capture user inputs that require a response message in the CL."""
    input = cmd_line.input
    help = Help()
    cl = Cmd_line()

    user_command, arguments, message = get_command_from_user_input(cmd_line.user_input)
    if message:
        input.value = message
    else:
        if user_command == help.name or user_command == help.short_name:
            if arguments:
                args, message = parse_arguments(arguments, help)
                if message:
                    input.value = message
                elif len(args) > 1:
                    input.value = (
                        "When using 'help', only one command can be requested."
                    )
                else:
                    if args[0] == "command line":
                        command = "cl"
                    else:
                        command = args[0]
                    cmd = locals()[command]
                    input.value = (
                        f"{cmd.name}: {cmd.description} {cmd.extended_description}"
                        f"Available arguments are: {cmd.arguments}. Usage: {cmd.examples}"
                    )
            else:
                input.value = (
                    f"{help.description} {help.extended_description}. "
                    f"Usage: {help.examples}"
                )
            write_command_resonse(cmd_line)

        elif user_command == cl.name or user_command == cl.short_name:
            args, message = parse_arguments(arguments, cl)
            if message:
                input.value = message
            else:
                for i, arg in enumerate(args):
                    if arg == "full screen" or arg == "fc":
                        if args[i + 1] == "on":
                            pygame.event.post(pygame.event.Event(CMD_FULL_SCREEN))
                        elif args[i + 1] == "off":
                            pygame.event.post(pygame.event.Event(CMD_REGULAR_SIZE))
                        else:
                            input.value = (
                                f"The 'full screen' argument must be followed by "
                                "either 'on' or 'off'."
                            )
                    if arg == "clear":
                        cmd_line._history = []


def write_command_resonse(cmd_line):
    """Write on CL the content of input.value and store it in CL history."""
    cmd_line.input.prompt = "  "
    cmd_line.reset_after_enter(cmd_line.input.value)
    cmd_line.input.prompt = "> "


def get_command_from_user_input(user_input):
    """Return main command and the arguments introduced by the user."""
    for command in COMMAND_LIST:
        index_ini = user_input.find(command)
        if not index_ini == -1:
            break
    else:
        message = f"Command '{user_input}' is not a valid command"
        return None, None, message
    assert index_ini == 0, "The command must be introduced in the first place"
    index_end = len(command)
    return user_input[index_ini:index_end], user_input[index_end:], ""


def parse_arguments(arguments, cmd):
    """Return the arguments introduced by the users after the command."""
    user_args = []
    for cmd_args in cmd.arguments:
        if type(cmd_args) is list:
            for names in cmd_args:
                for name in names:
                    ini_idx = arguments.find(name)
                    if not ini_idx == -1:
                        user_args.append(arguments[ini_idx : ini_idx + len(name)])
                        arguments = (
                            arguments[:ini_idx] + arguments[ini_idx + len(name) :]
                        )
                    if arguments.isspace():
                        break
                if arguments.isspace():
                    break
        elif type(cmd_args) is str:
            ini_idx = arguments.find(cmd_args)
            if not ini_idx == -1:
                user_args.append(arguments[ini_idx : ini_idx + len(cmd_args)])
                arguments = arguments[:ini_idx] + arguments[ini_idx + len(cmd_args) :]
            if arguments.isspace():
                break
        else:
            ini_idx = arguments.find(cmd_args[0])
            if not ini_idx == -1:
                user_args.append(arguments[ini_idx : ini_idx + len(cmd_args[0])])
                arguments = (
                    arguments[:ini_idx] + arguments[ini_idx + len(cmd_args[0]) :]
                )
            if arguments.isspace():
                break
    if not arguments.isspace():
        message = f"The following user inputs '{arguments}' have not been correctly identified."
    else:
        message = ""
    return user_args, message


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
        return (
            None,
            None,
            None,
            f"Invalid argument '{user_args[0]}' for command '{cmd.name}'",
        )


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
