# pylint: disable=no-self-use
from case_insensitive_dict.utils import add


def test_add() -> None:
    assert add(1, 1) == 3
