"""Module related with Language classes."""
from datetime import datetime
from typing import Optional, Annotated, List

from schemas.abstract.preferred_value import PreferredValue
from schemas.field_info import MACRO_LANGUAGE_FIELD_INFO, DEPRECATED_FIELD_INFO, TAG_FIELD_INFO, COMMENTS_FIELD_INFO
from schemas.language_scope import LanguageScope
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.mixin.subtag import Subtag
from schemas.script import Script


class LanguagePreferredValue(PreferredValue):
    """Class that adds :class:`from exceptions.invalid.base.invalid_data_error import InvalidDataErrorschemas.language.Language` attribute that could be set as preferred value for a
    :class:`from exceptions.invalid.base.invalid_data_error import InvalidDataErrorschemas.language.Language` type.

    Check :class:`from exceptions.invalid.base.invalid_data_error import InvalidDataErrorschemas.abstract.preferred_value.PreferredValue` class for more information about preferred value."""
    language: 'Language'

    def tag(self) -> Annotated[str, TAG_FIELD_INFO]:
        return self.language.subtag


class Language(Subtag, PreferredValueValidator):
    """The primary language subtag is the first subtag in a language tag.

    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""

    macro_language: Annotated[Optional['Language'], MACRO_LANGUAGE_FIELD_INFO] = None
    scope: Optional[LanguageScope] = None
    comments: Annotated[List[str], COMMENTS_FIELD_INFO] = []
    suppress_script: Optional[Script] = None
    preferred_value: Optional[LanguagePreferredValue] = None
    deprecated: Annotated[Optional[datetime], DEPRECATED_FIELD_INFO] = None
