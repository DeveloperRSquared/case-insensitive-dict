from __future__ import annotations

import sys
from collections import abc
from json import JSONEncoder
from typing import Any
from typing import Dict
from typing import Generic
from typing import Iterable
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import TypeVar
from typing import Union
from typing import overload

KT = TypeVar('KT')  # pylint: disable=invalid-name
VT = TypeVar('VT')  # pylint: disable=invalid-name


if sys.version_info < (3, 9):
    MutableMapping = abc.MutableMapping
else:
    MutableMapping = abc.MutableMapping[KT, VT]  # pylint: disable=unsubscriptable-object


class CaseInsensitiveDict(MutableMapping, Generic[KT, VT]):
    @overload
    def __init__(self, data: Optional[Mapping[KT, VT]] = None) -> None:
        ...

    @overload
    def __init__(self, data: Optional[Iterable[Tuple[KT, VT]]] = None) -> None:
        ...

    def __init__(self, data: Optional[Union[Mapping[KT, VT], Iterable[Tuple[KT, VT]]]] = None) -> None:
        # Mapping from lowercased key to tuple of (actual key, value)
        self._data: Dict[KT, Tuple[KT, VT]] = {}
        if data is None:
            data = {}
        self.update(data)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({dict(self.items())!r})'

    @staticmethod
    def _convert_key(key: KT) -> KT:
        if isinstance(key, str):
            return key.lower()  # type: ignore[return-value]
        return key

    def __setitem__(self, key: KT, value: VT) -> None:
        self._data[self._convert_key(key=key)] = (key, value)

    def __getitem__(self, key: KT) -> VT:
        try:
            return self._data[self._convert_key(key=key)][1]
        except KeyError:
            raise KeyError(f"Key: {key!r} not found.") from None

    def __delitem__(self, key: KT) -> None:
        del self._data[self._convert_key(key=key)]

    def __iter__(self) -> Iterator[KT]:
        return (key for key, _ in self._data.values())

    def __len__(self) -> int:
        return len(self._data)

    def lower_items(self) -> Iterator[Tuple[KT, VT]]:
        return ((key, val[1]) for key, val in self._data.items())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, abc.Mapping):
            return False
        other_dict = CaseInsensitiveDict[Any, Any](data=other)
        return dict(self.lower_items()) == dict(other_dict.lower_items())

    def copy(self) -> CaseInsensitiveDict[KT, VT]:
        return CaseInsensitiveDict(data=dict(self._data.values()))

    @classmethod
    def fromkeys(cls, iterable: Iterable[KT], value: VT) -> CaseInsensitiveDict[KT, VT]:
        return cls([(key, value) for key in iterable])


class CaseInsensitiveDictJSONEncoder(JSONEncoder):
    def default(self, o: CaseInsensitiveDict[KT, VT]) -> Mapping[KT, VT]:
        return dict(o._data.values())  # pylint: disable=protected-access


def case_insensitive_dict_json_decoder(data: Mapping[KT, VT]) -> CaseInsensitiveDict[KT, VT]:
    return CaseInsensitiveDict(data=data)
