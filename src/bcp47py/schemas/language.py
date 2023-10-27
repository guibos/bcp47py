from datetime import datetime
from typing import Optional, Annotated

from pydantic import ConfigDict, BaseModel

from schemas.field_info import MACRO_LANGUAGE_FIELD_INFO
from schemas.mixin.subtag import Subtag
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.language_scope import LanguageScope
from schemas.script import Script


class LanguagePreferredValue(BaseModel):
    """Class that implements language that could be set as preferred value from a Language type.

    Check :class:schemas.abstract.preferred_value.PreferredValue class for more information about preferred value."""
    language: 'Language'
    model_config = ConfigDict(extra='forbid')


class Language(Subtag, PreferredValueValidator):
    macro_language: Annotated[Optional['Language'], MACRO_LANGUAGE_FIELD_INFO] = None
    scope: Optional[LanguageScope] = None
    comments: Optional[str] = None
    suppress_script: Optional[Script] = None
    preferred_value: Optional[LanguagePreferredValue] = None
    deprecated: Optional[datetime] = None
