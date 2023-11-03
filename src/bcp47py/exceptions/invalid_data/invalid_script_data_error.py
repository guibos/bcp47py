class InvalidScriptDataError(RuntimeError):
    """Exception that should be raised when Script data is invalid."""
    _MESSAGE_TEMPLATE = 'Script data is invalid.'

    def __init__(self):
        super().__init__(self._MESSAGE_TEMPLATE)
