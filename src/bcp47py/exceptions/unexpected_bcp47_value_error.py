class UnexpectedBCP47ValueError(Exception):
    """Exception that should be raised when a bcp47 key is unexpected and is not possible to parse."""
    _MESSAGE_TEMPLATE = 'Unexpected BCP47 value: "{}" for key: "{}".'

    def __init__(self, unexpected_value: str, internal_name: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(unexpected_value, internal_name))
