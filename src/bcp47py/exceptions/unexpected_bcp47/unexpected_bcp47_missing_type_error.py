class UnexpectedBCP47MissingTypeError(RuntimeError):
    """Exception that should be raised when an unexpected_bcp47 key type and is not possible to manage the situation."""
    _MESSAGE_TEMPLATE = 'Unexpected workflow bcp_type was not retrieved'

    def __init__(self):
        super().__init__(self._MESSAGE_TEMPLATE)
