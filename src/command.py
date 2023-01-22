"""Module containing the Command class."""


class Command:
    """Command class containing all the information for a CL command."""

    def __init__(self):
        """Initialise command class."""
        self._name = ""
        self._description = ""
        self._extended_description = ""
        self._short_name = ""
        self._arguments = []
        self._examples = []

    @property
    def name(self):
        """Return command name."""
        self._name

    @property
    def description(self):
        """Return command description."""
        self._description

    @property
    def extended_description(self):
        """Return command extended_description."""
        self._extended_description

    @property
    def short_name(self):
        """Return command short_name."""
        self._short_name

    @property
    def arguments(self):
        """Return command arguments."""
        self._arguments

    @property
    def examples(self):
        """Return command examples."""
        self._examples

    def set_name(self, value):
        """Set command name property."""
        self._name = value

    def set_description(self, value):
        """Set command description property."""
        self._description = value

    def set_extended_description(self, value):
        """Set command extended description property."""
        self._extended_description = value

    def set_short_name(self, value):
        """Set command short name property."""
        self._short_name = value

    def set_arguments(self, value):
        """Set command arguments property."""
        self._arguments = value

    def set_examples(self, value):
        """Set command examples property."""
        self._examples = value
