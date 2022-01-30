# isort: skip_file
# pylint: disable=wrong-import-position
try:
    from importlib.metadata import version
    from importlib.metadata import PackageNotFoundError
except ImportError:
    from importlib_metadata import version  # type: ignore[no-redef]
    from importlib_metadata import PackageNotFoundError  # type: ignore[no-redef,misc]

try:
    __version__: str = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"
