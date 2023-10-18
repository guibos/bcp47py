from datetime import datetime
from typing import Optional, List

from pydantic import ConfigDict, BaseModel

from schemas.mixin.tag import Tag
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.language import Language
from schemas.region import Region
from schemas.variant import Variant, VariantPrefix


class GrandfatheredPreferredValue(BaseModel):
    language: Language
    region: Optional[Region] = None
    variant: Optional[Variant] = None
    model_config = ConfigDict(extra='forbid')


class GrandfatheredPrefix(VariantPrefix):
    pass


class Grandfathered(Tag, PreferredValueValidator):
    prefix: List['GrandfatheredPrefix'] = []
    comments: Optional[str] = None
    preferred_value: Optional['GrandfatheredPreferredValue'] = None
    deprecated: Optional[datetime] = None
