from enums.bcp47_type import BCP47Type
from exceptions.invalid_data.base.invalid_data_error import InvalidDataError


class InvalidExtLanguageDataError(InvalidDataError):
    """Exception that should be raised when ExtLanguage data is invalid."""
    _DATA_TYPE = BCP47Type.EXTLANG.value

    def __init__(self):
        super().__init__(self._DATA_TYPE)
