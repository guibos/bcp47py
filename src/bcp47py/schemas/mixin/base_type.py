"""Module that contains BaseType mixin."""

from datetime import datetime
from typing import List, Annotated

from pydantic import ConfigDict, BaseModel, Field


class BaseType(BaseModel):
    """Mixin that must be used by all BCP47 types. Only contains fields that are common between all BCP47 types."""
    description: Annotated[
        List[str],
        Field(title="description",
              description="The field 'Description' contains a description of the tag or subtag in the record. "
              "The 'Description' field MAY appear more than once per record.  The 'Description' field MAY "
              "include the full range of Unicode characters. At least one of the 'Description' fields MUST be "
              "written or transcribed into the Latin script; additional 'Description' fields MAY be in any "
              "script or language.\n"
              "The 'Description' field is used for identification purposes. Descriptions SHOULD contain all and "
              "only that information necessary to distinguish one subtag from others with which it might be "
              "confused.  They are not intended to provide general background information or to provide all "
              "possible alternate names or designations. 'Description' fields don't necessarily represent the "
              "actual native name of the item in the record, nor are any of the descriptions guaranteed to be "
              "in any particular language (such as English or French, for example).",
              examples=[["English"], ["Spanish"], ["Modern Greek (1453-)"], ["Bengali", "Bangla"]])] = []

    added: Annotated[datetime, Field(
        title="added",
        examples=[datetime(2000, 12, 1)],
    )]
    updated_at: Annotated[
        datetime,
        Field(
            title="updated_at",
            description="Field that is always the datetime version of the provided language subtag registry.",
            examples=[datetime(2000, 12, 1)],
        )]

    model_config = ConfigDict(extra='forbid')