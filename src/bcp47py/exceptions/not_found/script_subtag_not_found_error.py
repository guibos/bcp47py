from exceptions.not_found.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError


class ScriptSubtagNotFoundError(TagOrSubtagNotFoundError):
    """Exception raised when a script subtag is not found."""
    _MESSAGE_TEMPLATE = 'Script subtag not found: "{}".'

    def __init__(self, script_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(script_subtag))
