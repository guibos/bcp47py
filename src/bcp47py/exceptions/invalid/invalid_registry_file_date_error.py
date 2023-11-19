class InvalidRegistryFileDate(Exception):
    """Exception that should be raised when the File-Date field has not the correct format."""
    _MESSAGE_TEMPLATE = 'File-Date has not the correct format: "{}"'

    def __init__(self, file_date: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(file_date))
