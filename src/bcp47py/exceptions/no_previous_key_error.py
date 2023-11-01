class NoPreviousKeyError(Exception):
    _MESSAGE_TEMPLATE = "There was no previous key to which it should be concatenated"

    def __init__(self):
        super().__init__(self._MESSAGE_TEMPLATE)