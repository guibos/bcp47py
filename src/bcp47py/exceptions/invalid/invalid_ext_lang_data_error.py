"""InvalidExtLanguageDataError class module."""

from enums.bcp47_type import BCP47Type
from exceptions.invalid.mixin.invalid_data_error import InvalidDataError


class InvalidExtLanguageDataError(InvalidDataError):
    """Exception that should be raised when ExtLanguage data is invalid."""
    _BCP47_TYPE = BCP47Type.EXTLANG

    @property
    def _bcp47_type(self) -> BCP47Type:
        return self._BCP47_TYPE
