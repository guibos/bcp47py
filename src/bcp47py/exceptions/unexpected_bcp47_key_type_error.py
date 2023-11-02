from typing import Type


class UnexpectedBCP47KeyTypeError(RuntimeError):
    """Exception that should be raised when an unexpected key type and is not possible to manage the situation."""
    _MESSAGE_TEMPLATE = 'Unexpected BCP47 key type: "{}". Workflow is not correctly developed.'

    def __init__(self, unexpected_key_type: Type):
        super().__init__(self._MESSAGE_TEMPLATE.format(unexpected_key_type))
