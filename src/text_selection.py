"""Module containing the Selector class."""


class Selection:
    """Selection class. Operates with a selected text."""

    def __init__(self, text, start, end, mode="delete"):
        """Initialize selection class with a text and the two indices of the selection."""
        # It is assumed that start and end are negative integers (position from the right)
        # Mode can be either "delete" or "substitute".
        self.text = text
        self.start = start
        self.end = end
        self.mode = mode

        self._input_check()
        if mode == "substitute":
            # Assume that the letter that will be substituted is at the end of the string
            self.text, self.subsitute_letter = self._preprocess_string()

        self.text_length = len(self.text)
        self.is_inverted = self._check_if_selection_inverted()
        self.selection_length = self._get_selection_length()

    def _input_check(self):
        """Check if inputs are valid."""
        assert type(self.text) == str
        assert type(self.start) == int and self.start <= 0
        assert type(self.end) == int and self.end <= 0
        assert type(self.mode) == str and self.mode in ["delete", "substitute"]

    def _check_if_selection_inverted(self):
        """Assuming indices are negative, return whether the selection is inverted."""
        if self.start > self.end:
            return True  # inverted selection, selecting from left to right
        elif self.start <= self.end:
            return False  # not inverted, selecting from right to left

    def _get_selection_length(self):
        """Return the length of the selection."""
        if self.is_inverted:
            return self.start - self.end
        else:
            return self.end - self.start

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

    def _delete_selection(self):
        """Delete the selection. Return remaining string and new position."""
        if self.start == self.end == 0:
            text = self.text
            idx = 0
        elif self.end == 0:
            text = self.text[: self.start]
            idx = 0
        elif self.start == 0:
            text = self.text[: self.end]
            idx = 0
        elif self.start == self.end:
            text = self.text
            idx = self.start
        elif not self.start == self.end:
            if self.is_inverted:
                text = self.text[: self.end] + self.text[self.start :]
                idx = self.start
            else:
                text = self.text[: self.start] + self.text[self.end :]
                idx = -self.selection_length
        return text, idx

    def _preprocess_string(self):
        """Return original string and letter which wants to be substituted."""
        # String contains a letter at the end which has to substitute the selection
        new_letter = self.text[-1]
        text = self.text[:-1]
        return text, new_letter

    def resolve(self):
        """Resolve selection action, whether is deletion or substitution."""
        text, idx = self._delete_selection()
        if self.mode == "substitute":
            if idx == 0:
                text = text[idx:] + self.subsitute_letter
            else:
                text = text[:idx] + self.subsitute_letter + text[idx:]
        return text, idx
