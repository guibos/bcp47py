from enums.bcp47_type import BCP47Type


class UnexpectedBCP47TypeError(RuntimeError):
    """Exception that should be raised when an unexpected BCP47 type and is not possible to manage the situation."""
    _MESSAGE_TEMPLATE = 'Unexpected BCP47 type: "{}". Workflow is not correctly developed.'

    def __init__(self, bcp47_type: BCP47Type):
        super().__init__(self._MESSAGE_TEMPLATE.format(bcp47_type))