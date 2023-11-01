class FileDateNotFoundInLanguageSubtagRegistryError(Exception):
    """Exception that should be raised when File-Date is not present in the "Language subtag registry"."""
    _MESSAGE_TEMPLATE = 'File-Date is not present in the "Language subtag registry".'

    def __init__(self):
        super().__init__(self._MESSAGE_TEMPLATE)
