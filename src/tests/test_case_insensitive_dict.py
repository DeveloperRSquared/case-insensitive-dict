# pylint: disable=no-self-use,protected-access
from types import GeneratorType

import pytest

from case_insensitive_dict import CaseInsensitiveDict


class CaseInsensitiveDictTestCase:
    pass


class TestInit(CaseInsensitiveDictTestCase):
    # check that the store is structured as expected
    def test_store_written(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str](data={"a": "b"})
        assert case_insensitive_dict._data == {"a": ("a", "b")}

    # check that the key in the store is lowered
    def test_store_written_case_insensitive(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str](data={"A": "b"})
        assert case_insensitive_dict._data == {"a": ("A", "b")}

    # check instantiated with an empty dict
    def test_store_written_empty(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str](data={})
        assert isinstance(case_insensitive_dict._data, dict)
        assert not case_insensitive_dict._data

    # check instantiated with none
    def test_store_written_none(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]()
        assert isinstance(case_insensitive_dict._data, dict)
        assert not case_insensitive_dict._data


class TestSetItem(CaseInsensitiveDictTestCase):
    # check key lowered
    def test_store_written(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]()
        case_insensitive_dict["A"] = "b"
        assert case_insensitive_dict._data == {"a": ("A", "b")}

    # check init value overridden (case insensitive)
    def test_value(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"a": "b"})
        assert case_insensitive_dict._data == {"a": ("a", "b")}
        case_insensitive_dict["A"] = "c"
        assert case_insensitive_dict._data == {"a": ("A", "c")}


class TestGetItem(CaseInsensitiveDictTestCase):
    # check value returned
    def test_value_returned(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"a": "b"})
        assert case_insensitive_dict["A"] == "b"
        assert case_insensitive_dict["a"] == "b"
        with pytest.raises(KeyError):
            assert case_insensitive_dict["b"]

    # check value returned using get
    def test_value_returned_using_get(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"a": "b"})
        assert case_insensitive_dict.get("A") == "b"
        assert case_insensitive_dict.get("a") == "b"
        assert case_insensitive_dict.get("b") is None


class TestDelItem(CaseInsensitiveDictTestCase):
    # check value removed
    def test_value_removed(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"a": "b"})
        del case_insensitive_dict["A"]
        assert case_insensitive_dict.get("a") is None


class TestIter(CaseInsensitiveDictTestCase):
    # check iterated keys
    def test_iter(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"a": "b"})
        assert list(case_insensitive_dict) == ["a"]


class TestLen(CaseInsensitiveDictTestCase):
    # check len
    def test_len(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"a": "b"})
        assert len(case_insensitive_dict) == 1

    # check len empty data
    def test_len_empty(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]()
        assert len(case_insensitive_dict) == 0


class TestLowerItems(CaseInsensitiveDictTestCase):
    # check returned value
    def test_lower(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"A": "b"})
        assert list(case_insensitive_dict.lower_items()) == [("a", "b")]

    # check returned value for empty data
    def test_lower_empty(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]()
        assert isinstance(case_insensitive_dict.lower_items(), GeneratorType)
        assert not list(case_insensitive_dict.lower_items())


class TestEq(CaseInsensitiveDictTestCase):
    # check equality empty data
    def test_equality(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]()
        assert case_insensitive_dict == CaseInsensitiveDict[str]()

    # check equality (case insensitive)
    def test_equality_empty(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]()
        assert case_insensitive_dict == CaseInsensitiveDict[str]({})

    # check equality with dictionary
    def test_equality_dictionary(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"A": "b"})
        assert case_insensitive_dict == {"A": "b"}

    # check not equal
    def test_not_equality(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]()
        assert case_insensitive_dict != 1


class TestCopy(CaseInsensitiveDictTestCase):
    # check copy equality
    def test_copy(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"A": "b"})
        assert case_insensitive_dict == case_insensitive_dict.copy()

    # check copy ids
    def test_copy_ids(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str]({"A": "b"})
        assert id(case_insensitive_dict) != id(case_insensitive_dict.copy())
