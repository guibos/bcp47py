from exceptions.not_found.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError


class VariantSubtagNotFoundError(TagOrSubtagNotFoundError):
    """Exception raised when a variant subtag is not found."""
    _MESSAGE_TEMPLATE = 'Variant subtag not found: "{}".'

    def __init__(self, variant_subtag: str):
        super().__init__(self._MESSAGE_TEMPLATE.format(variant_subtag))
