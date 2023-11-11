"""InvalidGrandfatheredDataError class module."""
from enums.bcp47_type import BCP47Type
from exceptions.invalid_data.base.invalid_data_error import InvalidDataError


class InvalidGrandfatheredDataError(InvalidDataError):
    """Exception that should be raised when Grandfathered data is invalid."""
    _BCP47_TYPE = BCP47Type.GRANDFATHERED

    def _bcp47_type(self) -> BCP47Type:
        return self._BCP47_TYPE
