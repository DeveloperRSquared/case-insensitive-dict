# pylint: disable=no-self-use,protected-access
import json
from types import GeneratorType
from typing import Dict
from typing import Optional
from typing import Union

import pytest

from case_insensitive_dict import CaseInsensitiveDict
from case_insensitive_dict import CaseInsensitiveDictJSONEncoder
from case_insensitive_dict import case_insensitive_dict_json_decoder


class CaseInsensitiveDictTestCase:
    pass


class TestInit(CaseInsensitiveDictTestCase):
    # check that the store is structured as expected
    def test_store_written(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b"})
        assert case_insensitive_dict._data == {"a": ("a", "b")}

    # check that the key in the store is lowered
    def test_store_written_case_insensitive(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        assert case_insensitive_dict._data == {"a": ("A", "b")}

    # check instantiated with an empty dict
    def test_store_written_empty(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({})
        assert isinstance(case_insensitive_dict._data, dict)
        assert not case_insensitive_dict._data

    # check instantiated with none
    def test_store_written_none(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str](None)
        assert isinstance(case_insensitive_dict._data, dict)
        assert not case_insensitive_dict._data

    # check instantiated with none value
    def test_store_written_with_optional_value(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, Optional[str]]({"A": None})
        assert case_insensitive_dict._data == {"a": ("A", None)}

    # check instantiation with non-str keys
    def test_init_with_non_str_keys(self) -> None:
        case_insensitive_dict_int = CaseInsensitiveDict[int, str]({1: "b"})
        assert case_insensitive_dict_int._data == {1: (1, "b")}
        case_insensitive_dict_bool = CaseInsensitiveDict[bool, str]({True: "b"})
        assert case_insensitive_dict_bool._data == {True: (True, "b")}

    # check picks the last key/value if instantiated with conflicting cases
    def test_store_written_with_conflicting_cases(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b", "A": "c"})
        assert case_insensitive_dict._data == {"a": ("A", "c")}

    # check instantiated with list of tuples
    def test_store_written_with_list_of_tuples(self) -> None:
        data = [("A", "b")]
        case_insensitive_dict = CaseInsensitiveDict[str, str](data)
        assert case_insensitive_dict._data == {"a": ("A", "b")}


class TestTyping(CaseInsensitiveDictTestCase):
    # check valid typing
    def test_valid_types(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b"})
        # keys
        case_insensitive_dict["a"]  # pylint: disable=pointless-statement
        case_insensitive_dict.get("a")
        # values
        case_insensitive_dict["b"] = "a"

    # check valid typings
    def test_valid_types_non_str_keys(self) -> None:
        case_insensitive_dict_int = CaseInsensitiveDict[int, str]({1: "b"})
        # keys
        case_insensitive_dict_int[1]  # pylint: disable=pointless-statement
        case_insensitive_dict_int.get(1)
        # values
        case_insensitive_dict_int[2] = "a"

    # check valid with union
    def test_valid_types_union(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[Union[str, int], Union[str, int, bool]]({"a": "b", "b": 1, 1: "c"})
        # keys
        case_insensitive_dict[1]  # pylint: disable=pointless-statement
        case_insensitive_dict.get(1)
        case_insensitive_dict["a"]  # pylint: disable=pointless-statement
        case_insensitive_dict.get("a")
        # values
        case_insensitive_dict["b"] = "a"
        case_insensitive_dict["b"] = 2
        case_insensitive_dict["b"] = True
        case_insensitive_dict[2] = "a"
        case_insensitive_dict[2] = 2
        case_insensitive_dict[2] = True

    # check invalid types
    def test_invalid_type(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, int]({"a": "3"})  # type: ignore[dict-item]
        case_insensitive_dict[1] = 2  # type: ignore[index]
        case_insensitive_dict["b"] = "2"  # type: ignore[assignment]


class TestContains(CaseInsensitiveDictTestCase):
    # check that key in CaseInsensitiveDict check works as expected
    def test_contains(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        assert "A" in case_insensitive_dict
        assert "a" in case_insensitive_dict

    # check contains with non-str keys
    def test_contains_with_non_str_keys(self) -> None:
        case_insensitive_dict_int = CaseInsensitiveDict[int, str]({1: "b"})
        assert 1 in case_insensitive_dict_int
        case_insensitive_dict_bool = CaseInsensitiveDict[bool, str]({True: "b"})
        assert True in case_insensitive_dict_bool


class TestSetItem(CaseInsensitiveDictTestCase):
    # check key lowered
    def test_store_written(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        case_insensitive_dict["A"] = "b"
        assert case_insensitive_dict._data == {"a": ("A", "b")}

    # check init value overridden (case insensitive)
    def test_value(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b"})
        assert case_insensitive_dict._data == {"a": ("a", "b")}
        case_insensitive_dict["A"] = "c"
        assert case_insensitive_dict._data == {"a": ("A", "c")}

    # check set item with non-str keys
    def test_set_item_with_non_str_keys(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[int, str]({1: "b"})
        assert case_insensitive_dict._data == {1: (1, "b")}
        case_insensitive_dict[1] = "c"
        assert case_insensitive_dict._data == {1: (1, "c")}


class TestGetItem(CaseInsensitiveDictTestCase):
    # check value returned
    def test_value_returned(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b"})
        assert case_insensitive_dict["A"] == "b"
        assert case_insensitive_dict["a"] == "b"

    # check behaviour when key is missing
    def test_key_missing(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        assert case_insensitive_dict.get("b") is None
        with pytest.raises(KeyError, match=r"Key: 'b' not found."):
            assert case_insensitive_dict["b"]

    # check behaviour when key is missing and default passed
    def test_key_missing_with_default(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        assert case_insensitive_dict.get("b", 1) == 1

    # check value returned using get
    def test_value_returned_using_get(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b"})
        assert case_insensitive_dict.get("A") == "b"
        assert case_insensitive_dict.get("a") == "b"

    # check get item with non-str keys
    def test_get_item_with_non_str_keys(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[int, str]({1: "b"})
        assert case_insensitive_dict.get(1) == "b"
        assert case_insensitive_dict[1] == "b"

    # check instantiated with none value
    def test_store_written_with_optional_value(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, Optional[str]]({"A": None})
        assert case_insensitive_dict.get("a") is None
        assert case_insensitive_dict["a"] is None
        assert "a" in case_insensitive_dict


class TestDelItem(CaseInsensitiveDictTestCase):
    # check value removed
    def test_value_removed(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b"})
        assert case_insensitive_dict["a"] == "b"
        del case_insensitive_dict["A"]
        assert "a" not in case_insensitive_dict

    # check del item with non-str keys
    def test_del_item_with_non_str_keys(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[int, str]({1: "b"})
        assert case_insensitive_dict[1] == "b"
        del case_insensitive_dict[1]
        assert 1 not in case_insensitive_dict


class TestIter(CaseInsensitiveDictTestCase):
    # check iterated keys
    def test_iter(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b"})
        assert list(case_insensitive_dict) == ["a"]

    # check iter with non-str keys
    def test_iter_with_non_str_keys(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[Union[str, int], str]({1: "b", "a": "c"})
        assert list(case_insensitive_dict) == [1, "a"]


class TestLen(CaseInsensitiveDictTestCase):
    # check len
    def test_len(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"a": "b"})
        assert len(case_insensitive_dict) == 1

    # check len empty data
    def test_len_empty(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        assert len(case_insensitive_dict) == 0


class TestLowerItems(CaseInsensitiveDictTestCase):
    # check returned value
    def test_lower(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        assert list(case_insensitive_dict.lower_items()) == [("a", "b")]

    # check returned value for empty data
    def test_lower_empty(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        assert isinstance(case_insensitive_dict.lower_items(), GeneratorType)
        assert not list(case_insensitive_dict.lower_items())

    # check lower items with non-str keys
    def test_lower_items_with_non_str_keys(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[Union[str, int], str]({1: "b", "a": "c"})
        assert list(case_insensitive_dict.lower_items()) == [(1, "b"), ("a", "c")]


class TestEq(CaseInsensitiveDictTestCase):
    # check equality empty data
    def test_equality(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        assert case_insensitive_dict == CaseInsensitiveDict[str, str]()

    # check equality (case insensitive)
    def test_equality_empty(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        assert case_insensitive_dict == CaseInsensitiveDict[str, str]({})

    # check equality with dictionary
    def test_equality_dictionary(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        assert case_insensitive_dict == {"A": "b"}

    # check not equal
    def test_not_equality(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        assert case_insensitive_dict != 1

    # check equality with non-str keys
    def test_equality_with_non_str_keys(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[Union[str, int], str]({1: "b", "a": "c"})
        assert case_insensitive_dict == {1: "b", "a": "c"}


class TestCopy(CaseInsensitiveDictTestCase):
    # check copy equality
    def test_copy(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        assert case_insensitive_dict.copy() == case_insensitive_dict
        assert case_insensitive_dict == case_insensitive_dict.copy()

    # check copy ids
    def test_copy_ids(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        assert id(case_insensitive_dict) != id(case_insensitive_dict.copy())

    # check copy with non-str keys
    def test_copy_with_non_str_keys(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[Union[str, int], str]({1: "b", "a": "c"})
        assert case_insensitive_dict.copy() == case_insensitive_dict
        assert case_insensitive_dict == case_insensitive_dict.copy()


class TestGetKey(CaseInsensitiveDictTestCase):
    # check to ensure original key is returned after case-insensitive lookup
    def test_getkey(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        assert case_insensitive_dict.getkey('a') == 'A'
        assert case_insensitive_dict.getkey('A') == 'A'

    # check for key error
    def test_getkey_key_not_in_dictionary(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        with pytest.raises(KeyError):
            case_insensitive_dict.getkey("b")


class TestJson(CaseInsensitiveDictTestCase):
    # check to_json
    def test_to_json(self) -> None:
        data: Dict[Union[bool, str, int], Union[str, int, bool]] = {"A": "a", "b": 1, "c": False, 2: "a", True: 2}
        case_insensitive_dict = CaseInsensitiveDict[Union[bool, str, int], Union[str, int, bool]](data)
        json_string = json.dumps(obj=case_insensitive_dict, cls=CaseInsensitiveDictJSONEncoder)
        assert json_string == '{"A": "a", "b": 1, "c": false, "2": "a", "true": 2}'
        assert json_string == json.dumps(data)

    # check from_json
    def test_from_json(self) -> None:
        json_string = '{"A": "a", "b": 1, "c": false, "2": "a", "true": 2}'
        case_insensitive_dict = json.loads(s=json_string, object_hook=case_insensitive_dict_json_decoder)
        expected_case_insensitive_dict = CaseInsensitiveDict[Union[bool, str, int], Union[str, int, bool]]({"A": "a", "b": 1, "c": False, "2": "a", "true": 2})
        assert case_insensitive_dict == expected_case_insensitive_dict
        assert case_insensitive_dict == json.loads(json_string)


class TestStrAndRepr(CaseInsensitiveDictTestCase):
    # check string and representation
    def test_str_and_repr(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]({"A": "b"})
        assert case_insensitive_dict.__str__() == "CaseInsensitiveDict({'A': 'b'})"
        assert case_insensitive_dict.__repr__() == "CaseInsensitiveDict({'A': 'b'})"


class TestFromKeys(CaseInsensitiveDictTestCase):
    # check fromkeys
    def test_fromkeys(self) -> None:
        dictionary = dict.fromkeys(["A", "b"], "c")
        assert dictionary == {"A": "c", "b": "c"}
        case_insensitive_dict = CaseInsensitiveDict[str, str].fromkeys(["A", "b"], "c")
        assert case_insensitive_dict == dictionary


class TestDictMethods(CaseInsensitiveDictTestCase):
    # check dict
    def test_dict(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        assert dict(case_insensitive_dict) == dict(dictionary)

    # check dict with non-str keys
    def test_dict_with_non_str_keys(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[Union[str, int], str]({1: "b", "a": "c"})
        assert dict(case_insensitive_dict) == dict({1: "b", "a": "c"})

    # check falsey dict
    def test_falsey(self) -> None:
        case_insensitive_dict = CaseInsensitiveDict[str, str]()
        assert not case_insensitive_dict
        assert bool(case_insensitive_dict) is False
        assert not {}
        assert bool({}) is False

    # check truthy dict
    def test_truthy(self) -> None:
        dictionary = {"a": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        assert case_insensitive_dict
        assert bool(case_insensitive_dict) is True
        assert dictionary
        assert bool(dictionary) is True

    # check clear
    def test_clear(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        case_insensitive_dict.clear()
        assert not case_insensitive_dict
        dictionary.clear()
        assert not dictionary

    # check reference to instantiated value not maintained
    def test_reference(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        assert id(case_insensitive_dict._data) != id(dictionary)
        case_insensitive_dict.pop("a")
        assert dictionary == {"A": "b"}

    # check pop
    def test_pop(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        dict_response = dictionary.pop("A")
        response = case_insensitive_dict.pop("a")
        assert dict_response == response
        assert response == "b"
        assert not case_insensitive_dict
        assert not dictionary

    # check pop key not in dictionary
    def test_pop_key_not_in_dictionary(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        with pytest.raises(KeyError):
            case_insensitive_dict.pop("b")
        with pytest.raises(KeyError):
            dictionary.pop("b")

    # check pop key not in dictionary with default
    def test_pop_key_not_in_dictionary_with_default(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        dict_response = dictionary.pop("A")
        response = case_insensitive_dict.pop("a")
        assert dict_response == response
        assert response == "b"
        response = case_insensitive_dict.pop("b", "a")
        assert response == "a"

    # check popitem
    def test_pop_item(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        assert dictionary.popitem() == case_insensitive_dict.popitem() == ("A", "b")
        with pytest.raises(KeyError):
            case_insensitive_dict.popitem()
        with pytest.raises(KeyError):
            dictionary.popitem()

    # check keys
    def test_keys(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        assert dictionary.keys() == case_insensitive_dict.keys()
        assert list(dictionary.keys()) == list(case_insensitive_dict.keys()) == ["A"]

    # check values
    def test_values(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        assert list(dictionary.values()) == list(case_insensitive_dict.values()) == ["b"]

    # check items
    def test_items(self) -> None:
        dictionary = {"A": "b"}
        case_insensitive_dict = CaseInsensitiveDict[str, str](dictionary)
        assert list(dictionary.items()) == list(case_insensitive_dict.items()) == [("A", "b")]
