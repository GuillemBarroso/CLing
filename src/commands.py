"""Module containing the Command class."""

import pygame

from src.events_definition import CMD_FULL_SCREEN, CMD_REGULAR_SIZE, VALLEY

# from src.object_interaction import get_closest_object_requested_by_user
# from src.objects import BreakableWall, Wall


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

    def execute(self, cmd_line, arguments, _, __):
        """Execute command."""
        if arguments:
            args, message = self.parse_arguments(arguments)
            if message:
                cmd_line.input.value = message
                cmd_line.write_command_response()
            elif len(args) > 1:
                cmd_line.input.value = (
                    "When using 'help', only one command can be requested."
                )
                cmd_line.write_command_response()
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
        cmd_line.write_command_response()
        cmd_line.input.value = "Available arguments are:"
        cmd_line.write_command_response()
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
            cmd_line.write_command_response()
        cmd_line.input.value = "Usage:"
        cmd_line.write_command_response()
        for example in cmd.examples:
            cmd_line.input.value = f"  - {example}"
            cmd_line.write_command_response()


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

    def execute(self, cmd_line, arguments, _, __):
        """Execute command."""
        args, message = self.parse_arguments(arguments)
        if message:
            cmd_line.input.value = message
            cmd_line.write_command_response()
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

    def execute(self, cmd_line, arguments, player, sprites):
        """Execute command."""
        closest_sprites, distances = player.get_closest_sprites(sprites)
        if closest_sprites:
            min_dist_pos = distances.index(min(distances))
            closest_sprite = closest_sprites[min_dist_pos]
            if arguments in closest_sprite.sprite_type:
                cmd_line.input.value = closest_sprite.look_at()
            else:
                cmd_line.input.value = f"You don't find a '{arguments}' nearby."
        else:
            cmd_line.input.value = "There is nothing to interact with"
        cmd_line.write_command_response()


class Break(Command):
    """Break command."""

    def __init__(self):
        """Initialize."""
        parameters = {
            "name": "break",
            "short_name": "",
            "description": "Break an object.",
            "extended_description": "Some objectes will be able to be broken by the player.",
            "arguments": [
                "wall",
            ],
            "examples": ["break wall"],
        }
        super().__init__(**parameters)

    def execute(self, cmd_line, arguments, player, sprites):
        """Execute command."""
        closest_sprites, distances = player.get_closest_sprites(sprites)
        if closest_sprites:
            min_dist_pos = distances.index(min(distances))
            closest_sprite = closest_sprites[min_dist_pos]
            if arguments in closest_sprite.sprite_type:
                cmd_line.input.value = closest_sprite.break_it()
                cmd_line.entry_cave_opened = True
                closest_sprite.image = pygame.image.load("src/images/map/doors/315.png")
                closest_sprite.update()
            else:
                cmd_line.input.value = f"You don't find a '{arguments}' nearby."
        else:
            cmd_line.input.value = "There is nothing to interact with"
        cmd_line.write_command_response()


class Crawl_into(Command):
    """Crawl into command."""

    def __init__(self):
        """Initialize."""
        parameters = {
            "name": "crawl into",
            "short_name": "",
            "description": "Crawl into something.",
            "extended_description": "You may be able to crawl into narrow caves or tight holes.",
            "arguments": [
                "",
            ],
            "examples": ["crawl into hole"],
        }
        super().__init__(**parameters)

    def execute(self, cmd_line, arguments, player, sprites):
        """Execute command."""
        closest_sprites, distances = player.get_closest_sprites(sprites)
        if closest_sprites:
            min_dist_pos = distances.index(min(distances))
            closest_sprite = closest_sprites[min_dist_pos]
            if arguments in closest_sprite.sprite_type:
                pygame.event.post(pygame.event.Event(VALLEY))
            else:
                cmd_line.input.value = f"You don't find a {arguments} nearby."
        else:
            cmd_line.input.value = "There is nothing to interact with"
        cmd_line.write_command_response()


help = Help()
cl = Cmd_line()
look_at = Look_at()
break_ = Break()
crawl_into = Crawl_into()

cmd_dict = {
    "help": help,
    "h": help,
    "command line": cl,
    "cl": cl,
    "look at": look_at,
    "break": break_,
    "crawl into": crawl_into,
}
