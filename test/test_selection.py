"""Module containing tests for the Selection object."""

import pytest

from src.text import Selection

DELETE_STRING = "Jane_Joe"

# Lists with [
#   interval,
#   expected_selection,
#   is_inverted,
#   selection_length
#   expected_output_string,
#   expected_current_idx,
# ]
DELETE_LIST = [
    [[-4, -2], "_J", False, 2, "Janeoe", -2],
    [[-2, -4], "_J", True, 2, "Janeoe", -2],
    [[-8, -4], "Jane", False, 4, "_Joe", -4],
    [[-4, -8], "Jane", True, 4, "_Joe", -4],
    [[-3, 0], "Joe", False, 3, "Jane_", 0],
    [[0, -3], "Joe", True, 3, "Jane_", 0],
    [[0, 0], "", False, 0, "Jane_Joe", 0],
    [[-3, -3], "", False, 0, "Jane_Joe", -3],
    [[-8, -8], "", False, 0, "Jane_Joe", -8],
]


@pytest.fixture(params=DELETE_LIST)
def param_del(request):
    """Fixture for delete tests."""
    return DELETE_STRING, request.param


def test_selection(param_del):
    """Test selection init object."""
    text = param_del[0]
    start = int(param_del[1][0][0])
    end = int(param_del[1][0][1])

    selection = Selection(text, start, end)

    assert selection.get_selected_text() == param_del[1][1]
    assert selection.is_inverted == param_del[1][2]
    assert selection.selection_length == param_del[1][3]


def test_delete_selection(param_del):
    """Test delete section method."""
    text = param_del[0]
    start = int(param_del[1][0][0])
    end = int(param_del[1][0][1])

    selection = Selection(text, start, end)

    text, idx = selection._delete_selection()
    assert text == param_del[1][4]
    assert idx == param_del[1][5]


SUBSTITUTE_STRING = "Jane_Joek"

# Lists with [interval, expected_output_string, expected_current_idx]
SUBSTITUTE_LIST = [
    [[-4, -2], "Janekoe", -2],
    [[-2, -4], "Janekoe", -2],
    [[-8, -4], "k_Joe", -4],
    [[-4, -8], "k_Joe", -4],
    [[-3, 0], "Jane_k", 0],
    [[0, -3], "Jane_k", 0],
    [[0, 0], "Jane_Joek", 0],
    [[-3, -3], "Jane_kJoe", -3],
    [[-8, -8], "kJane_Joe", -8],
]


@pytest.fixture(params=SUBSTITUTE_LIST)
def param_subst(request):
    """Fixture for substitute tests."""
    return SUBSTITUTE_STRING, request.param


def test_substitute_selection(param_subst):
    """Test substitute selection method."""
    text = param_subst[0]
    start = int(param_subst[1][0][0])
    end = int(param_subst[1][0][1])

    selection = Selection(text, start, end, "substitute")

    text, idx = selection.resolve()

    assert text == param_subst[1][1]
    assert idx == param_subst[1][2]
