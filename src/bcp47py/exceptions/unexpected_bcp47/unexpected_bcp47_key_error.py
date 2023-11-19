class UnexpectedBCP47KeyError(Exception):
    """Exception that should be raised when a bcp47 key is unexpected_bcp47 and is not possible to parse."""
    _MESSAGE_TEMPLATE = 'Unexpected BCP47 key: "{}".'

    def __init__(self, unexpected_key: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(unexpected_key))
