"""Module that contains BaseType abstract."""

from datetime import datetime
from typing import List, Annotated

from pydantic import ConfigDict, BaseModel, Field

_DESCRIPTION_FIELD_INFO = Field(
    title="description",
    description="""The field 'Description' contains a description of the tag or subtag in the record. The 'Description' 
    field MAY appear more than once per record.
     
    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=[["English"], ["Spanish"], ["Modern Greek (1453-)"], ["Bengali", "Bangla"]])

_ADDED_FIELD_INFO = Field(
    title="added",
    examples=[datetime(2000, 12, 1)],
)
_UPDATED_AT_FIELD_INFO = Field(
    title="updated_at",
    description="""Field that is always the datetime version of the provided language subtag registry.
    
    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=[datetime(2000, 12, 1)],
)


class BaseType(BaseModel):
    """Mixin that must be used by all BCP47 types. Only contains fields that are common between all BCP47 types."""
    description: Annotated[List[str], _DESCRIPTION_FIELD_INFO]
    added: Annotated[datetime, _ADDED_FIELD_INFO]
    updated_at: Annotated[datetime, _UPDATED_AT_FIELD_INFO]

    model_config = ConfigDict(extra='forbid')
