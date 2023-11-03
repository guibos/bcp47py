from exceptions.not_found.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError


class GrandfatheredTagNotFoundError(TagOrSubtagNotFoundError):
    """Exception raised when a grandfathered tag is not found."""
    _MESSAGE_TEMPLATE = 'Grandfathered tag not found: "{}".'

    def __init__(self, grandfathered_tag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(grandfathered_tag))
