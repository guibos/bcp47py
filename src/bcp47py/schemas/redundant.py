"""Module related with Redundant classes."""
from datetime import datetime
from typing import Optional, Annotated, List

from pydantic import BaseModel, ConfigDict

from schemas.abstract.preferred_value import PreferredValue
from schemas.ext_lang import ExtLang
from schemas.field_info import TAG_FIELD_INFO
from schemas.language import Language
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.mixin.tag import Tag, _TAG_FIELD_INFO
from schemas.region import Region
from schemas.script import Script
from schemas.variant import Variant


class RedundantSubtags(BaseModel):
    language: Language
    extlang: List[ExtLang] = []
    script: Optional[Script] = None
    region: Optional[Region] = None
    variant: List[Variant] = []

    model_config = ConfigDict(extra='forbid')

    @property
    def tag(self) -> str:
        """Return a tag in string format."""
        return '-'.join((subtag.subtag
                         for subtag in (self.language, *self.extlang, self.script, self.region, *self.variant)
                         if subtag))


class RedundantPreferredValue(PreferredValue):
    """Class that adds :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.language.Language: and :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.script.Script` that could be set as
    preferred value for a :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.redundant.Redundant` type.

    Check :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.interface.preferred_value.PreferredValue` class for more information about preferred value."""
    language: Language
    script: Optional[Script] = None

    def tag(self) -> Annotated[str, TAG_FIELD_INFO]:
        return '-'.join([subtag.subtag for subtag in [self.language, self.script] if subtag])


class Redundant(Tag, PreferredValueValidator):
    """A redundant tag is a :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.grandfathered.Grandfathered` registration whose individual subtags appear
    with the same semantic meaning in the registry.

    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""

    preferred_value: Optional[RedundantPreferredValue] = None
    deprecated: Optional[datetime] = None
    subtags: RedundantSubtags

    @property
    def tag(self) -> Annotated[str, _TAG_FIELD_INFO]:
        return self.subtags.tag
