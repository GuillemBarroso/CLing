"""Module in charge of triggering CL commands."""

from src.commands import cmd_dict, write_command_response
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

    user_command, arguments, message = get_command_from_user_input(cmd_line.user_input)
    if message:
        input.value = message
        write_command_response(cmd_line)
    else:
        command = cmd_dict[user_command]
        command.execute(cmd_line, arguments)


def get_command_from_user_input(user_input):
    """Return main command and the arguments introduced by the user."""
    for command in cmd_dict.keys():
        index_ini = user_input.find(command)
        if not index_ini == -1:
            break
    else:
        message = f"Command '{user_input}' is not a valid command"
        return None, None, message
    assert index_ini == 0, "The command must be introduced in the first place"
    index_end = len(command)
    return user_input[index_ini:index_end], user_input[index_end:], ""
