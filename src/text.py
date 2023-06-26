"""Module containing the Text class."""


class Text:
    """Selection class. Operates with a selected text."""

    def __init__(self, text, start, end, modes):
        """Initialize selection class with a text and the two indices of the selection."""
        # It is assumed that start and end are negative integers (position from the right)
        # Mode can be either "delete" or "substitute".
        self.text = text
        self.start = start
        self.end = end
        self.modes = modes
        self.position = None
        self._correct_inputs()
        self._input_check()

        if modes["select_substitute"]:
            # Assume that the letter that will be substituted is at the end of the string
            self.text, self.subsitute_letter = self._preprocess_string()

        self.text_length = len(self.text)
        self.is_inverted = self._check_if_selection_inverted()
        self.selection_length = self._get_selection_length()

        # Check if text object contains a selection
        if (
            modes["select_ongoing"]
            or modes["select_maintain"]
            or modes["select_delete"]
            or modes["select_substitute"]
        ):
            self.has_selection = True
        else:
            self.has_selection = False
            self.position = self.end

    def _correct_inputs(self):
        """Correct inputs."""
        if self.end > 0:
            self.end = 0
        if self.end < -len(self.text):
            self.end = -len(self.text)
        if self.start > 0:
            self.start = 0
        if self.start < -len(self.text):
            self.start = -len(self.text)

    def _input_check(self):
        """Check if inputs are valid."""
        assert type(self.text) == str
        assert type(self.start) == int and self.start <= 0
        assert type(self.end) == int and self.end <= 0
        assert type(self.modes) == dict

    def _check_if_selection_inverted(self):
        """Assuming indices are negative, return whether the selection is inverted."""
        try:
            if self.start > self.end:
                return True  # inverted selection, selecting from left to right
            elif self.start <= self.end:
                return False  # not inverted, selecting from right to left
        except TypeError:
            return False

    def _get_selection_length(self):
        """Return the length of the selection."""
        try:
            if self.is_inverted:
                return self.start - self.end
            else:
                return self.end - self.start
        except TypeError:
            return 0

    def _preprocess_string(self):
        """Return original string and letter which wants to be substituted."""
        # String contains a letter at the end which has to substitute the selection
        new_letter = self.text[-1]
        text = self.text[:-1]
        return text, new_letter

    def get_selected_text(self):
        """Return the selected section of the given text."""
        if self.start == self.end:
            return ""
        elif self.end == 0:
            return self.text[self.start :]
        else:
            if self.is_inverted:
                if self.start == 0:
                    return self.text[self.end :]
                else:
                    return self.text[self.end : self.start]
            else:
                return self.text[self.start : self.end]

    def delete(self):
        """Delete the selection. Return remaining string and new position."""
        if self.has_selection:
            if self.start == self.end == 0:
                text = self.text[:-1]
                idx = 0
            elif self.end == 0:
                text = self.text[: self.start]
                self.start = self.end
                idx = 0
            elif self.start == 0:
                text = self.text[: self.end]
                self.end = self.start
                idx = 0
            elif self.start == self.end:
                text = self.text
                idx = self.start
            elif not self.start == self.end:
                if self.is_inverted:
                    text = self.text[: self.end] + self.text[self.start :]
                    self.end = self.start
                    idx = self.start
                else:
                    text = self.text[: self.start] + self.text[self.end :]
                    self.start = self.end = self.selection_length + self.start
                    idx = self.start
        else:
            if self.position == 0:
                text = self.text[:-1]
                idx = 0
            else:
                text = self.text[: self.position - 1] + self.text[self.position :]
                idx = self.position
        self.has_selection = False
        return text, idx

    def substitute(self):
        """Substitute selection by a letter."""
        assert self.has_selection == True

        text, idx = self.delete()
        if idx == 0:
            text = text[idx:] + self.subsitute_letter
        else:
            text = text[:idx] + self.subsitute_letter + text[idx:]
        return text, idx

    def correct_idxs_for_display(self):
        """Correct idxs by setting them to None if they are 0. Just for displaying purposes."""
        if self.is_inverted:
            if self.start == 0:
                disp_end = None
            else:
                disp_end = self.start
            if self.end == 0:
                disp_start = None
            else:
                disp_start = self.end
        else:
            if self.end == 0:
                disp_end = None
            else:
                disp_end = self.end
            if self.start == 0:
                disp_start = None
            else:
                disp_start = self.start
        return disp_start, disp_end
