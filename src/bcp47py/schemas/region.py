from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel

from schemas.abstract.subtag import Subtag
from schemas.abstract.preferred_value_validator import PreferredValueValidator


class RegionPreferredValue(BaseModel):
    region: 'Region'
    model_config = ConfigDict(extra='forbid')


class Region(Subtag, PreferredValueValidator):
    comments: Optional[str] = None
    preferred_value: Optional[RegionPreferredValue] = None
    deprecated: Optional[datetime] = None
