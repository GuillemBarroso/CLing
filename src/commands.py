"""Module containing the Command class."""


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
            "arguments": ["test", "test2"],
            "examples": ["help", "help <command>", "h <command>"],
        }
        super().__init__(**parameters)


class Cmd_line(Command):
    """Command line."""

    def __init__(self):
        """Initialize."""
        parameters = {
            "name": "command_line",
            "short_name": "cl",
            "description": "Interaction with the command line.",
            "extended_description": "This command allows the user to modify certain "
            "behaviors of the command line.",
            "arguments": [[("full_screen", "fc"), ("on", "off")]],
            "examples": ["command_line full_screen on", "cl fc off"],
        }
        super().__init__(**parameters)
