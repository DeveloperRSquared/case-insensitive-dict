from __future__ import annotations

import sys
from collections import abc
from typing import Any
from typing import Dict
from typing import Generic
from typing import Iterator
from typing import Mapping
from typing import Optional
from typing import Tuple
from typing import TypeVar

T = TypeVar('T')


if sys.version_info < (3, 9):
    AbcMutableMapping = abc.MutableMapping
else:
    AbcMutableMapping = abc.MutableMapping[str, T]  # pylint: disable=unsubscriptable-object


class CaseInsensitiveDict(AbcMutableMapping, Generic[T]):
    def __init__(self, data: Optional[Mapping[str, T]] = None) -> None:
        # Mapping from lowercased key to tuple of (actual key, value)
        self._data: Dict[str, Tuple[str, T]] = {}
        if data is None:
            data = {}
        self.update(data)

    def __setitem__(self, key: str, value: T) -> None:
        self._data[key.lower()] = (key, value)

    def __getitem__(self, key: str) -> T:
        return self._data[key.lower()][1]

    def __delitem__(self, key: str) -> None:
        del self._data[key.lower()]

    def __iter__(self) -> Iterator[str]:
        return (key for key, _ in self._data.values())

    def __len__(self) -> int:
        return len(self._data)

    def lower_items(self) -> Iterator[Tuple[str, T]]:
        return ((key, val[1]) for key, val in self._data.items())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, abc.Mapping):
            return False
        other_dict = CaseInsensitiveDict[Any](data=other)
        return dict(self.lower_items()) == dict(other_dict.lower_items())

    def copy(self) -> CaseInsensitiveDict[T]:
        return CaseInsensitiveDict(data=dict(self._data.values()))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({dict(self.items())!r})'
