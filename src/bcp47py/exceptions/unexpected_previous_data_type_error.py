from typing import Type


class UnexpectedPreviousDataTypeError(Exception):
    """Exception that should be raised when previous data type that are not managed to be appended"""
    _MESSAGE_TEMPLATE = '"Unexpected previous data type that are not managed to be appended": "{}".'

    def __init__(self, previous_data_type: Type):
        super().__init__(self._MESSAGE_TEMPLATE.format(previous_data_type))
