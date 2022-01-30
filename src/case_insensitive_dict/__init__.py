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

from .utils import DayOfWeek
from .utils import get_day_of_week
from .utils import is_weekend
from .utils import is_weekday
from .utils import get_previous_business_day
from .utils import get_next_business_day
from .utils import get_first_business_day_of_month
from .utils import get_nth_business_day_of_month
from .utils import datetime_to_string
from .utils import date_to_string
from .utils import datetime_from_string
from .utils import date_from_string
from .utils import datetime_from_windows_filetime
from .utils import datetime_from_seconds
from .utils import datetime_from_millis
from .utils import datetime_from_date
from .utils import datetime_to_seconds
from .utils import datetime_to_millis
