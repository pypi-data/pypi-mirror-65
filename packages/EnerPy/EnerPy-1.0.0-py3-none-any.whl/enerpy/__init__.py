from enerpy._api import API
from enerpy._types import EIASeries, Frequency


# region Exceptions
class APIKeyError(Exception):
    pass


class NoResultsError(Exception):
    pass


class BroadCategory(Exception):
    pass


class DateFormatError(Exception):
    pass


class InvalidSeries(Exception):
    pass


class UndefinedError(Exception):
    pass


class SeriesTypeError(Exception):
    pass

# endregion
