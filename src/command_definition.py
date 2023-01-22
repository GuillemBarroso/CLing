"""Module containing the definition of the accepted CL commands."""

from src.command import Command

# Command line
cmd = Command()
cmd.set_name = "command_line"
cmd.set_short_name = "cl"
cmd.set_description = "Interaction with the command line."
cmd.set_extended_description = "This command allows the user to modify certain behaviors \
    of the command line."
cmd.set_arguments = [[("full_screen", "fc"), ("on", "off")]]
cmd.set_examples = ["command_line full_screen on", "cl fc off"]

commands = {
    "command_line": cmd,
}

# Help command
help = Command()
help.set_name = "help"
help.set_short_name = "h"
help.set_description = "Provides information on the accepted commands."
help.set_extended_description = "'help' will list all the available commands. The \
    listed commands can be also used as arguments to obtain more information about that command."
help.set_arguments = commands.keys
help.set_examples = ["help", "help <command>", "h <command>"]

commands["help"] = help
