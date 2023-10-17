from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel

from schemas.abstract.tag import Tag
from schemas.abstract.preferred_value_validator import PreferredValueValidator
from schemas.language import Language
from schemas.script import Script


class RedundantPreferredValue(BaseModel):
    language: Language
    script: Optional[Script] = None
    model_config = ConfigDict(extra='forbid')


class Redundant(Tag, PreferredValueValidator):
    preferred_value: Optional[RedundantPreferredValue] = None
    deprecated: Optional[datetime] = None
