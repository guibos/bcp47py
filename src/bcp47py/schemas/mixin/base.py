from datetime import datetime
from typing import List

from pydantic import ConfigDict, BaseModel


class Base(BaseModel):
    description: List[str] = []
    added: datetime
    updated_at: datetime

    model_config = ConfigDict(extra='forbid')
