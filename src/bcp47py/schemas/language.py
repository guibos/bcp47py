from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel

from schemas.mixin.subtag import Subtag
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.language_scope import LanguageScope
from schemas.script import Script


class LanguagePreferredValue(BaseModel):
    language: 'Language'
    model_config = ConfigDict(extra='forbid')


class Language(Subtag, PreferredValueValidator):
    macro_language: Optional['Language'] = None
    scope: Optional[LanguageScope] = None
    comments: Optional[str] = None
    suppress_script: Optional[Script] = None
    preferred_value: Optional[LanguagePreferredValue] = None
    deprecated: Optional[datetime] = None
