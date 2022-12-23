# isort: skip_file
# pylint: disable=wrong-import-position
try:
    from importlib.metadata import version
    from importlib.metadata import PackageNotFoundError
except ImportError:
    from importlib_metadata import version  # type: ignore[no-redef]
    from importlib_metadata import PackageNotFoundError  # type: ignore[no-redef,misc]

try:
    __version__: str = version('case-insensitive-dictionary')
except PackageNotFoundError:
    __version__ = "unknown"

from .case_insensitive_dict import CaseInsensitiveDict
from .case_insensitive_dict import CaseInsensitiveDictJSONEncoder
from .case_insensitive_dict import case_insensitive_dict_json_decoder

__all__ = ['CaseInsensitiveDict', 'CaseInsensitiveDictJSONEncoder', 'case_insensitive_dict_json_decoder']
