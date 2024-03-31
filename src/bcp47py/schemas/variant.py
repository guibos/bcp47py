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

    variant: List['Variant'] = []

    @property
    def tag(self) -> Annotated[str, TAG_FIELD_INFO]:
        return '-'.join(variant.subtag for variant in self.variant)


class VariantPrefix(ExtLangPrefix):
    """Class that adds :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.ext_lang.ExtLang`, :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.script.Script`, :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.region.Region` and
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.variant.Variant` attributes, that could be set as preferred value from an
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.variant.Variant` type.

    Check :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.abstract.prefix.Prefix` class for more information about prefix."""

    extlang: List[ExtLang] = []
    script: Optional[Script] = None
    region: Optional[Region] = None
    variant: List['Variant'] = []

    @property
    def tag(self) -> str:
        return '-'.join(subtag.subtag
                        for subtag in (self.language, *self.extlang, self.script, self.region, *self.variant) if subtag)


class Variant(Subtag, PreferredValueValidator):
    prefix: List[VariantPrefix] = []
    comments: Annotated[List[str], COMMENTS_FIELD_INFO] = []
    preferred_value: Optional[VariantPreferredValue] = None
    deprecated: Annotated[Optional[datetime], DEPRECATED_FIELD_INFO] = None
