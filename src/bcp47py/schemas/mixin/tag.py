"""Module that contains Tag abstract class."""
from typing import Annotated

from pydantic import Field

from schemas.mixin.base_type import BaseType

_TAG_FIELD_INFO = Field(
    title="tag",
    description="""The field 'Tag' appears in records whose 'Type' is either 'grandfathered' or 'redundant' and 
    contains a tag registered under [RFC3066].
    
    Extract from https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=["art-lojban", "zh-yue"])


class Tag(BaseType):
    """Mixin that must be used by tag types (only :class:`from exceptions.invalid.base.invalid_data_error import InvalidDataErrorschemas.redundant.Redundant` and
    :class:`from exceptions.invalid.base.invalid_data_error import InvalidDataErrorschemas.grandfathered.Grandfathered` types)."""
    tag: Annotated[str, _TAG_FIELD_INFO]
