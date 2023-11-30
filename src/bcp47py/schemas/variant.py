"""Module related with Variant classes."""
from datetime import datetime
from typing import List, Optional, Annotated

from schemas.abstract.preferred_value import PreferredValue
from schemas.ext_lang import ExtLangPrefix, ExtLang
from schemas.field_info import TAG_FIELD_INFO, COMMENTS_FIELD_INFO, DEPRECATED_FIELD_INFO
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.mixin.subtag import Subtag
from schemas.region import Region
from schemas.script import Script


class VariantPreferredValue(PreferredValue):
    """Class that adds :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.variant.Variant` attribute that could be set as preferred value for a
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.variant.Variant` type.

    Check :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.abstract.preferred_value.PreferredValue` class for more information about preferred value."""

    variant: 'Variant'

    def tag(self) -> Annotated[str, TAG_FIELD_INFO]:
        return self.variant.subtag


class VariantPrefix(ExtLangPrefix):
    """Class that adds :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.ext_lang.ExtLang`, :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.script.Script`, :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.region.Region` and
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.variant.Variant` attributes, that could be set as preferred value from an
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.variant.Variant` type.

    Check :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.abstract.prefix.Prefix` class for more information about prefix."""

    ext_lang: Optional[ExtLang] = None
    script: Optional[Script] = None
    region: Optional[Region] = None
    variant: Optional['Variant'] = None

    @property
    def tag(self) -> str:
        return '-'.join((subtag.subtag
                         for subtag in (self.language, self.ext_lang, self.script, self.region, self.variant)
                         if subtag))


class Variant(Subtag, PreferredValueValidator):
    prefix: List[VariantPrefix] = []
    comments: Annotated[List[str], COMMENTS_FIELD_INFO] = []
    preferred_value: Optional[VariantPreferredValue] = None
    deprecated: Annotated[Optional[datetime], DEPRECATED_FIELD_INFO] = None
