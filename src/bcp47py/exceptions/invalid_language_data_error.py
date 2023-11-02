class InvalidLanguageDataError(RuntimeError):
    """Exception that should be raised when Language data is invalid."""
    _MESSAGE_TEMPLATE = 'Language data is invalid.'

    def __init__(self):
        super().__init__(self._MESSAGE_TEMPLATE)
