"""Module containing tests for the Selection object."""

import pytest

from src.text import Text

DELETE_STRING = "Jane_Joe"

# Lists with [
#   interval,
#   expected_selection,
#   is_inverted,
#   selection_length
#   expected_output_string,
#   expected_current_idx,
# ]
DEL_SELECT_LIST = [
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
TEXT_MODES_LIST = [
    "shifted",
    "moving_arrows",
    "select_ongoing",
    "select_maintain",
    "select_substitute",
    "select_delete",
]
DEL_SELECT_MODES = dict.fromkeys(TEXT_MODES_LIST, False)
DEL_SELECT_MODES["select_delete"] = True


@pytest.fixture(params=DEL_SELECT_LIST)
def param_del(request):
    """Fixture for delete tests."""
    return DELETE_STRING, request.param, DEL_SELECT_MODES


def test_selection(param_del):
    """Test selection init object."""
    text = param_del[0]
    start = int(param_del[1][0][0])
    end = int(param_del[1][0][1])

    selection = Text(text, start, end, param_del[2])

    assert selection.get_selected_text() == param_del[1][1]
    assert selection.is_inverted == param_del[1][2]
    assert selection.selection_length == param_del[1][3]


def test_delete_selection(param_del):
    """Test delete section method."""
    text = param_del[0]
    start = int(param_del[1][0][0])
    end = int(param_del[1][0][1])

    selection = Text(text, start, end, param_del[2])

    text, idx = selection.delete()
    assert text == param_del[1][4]
    assert idx == param_del[1][5]


DEL_LETTER_LIST = [
    [[0, 0], False, "Jane_Jo", 0],
    [[-3, -3], False, "JaneJoe", -3],
    [[-7, -7], False, "ane_Joe", -7],
    [[-8, -8], False, "Jane_Joe", -8],
]

DEL_LETTER_MODES = dict.fromkeys(TEXT_MODES_LIST, False)


@pytest.fixture(params=DEL_LETTER_LIST)
def param_del(request):
    """Fixture for delete tests."""
    return DELETE_STRING, request.param, DEL_LETTER_MODES


def test_delete_letter(param_del):
    """Testing deleting a letter."""
    text = param_del[0]
    start = int(param_del[1][0][0])
    end = int(param_del[1][0][1])

    text = Text(text, start, end, param_del[2])
    assert text.has_selection == param_del[1][1]

    text, idx = text.delete()
    assert text == param_del[1][2]
    assert idx == param_del[1][3]


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

SUBSTITUTE_MODES = dict.fromkeys(TEXT_MODES_LIST, False)
SUBSTITUTE_MODES["select_substitute"] = True


@pytest.fixture(params=SUBSTITUTE_LIST)
def param_subst(request):
    """Fixture for substitute tests."""
    return SUBSTITUTE_STRING, request.param, SUBSTITUTE_MODES


def test_substitute_selection(param_subst):
    """Test substitute selection method."""
    text = param_subst[0]
    start = int(param_subst[1][0][0])
    end = int(param_subst[1][0][1])

    selection = Text(text, start, end, SUBSTITUTE_MODES)

    text, idx = selection.substitute()

    assert text == param_subst[1][1]
    assert idx == param_subst[1][2]
