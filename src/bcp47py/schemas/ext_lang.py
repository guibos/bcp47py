"""Module related with ExtLangs classes."""

from datetime import datetime
from typing import List, Optional, Annotated

from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo

from schemas.abstract.preferred_value import PreferredValue
from schemas.abstract.prefix import Prefix
from schemas.field_info import DEPRECATED_FIELD_INFO, MACRO_LANGUAGE_FIELD_INFO
from schemas.language import Language
from schemas.mixin.subtag import Subtag


class ExtLangPreferredValue(PreferredValue):
    """Class that adds schemas.language.Language attribute that could be set as preferred value for an
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.ext_lang.ExtLang` type.

    Check :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.interface.preferred_value.PreferredValue` class for more information about preferred value."""
    language: Language

    @property
    def tag(self) -> str:
        return self.language.subtag


class ExtLangPrefix(Prefix):
    """Class that adds :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.language.Language` attribute, that could be set as preferred value
    from an :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.ext_lang.ExtLang` type.

    Check :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.interface.prefix.Prefix` class for more information about prefix."""
    language: Language

    @property
    def tag(self) -> str:
        return self.language.subtag


class ExtLang(Subtag):
    """Extended language subtags are used to identify certain specially selected :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.language.Language` that,
    for various historical and compatibility reasons, are closely identified with or tagged using an existing primary
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.language.Language` subtag.

    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""
    preferred_value: ExtLangPreferredValue
    prefix: List[ExtLangPrefix]
    macro_language: Annotated[Optional[Language], MACRO_LANGUAGE_FIELD_INFO] = None
    deprecated: Annotated[Optional[datetime], DEPRECATED_FIELD_INFO] = None

    @field_validator('preferred_value')
    def preferred_value_subtag_validator(cls, value: Language, validation_info: ValidationInfo):
        if value.language.subtag != validation_info.data['subtag']:
            raise ValueError('Preferred_value must be equal than subtag. In the moment of writing this validation all'
                             'extension languages are languages, so, it is possible that this validation it is not '
                             'necessary any more.')
        return value
