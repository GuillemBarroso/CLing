"""Module containing tests for the Cursor class."""
# import pytest

# from src.cursor import Cursor


# MOVE_POSITION_LIST = [
#     [[-4, -2], "_J", False, 2, "Janeoe", -2],
#     [[-2, -4], "_J", True, 2, "Janeoe", -2],
#     [[-8, -4], "Jane", False, 4, "_Joe", -4],
#     [[-4, -8], "Jane", True, 4, "_Joe", -4],
#     [[-3, 0], "Joe", False, 3, "Jane_", 0],
#     [[0, -3], "Joe", True, 3, "Jane_", 0],
#     [[0, 0], "", False, 0, "Jane_Joe", 0],
#     [[-3, -3], "", False, 0, "Jane_Joe", -3],
#     [[-8, -8], "", False, 0, "Jane_Joe", -8],
# ]

# @pytest.fixture(params=MOVE_POSITION_LIST)
# def param_del(request):
#     """Fixture for delete tests."""
#     return request.param

# def test_move_position():
#     """Test selection functionality."""
#     cursor = Cursor()
#     cl.input.value = "One Two Three"
#     cursor.position = -2
#     cursor.move_position()


# def test_create_rectangle():
