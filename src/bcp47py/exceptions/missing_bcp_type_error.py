class MissingBCPTypeError(RuntimeError):
    """Exception that should be raised when an unexpected key type and is not possible to manage the situation."""
    _MESSAGE_TEMPLATE = 'Unexpected workflow bcp_type was not retrieved'

    def __init__(self):
        super().__init__(self._MESSAGE_TEMPLATE)
