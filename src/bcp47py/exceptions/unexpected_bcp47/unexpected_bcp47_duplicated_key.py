class UnexpectedBCP47DuplicatedKeyError(Exception):
    """Exception that should be raised when a bcp47 item has a duplicated ."""
    _MESSAGE_TEMPLATE = 'Unexpected BCP47 key: "{}".'

    def __init__(self, unexpected_key: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(unexpected_key))
