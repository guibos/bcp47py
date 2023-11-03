from typing import Dict, Any

from enums.bcp47_type import BCP47Type


class InvalidDataError(RuntimeError):
    """Exception that should when dat is invalid."""
    _MESSAGE_TEMPLATE = '{} data is invalid.'

    def __init__(self, bcp47_type: BCP47Type, data: Dict[str, Any]):
        super().__init__(self._MESSAGE_TEMPLATE.format(bcp47_type.value))
