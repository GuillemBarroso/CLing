"""Module containing the Command class."""

import pygame

from src.events_definition import CMD_FULL_SCREEN, CMD_REGULAR_SIZE


class Command:
    """Command class containing all the information for a CL command."""

    def __init__(
        self, name, description, extended_description, short_name, arguments, examples
    ):
        """Initialise command class."""
        self.name = name
        self.short_name = short_name
        self.description = description
        self.extended_description = extended_description
        self.arguments = arguments
        self.examples = examples

    def parse_arguments(self, arguments):
        """Return the arguments introduced by the users after the command."""
        user_args = []
        for cmd_args in self.arguments:
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
                    arguments = (
                        arguments[:ini_idx] + arguments[ini_idx + len(cmd_args) :]
                    )
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
            message = (
                f"The argument '{arguments}' is not a valid argument for the "
                f"command '{self.name}'."
            )
        else:
            message = ""
        return user_args, message


HELP_ARGUMENTS = [[("command line", "cl")], "look at"]


class Help(Command):
    """Help command."""

    def __init__(self):
        """Initialize."""
        parameters = {
            "name": "help",
            "short_name": "h",
            "description": "Provides information about the command line commands used to "
            "interact with the game.",
            "extended_description": "During the game, you will learn different commands to "
            "interact with the different elements of the game. Use the help command to check "
            "the use of a particular command.",
            "arguments": HELP_ARGUMENTS,
            "examples": ["help", "help <command>", "h <command>"],
        }
        super().__init__(**parameters)

    def execute(self, cmd_line, arguments, _):
        """Execute command."""
        if arguments:
            args, message = self.parse_arguments(arguments)
            if message:
                cmd_line.input.value = message
                write_command_response(cmd_line)
            elif len(args) > 1:
                cmd_line.input.value = (
                    "When using 'help', only one command can be requested."
                )
                write_command_response(cmd_line)
            else:
                cmd = cmd_dict[args[0]]
                self.get_cmd_help_string(cmd_line, cmd)
        else:
            self.get_cmd_help_string(cmd_line, self)

    def get_cmd_help_string(self, cmd_line, cmd):
        """Print description of a command with its possible arguments and examples."""
        cmd_line.input.value = (
            f"'{cmd.name}' or '{cmd.short_name}': "
            f"{cmd.description} {cmd.extended_description}"
        )
        write_command_response(cmd_line)
        cmd_line.input.value = "Available arguments are:"
        write_command_response(cmd_line)
        for arg in cmd.arguments:
            out_string = f"  - "
            if type(arg) == list:
                for name in arg[0]:
                    out_string += f"'{name}' or "
                out_string = out_string[:-4]
                try:
                    out_string += ", which takes values: "
                    for val in arg[1]:
                        out_string += f"'{val}' or "
                    out_string = out_string[:-4]
                except IndexError:
                    out_string = out_string[:-22]
            elif type(arg) == str:
                out_string += arg
            cmd_line.input.value = out_string
            write_command_response(cmd_line)
        cmd_line.input.value = "Usage:"
        write_command_response(cmd_line)
        for example in cmd.examples:
            cmd_line.input.value = f"  - {example}"
            write_command_response(cmd_line)


class Cmd_line(Command):
    """Command line."""

    def __init__(self):
        """Initialize."""
        parameters = {
            "name": "command line",
            "short_name": "cl",
            "description": "Interaction with the command line.",
            "extended_description": "This command allows the user to modify certain "
            "behaviors of the command line.",
            "arguments": [
                [("full screen", "fc"), ("on", "off")],
                "clear",
            ],
            "examples": ["command line full screen on", "cl fc off", "cl clear"],
        }
        super().__init__(**parameters)

    def execute(self, cmd_line, arguments, _):
        """Execute command."""
        args, message = self.parse_arguments(arguments)
        if message:
            cmd_line.input.value = message
            write_command_response(cmd_line)
        else:
            for i, arg in enumerate(args):
                if arg == "full screen" or arg == "fc":
                    if args[i + 1] == "on":
                        pygame.event.post(pygame.event.Event(CMD_FULL_SCREEN))
                    elif args[i + 1] == "off":
                        pygame.event.post(pygame.event.Event(CMD_REGULAR_SIZE))
                    else:
                        cmd_line.input.value = (
                            f"The 'full screen' argument must be followed by "
                            "either 'on' or 'off'."
                        )
                if arg == "clear":
                    cmd_line._history = []


class Look_at(Command):
    """Look at command."""

    def __init__(self):
        """Initialize."""
        parameters = {
            "name": "look at",
            "short_name": "look at",
            "description": "Look at an object of the game.",
            "extended_description": "Some objectes within the game may revel additional "
            "information when looking at them.",
            "arguments": [
                "wall",
            ],
            "examples": ["look at wall"],
        }
        super().__init__(**parameters)

    @staticmethod
    def _get_clostest_object_from_player(closest_objects, distances):
        min_distance = 1e5
        for i, obj in enumerate(closest_objects):
            if min_distance > distances[i]:
                closest_object = obj
        return closest_object

    def execute(self, cmd_line, arguments, player):
        """Execute command."""
        args, message = self.parse_arguments(arguments)
        if message:
            cmd_line.input.value = message
            write_command_response(cmd_line)
        elif len(args) > 1:
            cmd_line.input.value = "The 'look at' command only accepts one argument"
            write_command_response(cmd_line)
        else:
            closest_objects, distances = player.get_closest_object_in_room()
            closest_object = self._get_clostest_object_from_player(
                closest_objects, distances
            )
            cmd_line.input.value = closest_object.look_at()
            write_command_response(cmd_line)


help = Help()
cl = Cmd_line()
look_at = Look_at()

cmd_dict = {
    "help": help,
    "h": help,
    "command line": cl,
    "cl": cl,
    "look at": look_at,
}


def write_command_response(cmd_line, prompt="  "):
    """Write on CL the content of input.value and store it in CL history."""
    cmd_line.input.prompt = prompt
    cmd_line.reset_after_enter(cmd_line.input.value)
    cmd_line.input.prompt = "> "
