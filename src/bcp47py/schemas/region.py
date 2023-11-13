"""Module related with Region classes."""
from datetime import datetime
from typing import Optional, Annotated, List

from schemas.abstract.preferred_value import PreferredValue
from schemas.field_info import DEPRECATED_FIELD_INFO, COMMENTS_FIELD_INFO, TAG_FIELD_INFO
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.mixin.subtag import Subtag


class RegionPreferredValue(PreferredValue):
    """Class that adds :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.region.Region` that could be set as preferred value for a
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.region.Region` type.

    Check :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.abstract.preferred_value.PreferredValue` class for more information about preferred value."""
    region: 'Region'

    def tag(self) -> Annotated[str, TAG_FIELD_INFO]:
        return self.region.subtag


class Region(Subtag, PreferredValueValidator):
    """Region subtags are used to indicate linguistic variations associated with or appropriate to a specific country,
    territory, or region.

    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""
    comments: Annotated[List[str], COMMENTS_FIELD_INFO] = []
    preferred_value: Optional[RegionPreferredValue] = None
    deprecated: Annotated[Optional[datetime], DEPRECATED_FIELD_INFO] = None
