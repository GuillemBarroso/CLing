"""Module containing text classes."""

import time

import pygame
import pygame.locals as locals


class ConfigError(KeyError):
    """Error class."""

    pass


class Config:
    """A utility for configuration."""

    def __init__(self, options, *look_for):
        """Initialize config class."""
        assertions = []
        for key in look_for:
            if key[0] in options.keys():
                exec("self." + key[0] + " = options['" + key[0] + "']")
            else:
                exec("self." + key[0] + " = " + key[1])
            assertions.append(key[0])
        for key in options.keys():
            if key not in assertions:
                raise ConfigError(key + " not expected as option")


class Input:
    """A text input for pygame apps."""

    def __init__(self, **options):
        """Options: x, y, font, color, restricted, maxlength, prompt."""
        self.options = Config(
            options,
            ["x", "0"],
            ["y", "0"],
            ["font", 'pygame.font.Font("src/fonts/Times_New_Roman.ttf", 18)'],
            ["color", "(0,0,0)"],
            [
                "restricted",
                "'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\
                !\"#$%&\\'()*+,-./:;<=>?@[\]^_`{|}~'",
            ],
            ["maxlength", "-1"],
            ["prompt", "''"],
            ["focus", "False"],
        )
        self.x = self.options.x
        self.y = self.options.y
        self.font = self.options.font
        self.color = self.options.color
        self.restricted = self.options.restricted
        self.maxlength = self.options.maxlength
        self.prompt = self.options.prompt
        self.value = ""
        self.shifted = False
        self.pause = 0
        self.focus = self.options.focus

    def set_pos(self, x, y):
        """Set the position to x, y."""
        self.x = x
        self.y = y

    def set_font(self, font):
        """Set the font for the input."""
        self.font = font

    def draw(self, surface):
        """Draw the text input to a surface."""
        text = self.font.render(self.prompt + self.value, 1, self.color)
        surface.blit(text, (self.x, self.y))

    def update(self, events):
        """Update the input based on passed events."""
        if self.focus != True:
            return

        pressed = (
            pygame.key.get_pressed()
        )  # Add ability to hold down delete key and delete text
        if self.pause == 3 and pressed[locals.K_BACKSPACE]:
            self.pause = 0
            self.value = self.value[:-1]
        elif pressed[locals.K_BACKSPACE]:
            self.pause += 1
        else:
            self.pause = 0

        for event in events:
            if event.type == locals.KEYUP:
                if event.key == locals.K_LSHIFT or event.key == locals.K_RSHIFT:
                    self.shifted = False
            if event.type == locals.KEYDOWN:
                if event.key == locals.K_BACKSPACE:
                    self.value = self.value[:-1]
                    # Add small delay to slow a bit the backspace action
                    time.sleep(0.1)
                elif event.key == locals.K_LSHIFT or event.key == locals.K_RSHIFT:
                    self.shifted = True
                elif event.key == locals.K_SPACE:
                    self.value += " "
                elif event.key == locals.K_RETURN:
                    return self.value  # return value
                if not self.shifted:
                    if event.key == locals.K_a and "a" in self.restricted:
                        self.value += "a"
                    elif event.key == locals.K_b and "b" in self.restricted:
                        self.value += "b"
                    elif event.key == locals.K_c and "c" in self.restricted:
                        self.value += "c"
                    elif event.key == locals.K_d and "d" in self.restricted:
                        self.value += "d"
                    elif event.key == locals.K_e and "e" in self.restricted:
                        self.value += "e"
                    elif event.key == locals.K_f and "f" in self.restricted:
                        self.value += "f"
                    elif event.key == locals.K_g and "g" in self.restricted:
                        self.value += "g"
                    elif event.key == locals.K_h and "h" in self.restricted:
                        self.value += "h"
                    elif event.key == locals.K_i and "i" in self.restricted:
                        self.value += "i"
                    elif event.key == locals.K_j and "j" in self.restricted:
                        self.value += "j"
                    elif event.key == locals.K_k and "k" in self.restricted:
                        self.value += "k"
                    elif event.key == locals.K_l and "l" in self.restricted:
                        self.value += "l"
                    elif event.key == locals.K_m and "m" in self.restricted:
                        self.value += "m"
                    elif event.key == locals.K_n and "n" in self.restricted:
                        self.value += "n"
                    elif event.key == locals.K_o and "o" in self.restricted:
                        self.value += "o"
                    elif event.key == locals.K_p and "p" in self.restricted:
                        self.value += "p"
                    elif event.key == locals.K_q and "q" in self.restricted:
                        self.value += "q"
                    elif event.key == locals.K_r and "r" in self.restricted:
                        self.value += "r"
                    elif event.key == locals.K_s and "s" in self.restricted:
                        self.value += "s"
                    elif event.key == locals.K_t and "t" in self.restricted:
                        self.value += "t"
                    elif event.key == locals.K_u and "u" in self.restricted:
                        self.value += "u"
                    elif event.key == locals.K_v and "v" in self.restricted:
                        self.value += "v"
                    elif event.key == locals.K_w and "w" in self.restricted:
                        self.value += "w"
                    elif event.key == locals.K_x and "x" in self.restricted:
                        self.value += "x"
                    elif event.key == locals.K_y and "y" in self.restricted:
                        self.value += "y"
                    elif event.key == locals.K_z and "z" in self.restricted:
                        self.value += "z"
                    elif event.key == locals.K_0 and "0" in self.restricted:
                        self.value += "0"
                    elif event.key == locals.K_1 and "1" in self.restricted:
                        self.value += "1"
                    elif event.key == locals.K_2 and "2" in self.restricted:
                        self.value += "2"
                    elif event.key == locals.K_3 and "3" in self.restricted:
                        self.value += "3"
                    elif event.key == locals.K_4 and "4" in self.restricted:
                        self.value += "4"
                    elif event.key == locals.K_5 and "5" in self.restricted:
                        self.value += "5"
                    elif event.key == locals.K_6 and "6" in self.restricted:
                        self.value += "6"
                    elif event.key == locals.K_7 and "7" in self.restricted:
                        self.value += "7"
                    elif event.key == locals.K_8 and "8" in self.restricted:
                        self.value += "8"
                    elif event.key == locals.K_9 and "9" in self.restricted:
                        self.value += "9"
                    elif event.key == locals.K_BACKQUOTE and "`" in self.restricted:
                        self.value += "`"
                    elif event.key == locals.K_MINUS and "-" in self.restricted:
                        self.value += "-"
                    elif event.key == locals.K_EQUALS and "=" in self.restricted:
                        self.value += "="
                    elif event.key == locals.K_LEFTBRACKET and "[" in self.restricted:
                        self.value += "["
                    elif event.key == locals.K_RIGHTBRACKET and "]" in self.restricted:
                        self.value += "]"
                    elif event.key == locals.K_BACKSLASH and "\\" in self.restricted:
                        self.value += "\\"
                    elif event.key == locals.K_SEMICOLON and ";" in self.restricted:
                        self.value += ";"
                    elif event.key == locals.K_QUOTE and "'" in self.restricted:
                        self.value += "'"
                    elif event.key == locals.K_COMMA and "," in self.restricted:
                        self.value += ","
                    elif event.key == locals.K_PERIOD and "." in self.restricted:
                        self.value += "."
                    elif event.key == locals.K_SLASH and "/" in self.restricted:
                        self.value += "/"
                elif self.shifted:
                    if event.key == locals.K_a and "A" in self.restricted:
                        self.value += "A"
                    elif event.key == locals.K_b and "B" in self.restricted:
                        self.value += "B"
                    elif event.key == locals.K_c and "C" in self.restricted:
                        self.value += "C"
                    elif event.key == locals.K_d and "D" in self.restricted:
                        self.value += "D"
                    elif event.key == locals.K_e and "E" in self.restricted:
                        self.value += "E"
                    elif event.key == locals.K_f and "F" in self.restricted:
                        self.value += "F"
                    elif event.key == locals.K_g and "G" in self.restricted:
                        self.value += "G"
                    elif event.key == locals.K_h and "H" in self.restricted:
                        self.value += "H"
                    elif event.key == locals.K_i and "I" in self.restricted:
                        self.value += "I"
                    elif event.key == locals.K_j and "J" in self.restricted:
                        self.value += "J"
                    elif event.key == locals.K_k and "K" in self.restricted:
                        self.value += "K"
                    elif event.key == locals.K_l and "L" in self.restricted:
                        self.value += "L"
                    elif event.key == locals.K_m and "M" in self.restricted:
                        self.value += "M"
                    elif event.key == locals.K_n and "N" in self.restricted:
                        self.value += "N"
                    elif event.key == locals.K_o and "O" in self.restricted:
                        self.value += "O"
                    elif event.key == locals.K_p and "P" in self.restricted:
                        self.value += "P"
                    elif event.key == locals.K_q and "Q" in self.restricted:
                        self.value += "Q"
                    elif event.key == locals.K_r and "R" in self.restricted:
                        self.value += "R"
                    elif event.key == locals.K_s and "S" in self.restricted:
                        self.value += "S"
                    elif event.key == locals.K_t and "T" in self.restricted:
                        self.value += "T"
                    elif event.key == locals.K_u and "U" in self.restricted:
                        self.value += "U"
                    elif event.key == locals.K_v and "V" in self.restricted:
                        self.value += "V"
                    elif event.key == locals.K_w and "W" in self.restricted:
                        self.value += "W"
                    elif event.key == locals.K_x and "X" in self.restricted:
                        self.value += "X"
                    elif event.key == locals.K_y and "Y" in self.restricted:
                        self.value += "Y"
                    elif event.key == locals.K_z and "Z" in self.restricted:
                        self.value += "Z"
                    elif event.key == locals.K_0 and ")" in self.restricted:
                        self.value += ")"
                    elif event.key == locals.K_1 and "!" in self.restricted:
                        self.value += "!"
                    elif event.key == locals.K_2 and "@" in self.restricted:
                        self.value += "@"
                    elif event.key == locals.K_3 and "#" in self.restricted:
                        self.value += "#"
                    elif event.key == locals.K_4 and "$" in self.restricted:
                        self.value += "$"
                    elif event.key == locals.K_5 and "%" in self.restricted:
                        self.value += "%"
                    elif event.key == locals.K_6 and "^" in self.restricted:
                        self.value += "^"
                    elif event.key == locals.K_7 and "&" in self.restricted:
                        self.value += "&"
                    elif event.key == locals.K_8 and "*" in self.restricted:
                        self.value += "*"
                    elif event.key == locals.K_9 and "(" in self.restricted:
                        self.value += "("
                    elif event.key == locals.K_BACKQUOTE and "~" in self.restricted:
                        self.value += "~"
                    elif event.key == locals.K_MINUS and "_" in self.restricted:
                        self.value += "_"
                    elif event.key == locals.K_EQUALS and "+" in self.restricted:
                        self.value += "+"
                    elif event.key == locals.K_LEFTBRACKET and "{" in self.restricted:
                        self.value += "{"
                    elif event.key == locals.K_RIGHTBRACKET and "}" in self.restricted:
                        self.value += "}"
                    elif event.key == locals.K_BACKSLASH and "|" in self.restricted:
                        self.value += "|"
                    elif event.key == locals.K_SEMICOLON and ":" in self.restricted:
                        self.value += ":"
                    elif event.key == locals.K_QUOTE and '"' in self.restricted:
                        self.value += '"'
                    elif event.key == locals.K_COMMA and "<" in self.restricted:
                        self.value += "<"
                    elif event.key == locals.K_PERIOD and ">" in self.restricted:
                        self.value += ">"
                    elif event.key == locals.K_SLASH and "?" in self.restricted:
                        self.value += "?"

        if len(self.value) > self.maxlength and self.maxlength >= 0:
            self.value = self.value[:-1]
