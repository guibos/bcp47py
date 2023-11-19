from abc import ABC, abstractmethod
from typing import Dict, Any

from enums.bcp47_type import BCP47Type


class InvalidDataError(RuntimeError, ABC):
    """Exception that should when dat is invalid."""
    _MESSAGE_TEMPLATE = '{} data is invalid.'

    def __init__(self, data: Dict[str, Any]):
        super().__init__(self._MESSAGE_TEMPLATE.format(self._bcp47_type.value))

    @property
    @abstractmethod
    def _bcp47_type(self) -> BCP47Type:
        """Returns bcp47 type"""
